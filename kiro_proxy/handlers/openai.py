"""OpenAI 协议处理 - /v1/chat/completions"""
import json
import uuid
import time
import asyncio
import httpx
from ..core.http_pool import http_pool
from datetime import datetime
from fastapi import Request, HTTPException
from fastapi.responses import StreamingResponse

from ..config import KIRO_API_URL, map_model_name
from ..core import state, is_retryable_error, stats_manager, flow_monitor, TokenUsage
from ..core.state import RequestLog
from ..core.history_manager import HistoryManager, get_history_config, is_content_length_error
from ..core.error_handler import classify_error, ErrorType, format_error_log
from ..core.rate_limiter import get_rate_limiter
from ..kiro_api import build_headers, build_kiro_request, parse_event_stream, parse_event_stream_full, is_quota_exceeded_error
from ..converters import (
    generate_session_id,
    convert_openai_messages_to_kiro,
    convert_kiro_response_to_openai,
    extract_images_from_content,
    fix_history_alternation,
)


async def handle_chat_completions(request: Request):
    """处理 /v1/chat/completions 请求"""
    start_time = time.time()
    log_id = uuid.uuid4().hex[:8]
    
    body = await request.json()
    model = map_model_name(body.get("model", "claude-sonnet-4"))
    messages = body.get("messages", [])
    stream = body.get("stream", False)
    tools = body.get("tools", None)
    tool_choice = body.get("tool_choice", None)
    
    if not messages:
        raise HTTPException(400, "messages required")
    
    session_id = generate_session_id(messages)
    account = state.get_available_account(session_id)
    
    if not account:
        raise HTTPException(503, "All accounts are rate limited or unavailable")
    
    # 创建 Flow 记录
    flow_id = flow_monitor.create_flow(
        protocol="openai",
        method="POST",
        path="/v1/chat/completions",
        headers=dict(request.headers),
        body=body,
        account_id=account.id,
        account_name=account.name,
    )
    
    # 检查 token 是否即将过期，尝试刷新
    if account.is_token_expiring_soon(5):
        print(f"[OpenAI] Token 即将过期，尝试刷新: {account.id}")
        success, msg = await account.refresh_token()
        if not success:
            print(f"[OpenAI] Token 刷新失败: {msg}")
    
    token = account.get_token()
    if not token:
        raise HTTPException(500, f"Failed to get token for account {account.name}")
    
    # 使用账号的动态 Machine ID（提前构建，供摘要使用）
    creds = account.get_credentials()
    headers = build_headers(
        token,
        machine_id=account.get_machine_id(),
        profile_arn=creds.profile_arn if creds else None,
        client_id=creds.client_id if creds else None
    )
    
    # 限速检查
    rate_limiter = get_rate_limiter()
    can_request, wait_seconds, reason = rate_limiter.can_request(account.id)
    if not can_request:
        print(f"[OpenAI] 限速: {reason}")
        await asyncio.sleep(wait_seconds)
    
    # 使用增强的转换函数
    user_content, history, tool_results, kiro_tools = convert_openai_messages_to_kiro(
        messages, model, tools, tool_choice
    )
    
    # 历史消息预处理
    history_manager = HistoryManager(get_history_config(), cache_key=session_id)
    
    async def call_summary(prompt: str) -> str:
        req = build_kiro_request(prompt, "claude-haiku-4.5", [])
        try:
            resp = await http_pool.short_client.post(KIRO_API_URL, json=req, headers=headers)
            if resp.status_code == 200:
                return parse_event_stream(resp.content)
        except Exception as e:
            print(f"[Summary] API 调用失败: {e}")
        return ""

    # 检查是否需要智能摘要或错误重试预摘要
    if history_manager.should_summarize(history) or history_manager.should_pre_summary_for_error_retry(history, user_content):
        history = await history_manager.pre_process_async(history, user_content, call_summary)
    else:
        history = history_manager.pre_process(history, user_content)
    
    # 摘要/截断后再次修复历史交替和 toolUses/toolResults 配对
    history = fix_history_alternation(history)
    
    if history_manager.was_truncated:
        print(f"[OpenAI] {history_manager.truncate_info}")

    
    # 提取最后一条消息中的图片
    images = []
    if messages:
        last_msg = messages[-1]
        if last_msg.get("role") == "user":
            _, images = await extract_images_from_content(last_msg.get("content", ""))
    
    kiro_request = build_kiro_request(
        user_content, model, history, 
        images=images,
        tools=kiro_tools if kiro_tools else None,
        tool_results=tool_results if tool_results else None
    )
    
    error_msg = None
    status_code = 200
    result = None  # parse_event_stream_full 返回的完整结构
    current_account = account
    max_retries = 2
    
    for retry in range(max_retries + 1):
        try:
            resp = await http_pool.api_client.post(KIRO_API_URL, json=kiro_request, headers=headers)
            status_code = resp.status_code
            
            # 处理配额超限
            if resp.status_code == 429 or is_quota_exceeded_error(resp.status_code, resp.text):
                current_account.mark_quota_exceeded("Rate limited")
                
                # 尝试切换账号
                next_account = state.get_next_available_account(current_account.id)
                if next_account and retry < max_retries:
                    print(f"[OpenAI] 配额超限，切换账号: {current_account.id} -> {next_account.id}")
                    current_account = next_account
                    token = current_account.get_token()
                    creds = current_account.get_credentials()
                    headers = build_headers(
                        token,
                        machine_id=current_account.get_machine_id(),
                        profile_arn=creds.profile_arn if creds else None,
                        client_id=creds.client_id if creds else None
                    )
                    continue
                
                if flow_id:
                    flow_monitor.fail_flow(flow_id, "rate_limit_error", "All accounts rate limited", 429)
                raise HTTPException(429, "All accounts rate limited")
            
            # 处理可重试的服务端错误
            if is_retryable_error(resp.status_code):
                if retry < max_retries:
                    print(f"[OpenAI] 服务端错误 {resp.status_code}，重试 {retry + 1}/{max_retries}")
                    await asyncio.sleep(0.5 * (2 ** retry))
                    continue
                if flow_id:
                    flow_monitor.fail_flow(flow_id, "api_error", "Server error after retries", resp.status_code)
                raise HTTPException(resp.status_code, f"Server error after {max_retries} retries")
            
            if resp.status_code != 200:
                error_msg = resp.text
                print(f"[OpenAI] Kiro API error {resp.status_code}: {resp.text[:500]}")
                
                # 使用统一的错误处理
                error = classify_error(resp.status_code, error_msg)
                print(format_error_log(error, current_account.id))
                
                # 账号封禁 - 禁用账号
                if error.should_disable_account:
                    current_account.enabled = False
                    from ..credential import CredentialStatus
                    current_account.status = CredentialStatus.SUSPENDED
                    print(f"[OpenAI] 账号 {current_account.id} 已被禁用 (封禁)")
                
                # 配额超限 - 标记冷却
                if error.type == ErrorType.RATE_LIMITED:
                    current_account.mark_quota_exceeded(error_msg[:100])
                
                # 尝试切换账号
                if error.should_switch_account:
                    next_account = state.get_next_available_account(current_account.id)
                    if next_account and retry < max_retries:
                        print(f"[OpenAI] 切换账号: {current_account.id} -> {next_account.id}")
                        current_account = next_account
                        headers["Authorization"] = f"Bearer {current_account.get_token()}"
                        continue
                
                # 检查是否为内容长度超限错误，尝试截断重试
                if error.type == ErrorType.CONTENT_TOO_LONG:
                    history_chars, user_chars, total_chars = history_manager.estimate_request_chars(
                        history, user_content
                    )
                    print(f"[OpenAI] 内容长度超限: history={history_chars} chars, user={user_chars} chars, total={total_chars} chars")
                    truncated_history, should_retry = await history_manager.handle_length_error_async(
                        history, retry, call_summary
                    )
                    if should_retry:
                        print(f"[OpenAI] 内容长度超限，{history_manager.truncate_info}")
                        history = truncated_history
                        kiro_request = build_kiro_request(
                            user_content, model, history,
                            images=images,
                            tools=kiro_tools if kiro_tools else None,
                            tool_results=tool_results if tool_results else None
                        )
                        continue
                    else:
                        print(f"[OpenAI] 内容长度超限但未重试: retry={retry}/{max_retries}")
                
                if flow_id:
                    flow_monitor.fail_flow(flow_id, error.type.value if hasattr(error.type, 'value') else str(error.type), error.user_message, resp.status_code, error_msg[:500])
                raise HTTPException(resp.status_code, error.user_message)
            
            # 成功：解析完整响应（包含 tool_uses）
            result = parse_event_stream_full(resp.content)
            current_account.request_count += 1
            current_account.last_used = time.time()
            get_rate_limiter().record_request(current_account.id)
            break
                
        except HTTPException:
            raise
        except httpx.TimeoutException:
            error_msg = "Request timeout"
            status_code = 408
            if retry < max_retries:
                print(f"[OpenAI] 请求超时，重试 {retry + 1}/{max_retries}")
                await asyncio.sleep(0.5 * (2 ** retry))
                continue
            if flow_id:
                flow_monitor.fail_flow(flow_id, "timeout", "Request timeout after retries", 408)
            raise HTTPException(408, "Request timeout after retries")
        except httpx.ConnectError:
            error_msg = "Connection error"
            status_code = 502
            if retry < max_retries:
                print(f"[OpenAI] 连接错误，重试 {retry + 1}/{max_retries}")
                await asyncio.sleep(0.5 * (2 ** retry))
                continue
            if flow_id:
                flow_monitor.fail_flow(flow_id, "connect_error", "Connection error after retries", 502)
            raise HTTPException(502, "Connection error after retries")
        except Exception as e:
            error_msg = str(e)
            status_code = 500
            # 检查是否为可重试的网络错误
            if is_retryable_error(None, e) and retry < max_retries:
                print(f"[OpenAI] 网络错误，重试 {retry + 1}/{max_retries}: {type(e).__name__}")
                await asyncio.sleep(0.5 * (2 ** retry))
                continue
            if flow_id:
                flow_monitor.fail_flow(flow_id, "internal_error", str(e), 500)
            raise HTTPException(500, str(e))
    
    # 记录日志
    duration = (time.time() - start_time) * 1000
    state.add_log(RequestLog(
        id=log_id,
        timestamp=time.time(),
        method="POST",
        path="/v1/chat/completions",
        model=model,
        account_id=current_account.id if current_account else None,
        status=status_code,
        duration_ms=duration,
        error=error_msg
    ))
    
    # 记录统计
    stats_manager.record_request(
        account_id=current_account.id if current_account else "unknown",
        model=model,
        success=status_code == 200,
        latency_ms=duration
    )
    
    msg_id = f"chatcmpl-{log_id}"
    
    if stream:
        return _stream_openai_response(result, model, msg_id, flow_id, full_content="".join(result.get("content", [])))
    
    # 非流式：直接用 convert_kiro_response_to_openai
    response = convert_kiro_response_to_openai(result, model, msg_id)
    
    # 完成 Flow
    if flow_id:
        full_content = "".join(result.get("content", []))
        flow_monitor.complete_flow(
            flow_id,
            status_code=200,
            content=full_content,
            tool_calls=result.get("tool_uses", []),
            stop_reason=result.get("stop_reason", "stop"),
            usage=TokenUsage(
                input_tokens=result.get("input_tokens", 0),
                output_tokens=result.get("output_tokens", 0),
            ),
        )
    
    return response


def _stream_openai_response(result: dict, model: str, msg_id: str, flow_id: str = None, full_content: str = ""):
    """将 Kiro 完整响应转为 OpenAI SSE 流式格式
    
    按照 OpenAI streaming 规范:
    - 文本内容通过 delta.content 逐块发送
    - 工具调用通过 delta.tool_calls 发送（先发 name+id，再发 arguments）
    - finish_reason 在最后一个 chunk 中设置
    """
    tool_uses = result.get("tool_uses", [])
    stop_reason = result.get("stop_reason", "stop")
    
    # 映射 finish_reason
    if tool_uses:
        finish_reason = "tool_calls"
    elif stop_reason == "max_tokens":
        finish_reason = "length"
    else:
        finish_reason = "stop"
    
    async def generate():
        created = int(time.time())
        
        # 流式发送文本内容
        text = "".join(result.get("content", []))
        if text:
            # 逐块发送文本，每块 80 字符（比原来 20 大，减少 chunk 数量）
            chunk_size = 80
            for i in range(0, len(text), chunk_size):
                chunk_text = text[i:i + chunk_size]
                data = {
                    "id": msg_id,
                    "object": "chat.completion.chunk",
                    "created": created,
                    "model": model,
                    "choices": [{
                        "index": 0,
                        "delta": {"content": chunk_text},
                        "finish_reason": None
                    }]
                }
                yield f"data: {json.dumps(data)}\n\n"
                await asyncio.sleep(0.01)
        
        # 流式发送工具调用（OpenAI streaming tool call 格式）
        for idx, tool_use in enumerate(tool_uses):
            tool_call_id = tool_use.get("id", "")
            if not tool_call_id:
                tool_call_id = f"call_{uuid.uuid4().hex[:24]}"
            
            func_name = tool_use.get("name", "")
            func_args = json.dumps(tool_use.get("input", {}))
            
            # 第一个 chunk: 发送 tool_call 的 id, type, name (arguments 为空)
            data = {
                "id": msg_id,
                "object": "chat.completion.chunk",
                "created": created,
                "model": model,
                "choices": [{
                    "index": 0,
                    "delta": {
                        "tool_calls": [{
                            "index": idx,
                            "id": tool_call_id,
                            "type": "function",
                            "function": {
                                "name": func_name,
                                "arguments": ""
                            }
                        }]
                    },
                    "finish_reason": None
                }]
            }
            yield f"data: {json.dumps(data)}\n\n"
            await asyncio.sleep(0.01)
            
            # 后续 chunks: 分块发送 arguments
            arg_chunk_size = 200
            for j in range(0, max(len(func_args), 1), arg_chunk_size):
                arg_chunk = func_args[j:j + arg_chunk_size]
                if not arg_chunk:
                    break
                data = {
                    "id": msg_id,
                    "object": "chat.completion.chunk",
                    "created": created,
                    "model": model,
                    "choices": [{
                        "index": 0,
                        "delta": {
                            "tool_calls": [{
                                "index": idx,
                                "function": {
                                    "arguments": arg_chunk
                                }
                            }]
                        },
                        "finish_reason": None
                    }]
                }
                yield f"data: {json.dumps(data)}\n\n"
                await asyncio.sleep(0.01)
        
        # 最终 chunk: finish_reason
        end_data = {
            "id": msg_id,
            "object": "chat.completion.chunk",
            "created": created,
            "model": model,
            "choices": [{
                "index": 0,
                "delta": {},
                "finish_reason": finish_reason
            }]
        }
        yield f"data: {json.dumps(end_data)}\n\n"
        yield "data: [DONE]\n\n"
        
        # 完成 Flow
        if flow_id:
            flow_monitor.complete_flow(
                flow_id,
                status_code=200,
                content=full_content,
                tool_calls=tool_uses,
                stop_reason=stop_reason,
                usage=TokenUsage(
                    input_tokens=result.get("input_tokens", 0),
                    output_tokens=result.get("output_tokens", 0),
                ),
            )
    
    return StreamingResponse(generate(), media_type="text/event-stream")

"""Gemini 协议处理 - /v1/models/{model}:generateContent"""
import json
import uuid
import time
import hashlib
import httpx
from fastapi import Request, HTTPException

from ..config import KIRO_API_URL, map_model_name
from ..core import state
from ..core.state import RequestLog
from ..kiro_api import build_headers, build_kiro_request, parse_event_stream
from ..converters import convert_gemini_contents_to_kiro


async def handle_generate_content(model_name: str, request: Request):
    """处理 Gemini generateContent 请求"""
    start_time = time.time()
    log_id = uuid.uuid4().hex[:8]
    
    body = await request.json()
    contents = body.get("contents", [])
    system_instruction = body.get("systemInstruction", {})
    
    model_raw = model_name.replace("models/", "")
    model = map_model_name(model_raw)
    
    session_id = hashlib.sha256(json.dumps(contents[:3], sort_keys=True).encode()).hexdigest()[:16]
    account = state.get_available_account(session_id)
    
    if not account:
        raise HTTPException(503, "All accounts are rate limited")
    
    token = account.get_token()
    if not token:
        raise HTTPException(500, f"Failed to get token for account {account.name}")
    
    user_content, history = convert_gemini_contents_to_kiro(contents, system_instruction, model)
    kiro_request = build_kiro_request(user_content, model, history)
    headers = build_headers(token)
    
    error_msg = None
    status_code = 200
    content = ""
    
    try:
        async with httpx.AsyncClient(verify=False, timeout=120) as client:
            resp = await client.post(KIRO_API_URL, json=kiro_request, headers=headers)
            status_code = resp.status_code
            
            if resp.status_code == 429:
                state.mark_rate_limited(account.id, 60)
                new_account = state.get_available_account()
                if new_account and new_account.id != account.id:
                    token = new_account.get_token()
                    headers = build_headers(token)
                    resp = await client.post(KIRO_API_URL, json=kiro_request, headers=headers)
                    status_code = resp.status_code
                    account = new_account
                else:
                    raise HTTPException(429, "Rate limited")
            
            if resp.status_code != 200:
                error_msg = resp.text
                raise HTTPException(resp.status_code, resp.text)
            
            content = parse_event_stream(resp.content)
            account.request_count += 1
            account.last_used = time.time()
            
    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)
        status_code = 500
        raise HTTPException(500, str(e))
    finally:
        duration = (time.time() - start_time) * 1000
        state.add_log(RequestLog(
            id=log_id,
            timestamp=time.time(),
            method="POST",
            path=f"/v1/models/{model_name}:generateContent",
            model=model,
            account_id=account.id if account else None,
            status=status_code,
            duration_ms=duration,
            error=error_msg
        ))
    
    return {
        "candidates": [{
            "content": {
                "parts": [{"text": content}],
                "role": "model"
            },
            "finishReason": "STOP",
            "index": 0
        }],
        "usageMetadata": {
            "promptTokenCount": len(user_content) // 4,
            "candidatesTokenCount": len(content) // 4,
            "totalTokenCount": (len(user_content) + len(content)) // 4
        }
    }

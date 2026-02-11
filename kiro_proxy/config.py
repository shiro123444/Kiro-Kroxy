"""配置模块"""
import json
from pathlib import Path

KIRO_API_URL = "https://q.us-east-1.amazonaws.com/generateAssistantResponse"
MODELS_URL = "https://q.us-east-1.amazonaws.com/ListAvailableModels"
TOKEN_PATH = Path.home() / ".aws/sso/cache/kiro-auth-token.json"

# 配额管理配置
QUOTA_COOLDOWN_SECONDS = 300  # 配额超限冷却时间（秒）

# 模型映射
MODEL_MAPPING = {
    # Claude 3.5 -> Kiro Claude 4
    "claude-3-5-sonnet-20241022": "claude-sonnet-4",
    "claude-3-5-sonnet-latest": "claude-sonnet-4",
    "claude-3-5-sonnet": "claude-sonnet-4",
    "claude-3-5-haiku-20241022": "claude-haiku-4.5",
    "claude-3-5-haiku-latest": "claude-haiku-4.5",
    # Claude 3
    "claude-3-opus-20240229": "claude-opus-4.5",
    "claude-3-opus-latest": "claude-opus-4.5",
    "claude-3-sonnet-20240229": "claude-sonnet-4",
    "claude-3-haiku-20240307": "claude-haiku-4.5",
    # Claude 4
    "claude-4-sonnet": "claude-sonnet-4",
    "claude-4-opus": "claude-opus-4.5",
    # OpenAI GPT -> Claude
    "gpt-4o": "claude-sonnet-4",
    "gpt-4o-mini": "claude-haiku-4.5",
    "gpt-4-turbo": "claude-sonnet-4",
    "gpt-4": "claude-sonnet-4",
    "gpt-3.5-turbo": "claude-haiku-4.5",
    # OpenAI o1 -> Claude Opus
    "o1": "claude-opus-4.5",
    "o1-preview": "claude-opus-4.5",
    "o1-mini": "claude-sonnet-4",
    # Gemini -> Claude
    "gemini-2.0-flash": "claude-sonnet-4",
    "gemini-2.0-flash-thinking": "claude-opus-4.5",
    "gemini-1.5-pro": "claude-sonnet-4.5",
    "gemini-1.5-flash": "claude-sonnet-4",
    # 别名
    "sonnet": "claude-sonnet-4",
    "haiku": "claude-haiku-4.5",
    "opus": "claude-opus-4.5",
}

# 内置 Kiro 模型
BUILTIN_KIRO_MODELS = {"auto", "claude-sonnet-4.5", "claude-sonnet-4", "claude-haiku-4.5", "claude-opus-4.5", "claude-opus-4.6"}

# 运行时自定义模型（从配置加载）
_custom_models = {}  # {model_id: {"name": "...", "description": "..."}}

def _load_custom_models():
    """从配置文件加载自定义模型"""
    global _custom_models
    try:
        from .core.persistence import load_config
        config = load_config()
        _custom_models = config.get("custom_models", {})
    except Exception:
        pass

def get_all_kiro_models() -> set:
    """获取所有 Kiro 模型 ID（内置 + 自定义）"""
    return BUILTIN_KIRO_MODELS | set(_custom_models.keys())

def get_custom_models() -> dict:
    """获取自定义模型列表"""
    return _custom_models.copy()

def add_custom_model(model_id: str, name: str = "", description: str = "") -> bool:
    """添加自定义模型"""
    global _custom_models
    _custom_models[model_id] = {
        "name": name or model_id,
        "description": description,
    }
    _save_custom_models()
    return True

def remove_custom_model(model_id: str) -> bool:
    """删除自定义模型"""
    global _custom_models
    if model_id in _custom_models:
        del _custom_models[model_id]
        _save_custom_models()
        return True
    return False

def _save_custom_models():
    """保存自定义模型到配置文件"""
    try:
        from .core.persistence import load_config, save_config
        config = load_config()
        config["custom_models"] = _custom_models
        save_config(config)
    except Exception as e:
        print(f"[Config] 保存自定义模型失败: {e}")

# 兼容旧代码
KIRO_MODELS = BUILTIN_KIRO_MODELS

def map_model_name(model: str) -> str:
    """将外部模型名称映射到 Kiro 支持的名称"""
    if not model:
        return "claude-sonnet-4"
    if model in MODEL_MAPPING:
        return MODEL_MAPPING[model]
    all_models = get_all_kiro_models()
    if model in all_models:
        return model
    model_lower = model.lower()
    if "opus" in model_lower:
        # 检查版本号
        if "4.6" in model_lower:
            return "claude-opus-4.6"
        return "claude-opus-4.5"
    if "haiku" in model_lower:
        return "claude-haiku-4.5"
    if "sonnet" in model_lower:
        return "claude-sonnet-4.5" if "4.5" in model_lower else "claude-sonnet-4"
    return "claude-sonnet-4"

from typing import Dict, List, Optional

from exam_funcall_simple.function_caller.infra import GPT_MODEL_NAME

def prepare_messages(
        user_message: str,
        system_message: Optional[str],
        history: Optional[List[Dict[str, str]]]
) -> List[Dict[str, str]]:
    """准备消息列表
    Args:
        user_message: 用户消息
        system_message: 系统消息
        history: 历史消息
    Returns:
        messages: 准备好的消息列表
    """
    messages = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_message})
    return messages

def prepare_request_data(
        messages: List[Dict[str, str]],
        functions: List[Dict],
        force_function_call: bool,
        user_message: str
) -> Dict:
    """准备请求数据
    Args:
        messages: 消息列表
        functions: 函数描述列表
        force_function_call: 是否强制使用函数调用
        user_message: 用户消息
    Returns:
        request_data: 准备好的请求数据
    """
    request_data = {
        "model": GPT_MODEL_NAME,
        "messages": messages,
    }
    
    if functions and (force_function_call or "function" in user_message.lower()):
        request_data.update({
            "tools": [{"type": "function", "function": f} for f in functions],
            "tool_choice": "auto"
        })
    return request_data

def format_function_call(function_call) -> str:
    """格式化函数调用信息
    Args:
        function_call: 函数调用信息
    Returns:
        str: 格式化后的字符串
    """
    if not function_call:
        return "No function call"
    return (
        f"Function: {function_call.name}\n"
        f"Arguments: {function_call.arguments}"
    ) 
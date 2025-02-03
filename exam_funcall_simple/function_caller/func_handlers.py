import json
from typing import Dict, List, Any

from exam_funcall_simple.function_caller.infra import LogType, log_debug
from exam_funcall_simple.function_caller.func_utils import format_function_call

def execute_function(
        func_name: str,
        func_args: Dict,
        available_functions: Dict[str, callable],
        logger: Any
) -> Any:
    """执行函数调用
    Args:
        func_name: 函数名
        func_args: 函数参数
        available_functions: 可用函数映射
        logger: 日志器
    Returns:
        function_response: 函数执行结果
    Raises:
        ValueError: 函数未找到
        Exception: 函数执行失败
    """
    if func_name not in available_functions:
        error_msg = f"未找到函数: {func_name}"
        log_debug(logger, LogType.ERROR, error_msg)
        raise ValueError(error_msg)
        
    try:
        function_response = available_functions[func_name](**func_args)
        log_debug(logger, LogType.FUNCTION_RESULT, str(function_response))
        return function_response
    except Exception as e:
        log_debug(logger, LogType.ERROR, f"函数执行失败: {str(e)}")
        raise

def handle_conversation_tool_call(
        tool_call: Any,
        messages: List[Dict],
        available_functions: Dict[str, callable],
        logger: Any
) -> None:
    """处理会话中的单个工具调用，并将结果添加到消息历史
    Args:
        tool_call: 工具调用信息
        messages: 消息历史列表
        available_functions: 可用函数映射
        logger: 日志器
    """
    if tool_call.type == "function":
        log_debug(logger, LogType.FUNCTION_CALL, format_function_call(tool_call.function))
        
        func_name = tool_call.function.name
        func_args = json.loads(tool_call.function.arguments)
        function_response = execute_function(func_name, func_args, available_functions, logger)
        
        # 将函数调用结果添加到消息历史
        messages.append({
            "role": "assistant",
            "content": None,
            "tool_calls": [tool_call]
        })
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": func_name,
            "content": str(function_response)
        }) 
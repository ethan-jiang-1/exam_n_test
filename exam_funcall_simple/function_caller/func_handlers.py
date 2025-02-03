import json
from typing import Dict, List, Any
from exam_funcall_simple.function_caller.infra import logger

def execute_function(
        func_name: str,
        func_args: Dict,
        available_functions: Dict[str, callable],
        custom_logger: Any = None
) -> Any:
    """执行函数调用
    Args:
        func_name: 函数名
        func_args: 函数参数
        available_functions: 可用函数映射
        custom_logger: 自定义日志器（可选）
    Returns:
        function_response: 函数执行结果
    Raises:
        ValueError: 函数未找到
        Exception: 函数执行失败
    """
    log = custom_logger or logger
    
    if func_name not in available_functions:
        error_msg = f"未找到函数: {func_name}"
        log.error(error_msg)
        raise ValueError(error_msg)
        
    try:
        # 获取函数并执行
        func = available_functions[func_name]
        # 解包参数字典
        if func_args:
            function_response = func(**func_args)
        else:
            function_response = func()
        log.function_result(str(function_response))
        return function_response
    except Exception as e:
        log.error(f"函数执行失败: {str(e)}")
        raise

def handle_conversation_tool_call(
        tool_call: Any,
        messages: List[Dict],
        available_functions: Dict[str, callable],
        custom_logger: Any = None
) -> None:
    """处理会话中的单个工具调用，并将结果添加到消息历史
    Args:
        tool_call: 工具调用信息
        messages: 消息历史列表
        available_functions: 可用函数映射
        custom_logger: 自定义日志器（可选）
    """
    log = custom_logger or logger
    
    if tool_call.type == "function":
        log.function_call(tool_call.function.name, tool_call.function.arguments)
        
        func_name = tool_call.function.name
        func_args = json.loads(tool_call.function.arguments)
        function_response = execute_function(func_name, func_args, available_functions, log)
        
        # 将函数调用结果添加到消息历史
        messages.append({
            "role": "assistant",
            "content": "",
            "tool_calls": [tool_call]
        })
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": func_name,
            "content": str(function_response)
        })
        # 添加一个空的assistant消息，允许模型继续对话
        messages.append({
            "role": "assistant",
            "content": "",
            "tool_calls": None
        }) 
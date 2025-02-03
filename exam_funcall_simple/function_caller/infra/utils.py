"""测试辅助函数"""
from typing import Any, Dict, List  # , Optional
#from .logger import LogType, log_debug

def print_test_header(test_name: str):
    """打印测试标题"""
    print(f"\n{'='*80}\n{test_name}\n{'='*80}\n")

def print_user_input(message: str):
    """打印用户输入"""
    print(f"\n--- 用户输入 ---\n{message}\n")

def print_system_message(message: str):
    """打印系统消息"""
    print(f"\n--- 系统消息 ---\n{message}\n")

def print_request_data(data: Dict):
    """打印请求数据"""
    print(f"\n--- 请求数据 ---\n{data}\n")

def print_api_response(response: Any):
    """打印API响应"""
    print(f"\n--- API响应 ---\n{response}\n")

def print_function_result(result: Any):
    """打印函数执行结果"""
    print(f"\n--- 函数执行结果 ---\n{result}\n")

def print_execution_time(time: float):
    """打印执行时间"""
    print(f"\n--- 执行时间 ---\n{time:.2f} 秒\n")

def print_conversation_history(history: List[Dict[str, str]]):
    """打印对话历史"""
    print("\n--- 对话历史 ---")
    for msg in history:
        role = msg["role"].upper()
        content = msg["content"]
        print(f"\n{role}: {content}")
    print()

def log_function_call(func_name: str, *args, **kwargs):
    """函数调用装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"\n[调用函数] {func_name}")
            print(f"参数: {args}, {kwargs}")
            result = func(*args, **kwargs)
            print(f"返回值: {result}\n")
            return result
        return wrapper
    return decorator

class TestLogger:
    """测试日志器"""
    def __init__(self):
        self.logs = []
    
    def log(self, level: int, message: str):
        """记录日志"""
        self.logs.append((level, message))
    
    def get_logs(self) -> List[tuple]:
        """获取所有日志"""
        return self.logs 
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.syntax import Syntax
import json
from typing import Any, Dict, Optional, List, Callable
import colorlog
import logging
import functools
#from datetime import datetime

class TestLogger:
    def __init__(self):
        self.console = Console()
        
    def print_title(self, title: str):
        """打印测试标题"""
        self.console.print()
        self.console.rule(f"[bold cyan]{title}[/]", style="cyan")
        self.console.print()
        
    def print_step(self, step: str):
        """打印测试步骤"""
        text = Text(">>> ", style="yellow") + Text(step, style="yellow bold")
        self.console.print(text)
        self.console.print()
        
    def print_gpt_request(self, user_input: str, request_data: Dict):
        """打印GPT请求信息"""
        # 用户输入
        self.print_panel("用户输入", user_input, "blue")
        
        # 请求数据
        formatted_json = json.dumps(request_data, indent=2, ensure_ascii=False)
        self.print_panel("请求数据", formatted_json, "cyan", syntax="json")
        
    def print_gpt_response(self, response_data: Dict, function_result: Optional[Any] = None):
        """打印GPT响应信息"""
        # API响应
        formatted_json = json.dumps(response_data, indent=2, ensure_ascii=False)
        self.print_panel("API响应", formatted_json, "yellow", syntax="json")
        
        # 如果有函数调用结果
        if function_result is not None:
            if isinstance(function_result, (dict, list)):
                result_str = json.dumps(function_result, indent=2, ensure_ascii=False)
            else:
                result_str = str(function_result)
            self.print_panel("函数执行结果", result_str, "green", syntax="json")
            
    def print_panel(self, title: str, content: str, color: str, syntax: Optional[str] = None):
        """打印带颜色的面板"""
        if syntax:
            content = Syntax(content, syntax, theme="monokai", line_numbers=True)
            
        panel = Panel(
            content,
            title=f"[bold {color}]{title}[/]",
            border_style=color
        )
        self.console.print(panel)
        self.console.print()
        
    def print_table(self, title: str, data: Dict[str, Any]):
        """打印表格形式的数据"""
        table = Table(title=title, show_header=True, header_style="bold magenta")
        table.add_column("Key", style="cyan")
        table.add_column("Value", style="green")
        
        for key, value in data.items():
            table.add_row(str(key), str(value))
            
        self.console.print(table)
        self.console.print()
        
    def print_error(self, error: str):
        """打印错误信息"""
        self.print_panel("Error", error, "red")
        
    def print_success(self, message: str):
        """打印成功信息"""
        text = Text("✓ ", style="green") + Text(message, style="green bold")
        self.console.print(text)
        self.console.print()
        
    def print_separator(self):
        """打印分隔线"""
        self.console.rule(style="blue")
        
    def print_timing(self, seconds: float):
        """打印执行时间"""
        self.print_panel("执行耗时", f"{seconds:.2f} 秒", "cyan")

# 创建一个全局的TestLogger实例
_logger = TestLogger()

def setup_function_logger() -> colorlog.Logger:
    """设置函数调用的彩色日志"""
    logger = colorlog.getLogger('function_logger')
    if not logger.handlers:
        handler = colorlog.StreamHandler()
        handler.setFormatter(colorlog.ColoredFormatter(
            '%(log_color)s[%(asctime)s] %(message)s%(reset)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        ))
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    return logger

# 全局logger实例
function_logger = setup_function_logger()

def log_function_call(func: Callable) -> Callable:
    """记录函数调用的装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 记录函数调用
        func_name = func.__name__
        params = {
            "args": args,
            "kwargs": kwargs
        }
        function_logger.info("┌──────────── 函数调用 ────────────")
        function_logger.info(f"│ 函数名称: {func_name}")
        function_logger.info(f"│ 调用参数: {json.dumps(params, ensure_ascii=False)}")
        
        try:
            # 执行函数
            result = func(*args, **kwargs)
            # 记录返回值
            function_logger.info(f"│ 返回结果: {result}")
            function_logger.info("└─────────────────────────────")
            return result
        except Exception as e:
            function_logger.error(f"│ 执行错误: {str(e)}")
            function_logger.error("└─────────────────────────────")
            raise
    return wrapper

def print_test_header(title: str):
    """打印测试标题"""
    _logger.print_title(title)

def print_user_input(user_input: str):
    """打印用户输入"""
    _logger.print_panel("用户输入", user_input, "blue")

def print_system_message(system_message: str):
    """打印系统消息"""
    _logger.print_panel("系统消息", system_message, "magenta")

def print_conversation_history(history: List[Dict[str, str]]):
    """打印对话历史"""
    formatted_json = json.dumps(history, indent=2, ensure_ascii=False)
    _logger.print_panel("对话历史", formatted_json, "yellow", syntax="json")

def _serialize_object(obj):
    """序列化对象，处理不可直接序列化的特殊对象"""
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    elif hasattr(obj, "__dict__"):
        return obj.__dict__
    return str(obj)

def print_request_data(request_data):
    """打印请求数据"""
    try:
        # 递归处理不可序列化的对象
        def process_dict(d):
            if isinstance(d, dict):
                return {k: process_dict(v) for k, v in d.items()}
            elif isinstance(d, list):
                return [process_dict(item) for item in d]
            else:
                return _serialize_object(d)
        
        serializable_data = process_dict(request_data)
        formatted_json = json.dumps(serializable_data, indent=2, ensure_ascii=False)
        _logger.print_panel("请求数据", formatted_json, "cyan", syntax="json")
    except Exception as e:
        print(f"Error formatting request data: {str(e)}")
        print(request_data)

def print_api_response(response_data):
    """打印API响应"""
    try:
        # 递归处理不可序列化的对象
        def process_dict(d):
            if isinstance(d, dict):
                return {k: process_dict(v) for k, v in d.items()}
            elif isinstance(d, list):
                return [process_dict(item) for item in d]
            else:
                return _serialize_object(d)
        
        serializable_data = process_dict(response_data)
        formatted_json = json.dumps(serializable_data, indent=2, ensure_ascii=False)
        _logger.print_panel("API响应", formatted_json, "yellow", syntax="json")
    except Exception as e:
        print(f"Error formatting response data: {str(e)}")
        print(response_data)

def print_function_result(function_result: Any):
    """打印函数执行结果"""
    if hasattr(function_result, 'name') and hasattr(function_result, 'arguments'):
        # 处理function_call对象
        try:
            args_dict = json.loads(function_result.arguments)
            result_str = json.dumps({
                "函数名称": function_result.name,
                "函数参数": args_dict
            }, indent=2, ensure_ascii=False)
        except json.JSONDecodeError:
            result_str = json.dumps({
                "函数名称": function_result.name,
                "函数参数": function_result.arguments
            }, indent=2, ensure_ascii=False)
    elif isinstance(function_result, (dict, list)):
        result_str = json.dumps(function_result, indent=2, ensure_ascii=False)
    else:
        result_str = str(function_result)
    
    _logger.print_panel("函数执行结果", result_str, "green", syntax="json")
    
    # 如果是字典类型，还要打印表格形式
    if isinstance(function_result, dict):
        _logger.print_table("转换结果", function_result)

def print_execution_time(seconds: float):
    """打印执行时间"""
    _logger.print_timing(seconds) 
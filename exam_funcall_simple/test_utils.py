from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.syntax import Syntax
import json
from typing import Any, Dict, Optional, List

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

def print_request_data(request_data: Dict):
    """打印请求数据"""
    formatted_json = json.dumps(request_data, indent=2, ensure_ascii=False)
    _logger.print_panel("请求数据", formatted_json, "cyan", syntax="json")

def print_api_response(response_data: Dict):
    """打印API响应"""
    formatted_json = json.dumps(response_data, indent=2, ensure_ascii=False)
    _logger.print_panel("API响应", formatted_json, "yellow", syntax="json")

def print_function_result(function_result: Any):
    """打印函数执行结果"""
    if isinstance(function_result, (dict, list)):
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
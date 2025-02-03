import logging
import colorlog
from enum import Enum
from typing import Any, Dict, List
from functools import wraps

class LogLevel(Enum):
    """自定义日志级别，避免与标准日志级别混淆"""
    TEST = 100
    USER = 101
    SYSTEM = 102
    REQUEST = 103
    RESPONSE = 104
    FUNCTION = 105
    RESULT = 106
    TIMING = 107
    ERROR = 108

class LogType(Enum):
    """日志类型枚举，定义不同类型日志的级别和颜色"""
    TEST_HEADER = (LogLevel.TEST, 'bold_white', '测试')
    USER_INPUT = (LogLevel.USER, 'cyan', '用户输入')
    SYSTEM_MESSAGE = (LogLevel.SYSTEM, 'blue', '系统消息')
    REQUEST = (LogLevel.REQUEST, 'green', '请求数据')
    RESPONSE = (LogLevel.RESPONSE, 'yellow', '原始响应')
    FUNCTION_CALL = (LogLevel.FUNCTION, 'magenta', '函数调用')
    FUNCTION_RESULT = (LogLevel.RESULT, 'bold_green', '执行结果')
    TIMING = (LogLevel.TIMING, 'white', '执行耗时')
    ERROR = (LogLevel.ERROR, 'bold_red', '错误')

    def __init__(self, level, color, title):
        self.level = level.value
        self.color = color
        self.title = title

class Logger:
    """统一的日志管理类"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance
    
    def _init(self):
        """初始化日志器"""
        self.logger = colorlog.getLogger('gpt_caller')
        if not self.logger.handlers:
            # 注册自定义日志级别
            for level in LogLevel:
                logging.addLevelName(level.value, level.name)
            
            # 配置处理器
            handler = colorlog.StreamHandler()
            handler.setFormatter(colorlog.ColoredFormatter(
                '%(log_color)s%(message)s%(reset)s',
                log_colors={name: log_type.color for name, log_type in LogType.__members__.items()}
            ))
            self.logger.addHandler(handler)
            self.logger.setLevel(min(level.value for level in LogLevel))
    
    def _format_content(self, content: Any) -> str:
        """格式化日志内容"""
        if isinstance(content, (dict, list)):
            import json
            return json.dumps(content, indent=2, ensure_ascii=False)
        return str(content)
    
    def _log(self, log_type: LogType, content: Any):
        """输出带格式的日志"""
        self.logger.log(log_type.level, f"\n{'='*80}")
        self.logger.log(log_type.level, f"{log_type.title}")
        self.logger.log(log_type.level, f"{'='*80}\n")
        self.logger.log(log_type.level, self._format_content(content))
        self.logger.log(log_type.level, f"\n{'='*80}\n")
    
    # 日志输出方法
    def test_header(self, name: str):
        """输出测试标题"""
        self._log(LogType.TEST_HEADER, name)
    
    def user_input(self, message: str):
        """输出用户输入"""
        self._log(LogType.USER_INPUT, message)
    
    def system_message(self, message: str):
        """输出系统消息"""
        self._log(LogType.SYSTEM_MESSAGE, message)
    
    def request_data(self, data: Dict):
        """输出请求数据"""
        self._log(LogType.REQUEST, data)
    
    def api_response(self, response: Any):
        """输出API响应"""
        self._log(LogType.RESPONSE, response)
    
    def function_call(self, name: str, *args, **kwargs):
        """输出函数调用信息"""
        self._log(LogType.FUNCTION_CALL, {
            'name': name,
            'args': args,
            'kwargs': kwargs
        })
    
    def function_result(self, result: Any):
        """输出函数执行结果"""
        self._log(LogType.FUNCTION_RESULT, result)
    
    def execution_time(self, time: float):
        """输出执行时间"""
        self._log(LogType.TIMING, f"{time:.2f} 秒")
    
    def conversation_history(self, history: List[Dict[str, str]]):
        """输出对话历史"""
        formatted = []
        for msg in history:
            formatted.append(f"{msg['role'].upper()}: {msg['content']}")
        self._log(LogType.SYSTEM_MESSAGE, "\n".join(formatted))
    
    def error(self, message: str):
        """输出错误信息"""
        self._log(LogType.ERROR, message)
    
    def function_logger(self, func_name: str):
        """函数调用日志装饰器
        用法:
        @logger.function_logger("函数名")
        def some_function(*args, **kwargs):
            pass
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                self.function_call(func_name, *args, **kwargs)
                result = func(*args, **kwargs)
                self.function_result(result)
                return result
            return wrapper
        return decorator

# 全局日志器实例
logger = Logger()

# 为了保持向后兼容，保留原有的函数名
print_test_header = logger.test_header
print_user_input = logger.user_input
print_system_message = logger.system_message
print_request_data = logger.request_data
print_api_response = logger.api_response
print_function_result = logger.function_result
print_execution_time = logger.execution_time
print_conversation_history = logger.conversation_history
log_function_call = logger.function_logger 
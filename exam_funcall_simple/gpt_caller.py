from openai import AzureOpenAI
import json
import time
import colorlog
import logging
from enum import Enum

from exam_funcall_simple import config
from exam_funcall_simple import func_simple

class LogType(Enum):
    """日志类型枚举，定义不同类型日志的级别和颜色"""
    USER_INPUT = (logging.DEBUG, 'blue', '用户输入')          # 蓝色
    REQUEST = (logging.INFO, 'green', '请求数据')            # 绿色
    RESPONSE = (logging.WARNING, 'yellow', '原始响应')       # 黄色
    FUNCTION_CALL = (logging.ERROR, 'red', '函数调用信息')   # 红色
    FUNCTION_RESULT = (logging.CRITICAL, 'red,bg_white', '函数执行结果')  # 红底白字
    ERROR = (logging.ERROR, 'red', '错误信息')              # 红色
    TIMING = (logging.INFO, 'green', '执行耗时')            # 绿色

    def __init__(self, level, color, title):
        self.level = level
        self.color = color
        self.title = title

class GPTFunctionCaller:
    def __init__(self, debug=True):
        """
        初始化GPT函数调用器
        Args:
            debug (bool): 是否启用调试模式，显示详细日志
        """
        self.client = AzureOpenAI(
            api_key=config.AZURE_OPENAI_API_KEY,
            api_version=config.AZURE_OPENAI_VERSION,
            azure_endpoint=config.AZURE_OPENAI_ENDPOINT
        )
        
        self.available_functions = {
            "get_current_time": func_simple.get_current_time,
            "calculate_circle_area": func_simple.calculate_circle_area
        }
        self.debug = debug
        self.logger = self._setup_logger() if debug else None
        
    def _setup_logger(self):
        """设置彩色日志"""
        logger = colorlog.getLogger('gpt_caller')
        if not logger.handlers:
            handler = colorlog.StreamHandler()
            handler.setFormatter(colorlog.ColoredFormatter(
                '%(log_color)s%(message)s%(reset)s',
                log_colors={
                    'DEBUG': LogType.USER_INPUT.color,
                    'INFO': LogType.REQUEST.color,
                    'WARNING': LogType.RESPONSE.color,
                    'ERROR': LogType.FUNCTION_CALL.color,
                    'CRITICAL': LogType.FUNCTION_RESULT.color,
                }
            ))
            logger.addHandler(handler)
            logger.setLevel(logging.DEBUG)
        return logger
                
    def _log_debug(self, log_type: LogType, content: any):
        """输出调试信息，使用彩色输出"""
        if not self.debug:
            return
            
        # 输出带颜色的标题
        self.logger.log(log_type.level, f"\n=== {log_type.title} ===")
        
        # 输出内容
        if isinstance(content, str):
            self.logger.log(log_type.level, content)
        else:
            self.logger.log(
                log_type.level,
                json.dumps(content, indent=2, ensure_ascii=False)
            )
                
    def _format_function_call(self, function_call) -> str:
        """格式化函数调用信息"""
        if not function_call:
            return "No function call"
        return (
            f"Function: {function_call.name}\n"
            f"Arguments: {function_call.arguments}"
        )

    def call_with_functions(self, user_message: str):
        """
        使用function calling功能调用GPT
        Args:
            user_message (str): 用户输入的消息
        Returns:
            response: GPT的响应
        """
        start_time = time.time()
        self._log_debug(LogType.USER_INPUT, user_message)
        
        # 准备请求
        messages = [{"role": "user", "content": user_message}]
        request_data = {
            "model": config.GPT4_DEPLOYMENT_NAME,
            "messages": messages,
            "functions": func_simple.FUNCTION_DESCRIPTIONS,
            "function_call": "auto"
        }
        self._log_debug(LogType.REQUEST, request_data)
        
        # 发送请求
        try:
            response = self.client.chat.completions.create(**request_data)
            
            # 记录响应
            response_data = response.model_dump()
            self._log_debug(LogType.RESPONSE, response_data)
            
            # 提取并记录函数调用信息
            if response.choices and response.choices[0].message.function_call:
                self._log_debug(
                    LogType.FUNCTION_CALL,
                    self._format_function_call(response.choices[0].message.function_call)
                )
                
                # 执行函数调用
                func_name = response.choices[0].message.function_call.name
                func_args = json.loads(response.choices[0].message.function_call.arguments)
                
                if func_name in self.available_functions:
                    function_response = self.available_functions[func_name](**func_args)
                    self._log_debug(LogType.FUNCTION_RESULT, str(function_response))
            
            # 记录完整耗时
            elapsed_time = time.time() - start_time
            self._log_debug(LogType.TIMING, f"{elapsed_time:.2f} 秒")
            
            return response
            
        except Exception as e:
            self._log_debug(LogType.ERROR, str(e))
            raise

if __name__ == "__main__":
    # 测试不同场景
    caller = GPTFunctionCaller(debug=True)
    
    print("\n=== 测试时间查询 ===")
    response = caller.call_with_functions("现在几点了？")
    
    print("\n=== 测试圆面积计算 ===")
    response = caller.call_with_functions("计算半径为3.5的圆的面积")
    
    print("\n=== 测试普通对话 ===")
    response = caller.call_with_functions("你好，请介绍一下你自己") 
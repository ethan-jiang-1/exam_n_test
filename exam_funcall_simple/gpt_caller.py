from openai import AzureOpenAI
import json
import time
import colorlog
import logging
from enum import Enum
from typing import Dict, List, Any, Optional

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
    def __init__(
            self,
            functions: List[Dict],
            function_map: Dict[str, callable],
            debug: bool = True
    ):
        """
        初始化GPT函数调用器
        Args:
            functions: Function descriptions 列表
            function_map: 函数名到实际函数的映射
            debug: 是否启用调试模式
        """
        self.client = AzureOpenAI(
            api_key=config.AZURE_OPENAI_API_KEY,
            api_version=config.AZURE_OPENAI_VERSION,
            azure_endpoint=config.AZURE_OPENAI_ENDPOINT
        )
        
        self.functions = functions
        self.available_functions = function_map
        self.debug = debug
        self.logger = self._setup_logger() if debug else None
        
    def _setup_logger(self):
        """设置彩色日志"""
        logger = colorlog.getLogger('gpt_caller')
        if not logger.handlers:
            handler = colorlog.StreamHandler()
            handler.setFormatter(colorlog.ColoredFormatter(
                '%(log_color)s[%(asctime)s] %(message)s%(reset)s',
                datefmt='%Y-%m-%d %H:%M:%S',
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
        self.logger.log(log_type.level, f"\n{'='*50}")
        self.logger.log(log_type.level, f"=== {log_type.title} ===")
        self.logger.log(log_type.level, f"{'='*50}\n")
        
        # 输出内容
        if isinstance(content, str):
            self.logger.log(log_type.level, content)
        else:
            self.logger.log(
                log_type.level,
                json.dumps(content, indent=2, ensure_ascii=False)
            )
        
        # 输出分隔符
        self.logger.log(log_type.level, f"\n{'='*50}\n")
                
    def _format_function_call(self, function_call) -> str:
        """格式化函数调用信息"""
        if not function_call:
            return "No function call"
        return (
            f"Function: {function_call.name}\n"
            f"Arguments: {function_call.arguments}"
        )

    def call_with_functions(
            self,
            user_message: str,
            system_message: Optional[str] = None,
            history: Optional[List[Dict[str, str]]] = None
    ) -> Any:
        """
        使用function calling功能调用GPT
        Args:
            user_message: 用户输入的消息
            system_message: 系统提示消息（可选）
            history: 对话历史（可选）
        Returns:
            response: GPT的响应
        """
        start_time = time.time()
        self._log_debug(LogType.USER_INPUT, user_message)
        
        try:
            # 准备消息
            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            if history:
                messages.extend(history)
            messages.append({"role": "user", "content": user_message})
            
            # 准备请求
            request_data = {
                "model": config.GPT4_DEPLOYMENT_NAME,
                "messages": messages,
                "functions": self.functions,
                "function_call": "auto"
            }
            self._log_debug(LogType.REQUEST, request_data)
            
            # 发送请求
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
                    try:
                        function_response = self.available_functions[func_name](**func_args)
                        self._log_debug(LogType.FUNCTION_RESULT, str(function_response))
                    except Exception as e:
                        self._log_debug(LogType.ERROR, f"函数执行失败: {str(e)}")
                        raise
                else:
                    error_msg = f"未找到函数: {func_name}"
                    self._log_debug(LogType.ERROR, error_msg)
                    raise ValueError(error_msg)
            
            # 记录完整耗时
            elapsed_time = time.time() - start_time
            self._log_debug(LogType.TIMING, f"{elapsed_time:.2f} 秒")
            
            return response
            
        except Exception as e:
            self._log_debug(LogType.ERROR, f"调用失败: {str(e)}")
            raise

if __name__ == "__main__":
    # 创建简单函数调用器用于测试
    caller = GPTFunctionCaller(
        functions=func_simple.FUNCTION_DESCRIPTIONS,
        function_map={
            "get_current_time": func_simple.get_current_time,
            "calculate_circle_area": func_simple.calculate_circle_area
        }
    )
    
    # 测试时间查询
    print("\n=== 测试时间查询 ===")
    caller.call_with_functions("现在几点了？")
    
    # 测试圆面积计算
    print("\n=== 测试圆面积计算 ===")
    caller.call_with_functions("计算半径为3.5的圆的面积")
    
    # 测试普通对话
    print("\n=== 测试普通对话 ===")
    caller.call_with_functions("你好，请介绍一下你自己") 
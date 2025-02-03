from openai import AzureOpenAI
import json
import time
import colorlog
import logging
from enum import Enum
from typing import Dict, List, Any, Optional

from exam_funcall_simple import config
#from exam_funcall_simple import func_simple

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

class GPTBase:
    """GPT调用器基类，提供基础功能"""
    
    def __init__(self, debug: bool = True):
        """初始化基类
        Args:
            debug: 是否启用调试模式
        """
        self.client = AzureOpenAI(
            api_key=config.AZURE_OPENAI_API_KEY,
            api_version=config.AZURE_OPENAI_VERSION,
            azure_endpoint=config.AZURE_OPENAI_ENDPOINT
        )
        
        self.debug = debug
        self.logger = self._setup_logger() if debug else None
        self.last_request = None
        self.raw_response = None
        self.execution_time = 0.0
    
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
    
    def call(
            self,
            user_message: str,
            system_message: Optional[str] = None,
            history: Optional[List[Dict[str, str]]] = None
    ) -> Any:
        """基础调用方法"""
        raise NotImplementedError("Subclasses must implement call method")

class GPTCaller(GPTBase):
    """普通GPT调用器，用于文本对话"""
    
    def call(
            self,
            user_message: str,
            system_message: Optional[str] = None,
            history: Optional[List[Dict[str, str]]] = None
    ) -> Any:
        """执行普通的GPT调用
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
                "messages": messages
            }
            self.last_request = request_data
            self._log_debug(LogType.REQUEST, request_data)
            
            # 发送请求
            response = self.client.chat.completions.create(**request_data)
            
            # 记录响应
            response_data = response.model_dump()
            self.raw_response = response_data
            self._log_debug(LogType.RESPONSE, response_data)
            
            # 记录完整耗时
            elapsed_time = time.time() - start_time
            self.execution_time = elapsed_time
            self._log_debug(LogType.TIMING, f"{elapsed_time:.2f} 秒")
            
            return response
            
        except Exception as e:
            self._log_debug(LogType.ERROR, str(e))
            raise

class GPTFunctionCaller(GPTBase):
    """支持函数调用的GPT调用器"""
    
    def __init__(
            self,
            functions: List[Dict],
            function_map: Dict[str, callable],
            debug: bool = True
    ):
        """初始化函数调用器
        Args:
            functions: Function descriptions 列表
            function_map: 函数名到实际函数的映射
            debug: 是否启用调试模式
        """
        super().__init__(debug)
        self.functions = functions
        self.available_functions = function_map
    
    def _format_function_call(self, function_call) -> str:
        """格式化函数调用信息"""
        if not function_call:
            return "No function call"
        return (
            f"Function: {function_call.name}\n"
            f"Arguments: {function_call.arguments}"
        )

    def call_single_function(
            self,
            user_message: str,
            system_message: Optional[str] = None,
            history: Optional[List[Dict[str, str]]] = None,
            force_function_call: bool = True
    ) -> Any:
        """单次函数调用
        执行一次函数调用并返回结果，不会继续对话。
        适用于简单的单一操作场景。
        
        Args:
            user_message: 用户输入的消息
            system_message: 系统提示消息（可选）
            history: 对话历史（可选）
            force_function_call: 是否强制使用函数调用（默认True）
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
            }
            
            # 只在需要时添加函数调用相关配置
            if self.functions and (force_function_call or "function" in user_message.lower()):
                request_data.update({
                    "tools": [{"type": "function", "function": f} for f in self.functions],
                    "tool_choice": "auto"  # 让模型自动选择函数
                })
            self.last_request = request_data  # 保存请求数据
            self._log_debug(LogType.REQUEST, request_data)
            
            # 发送请求
            response = self.client.chat.completions.create(**request_data)
            
            # 记录响应
            response_data = response.model_dump()
            self.raw_response = response_data  # 保存原始响应
            self._log_debug(LogType.RESPONSE, response_data)
            
            # 提取并记录函数调用信息
            if response.choices and response.choices[0].message:
                message = response.choices[0].message
                function_results = []  # 存储所有函数调用的结果
                
                # 处理tool_calls（新的多函数调用方式）
                if message.tool_calls:
                    for tool_call in message.tool_calls:
                        if tool_call.type == "function":
                            self._log_debug(
                                LogType.FUNCTION_CALL,
                                self._format_function_call(tool_call.function)
                            )
                            
                            # 执行函数调用
                            func_name = tool_call.function.name
                            func_args = json.loads(tool_call.function.arguments)
                            
                            if func_name in self.available_functions:
                                try:
                                    function_response = self.available_functions[func_name](**func_args)
                                    self._log_debug(LogType.FUNCTION_RESULT, str(function_response))
                                    function_results.append({
                                        'name': func_name,
                                        'result': function_response
                                    })
                                except Exception as e:
                                    self._log_debug(LogType.ERROR, f"函数执行失败: {str(e)}")
                                    raise
                            else:
                                error_msg = f"未找到函数: {func_name}"
                                self._log_debug(LogType.ERROR, error_msg)
                                raise ValueError(error_msg)
                
                # 处理单个function_call（旧方式，保持向后兼容）
                elif message.function_call:
                    self._log_debug(
                        LogType.FUNCTION_CALL,
                        self._format_function_call(message.function_call)
                    )
                    
                    # 执行函数调用
                    func_name = message.function_call.name
                    func_args = json.loads(message.function_call.arguments)
                    
                    if func_name in self.available_functions:
                        try:
                            function_response = self.available_functions[func_name](**func_args)
                            self._log_debug(LogType.FUNCTION_RESULT, str(function_response))
                            function_results.append({
                                'name': func_name,
                                'result': function_response
                            })
                        except Exception as e:
                            self._log_debug(LogType.ERROR, f"函数执行失败: {str(e)}")
                            raise
                    else:
                        error_msg = f"未找到函数: {func_name}"
                        self._log_debug(LogType.ERROR, error_msg)
                        raise ValueError(error_msg)
                
                # 将函数执行结果添加到response中
                response.function_results = function_results
            
            # 记录完整耗时
            elapsed_time = time.time() - start_time
            self.execution_time = elapsed_time
            self._log_debug(LogType.TIMING, f"{elapsed_time:.2f} 秒")
            
            return response
            
        except Exception as e:
            self._log_debug(LogType.ERROR, str(e))
            raise

    def call_with_conversation(
            self,
            user_message: str,
            system_message: Optional[str] = None,
            history: Optional[List[Dict[str, str]]] = None
    ) -> Any:
        """交互式函数调用
        支持多轮函数调用，会将函数结果加入对话历史，并生成最终响应。
        适用于需要多个函数协同工作的复杂场景。
        
        Args:
            user_message: 用户输入的消息
            system_message: 系统提示消息（可选）
            history: 对话历史（可选）
        Returns:
            response: GPT的响应，包含所有函数调用结果的总结
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
                "tools": [{"type": "function", "function": f} for f in self.functions],
                "tool_choice": "auto"  # 让模型自动选择是否调用函数
            }
            self.last_request = request_data  # 保存请求数据
            self._log_debug(LogType.REQUEST, request_data)
            
            # 发送请求
            response = self.client.chat.completions.create(**request_data)
            
            # 记录响应
            response_data = response.model_dump()
            self.raw_response = response_data
            self._log_debug(LogType.RESPONSE, response_data)
            
            # 提取并记录函数调用信息
            if response.choices and response.choices[0].message:
                message = response.choices[0].message
                
                # 处理tool_calls（新的多函数调用方式）
                if message.tool_calls:
                    for tool_call in message.tool_calls:
                        if tool_call.type == "function":
                            self._log_debug(
                                LogType.FUNCTION_CALL,
                                self._format_function_call(tool_call.function)
                            )
                            
                            # 执行函数调用
                            func_name = tool_call.function.name
                            func_args = json.loads(tool_call.function.arguments)
                            
                            if func_name in self.available_functions:
                                try:
                                    function_response = self.available_functions[func_name](**func_args)
                                    self._log_debug(LogType.FUNCTION_RESULT, str(function_response))
                                    
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
                                except Exception as e:
                                    self._log_debug(LogType.ERROR, str(e))
                                    raise
                            else:
                                error_msg = f"未找到函数: {func_name}"
                                self._log_debug(LogType.ERROR, error_msg)
                                raise ValueError(error_msg)
                
                # 如果有函数调用结果，再次调用模型生成最终响应
                if len(messages) > 1:  # 确保有新的消息添加
                    final_response = self.client.chat.completions.create(
                        model=config.GPT4_DEPLOYMENT_NAME,
                        messages=messages
                    )
                    response = final_response  # 更新响应
        
            # 记录完整耗时
            elapsed_time = time.time() - start_time
            self.execution_time = elapsed_time
            self._log_debug(LogType.TIMING, f"{elapsed_time:.2f} 秒")
            
            return response
            
        except Exception as e:
            self._log_debug(LogType.ERROR, str(e))
            raise

if __name__ == "__main__":
    # 导入函数
    from exam_funcall_simple.func_simple import get_current_time
    
    # 测试普通对话
    print("\n=== 测试普通对话 ===")
    caller = GPTCaller()
    response = caller.call("你好，请介绍一下你自己")
    if response.choices:
        print("\n回复:", response.choices[0].message.content)
    
    # 测试函数调用
    print("\n=== 测试函数调用 ===")
    function_caller = GPTFunctionCaller(
        functions=[{
            "name": "get_current_time",
            "description": "获取当前的系统时间",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }],
        function_map={"get_current_time": get_current_time}
    )
    response = function_caller.call_single_function("请告诉我现在的时间")
    if response.choices:
        print("\n执行结果:", response.choices[0].message.content or "函数调用成功") 
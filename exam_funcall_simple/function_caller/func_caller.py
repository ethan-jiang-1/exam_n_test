import time
import json
from typing import Dict, List, Any, Optional

from exam_funcall_simple import config
from exam_funcall_simple.core_base_caller import GPTBase
from exam_funcall_simple.infra_logger import LogType
from exam_funcall_simple.function_caller.func_utils import prepare_messages, prepare_request_data, format_function_call
from exam_funcall_simple.function_caller.func_handlers import execute_function, handle_conversation_tool_call

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
            # 准备请求
            messages = prepare_messages(user_message, system_message, history)
            request_data = prepare_request_data(messages, self.functions, force_function_call, user_message)
            self.last_request = request_data
            self._log_debug(LogType.REQUEST, request_data)
            
            # 发送请求
            response = self.client.chat.completions.create(**request_data)
            response_data = response.model_dump()
            self.raw_response = response_data
            self._log_debug(LogType.RESPONSE, response_data)
            
            # 处理函数调用
            if response.choices and response.choices[0].message:
                message = response.choices[0].message
                function_results = []
                
                # 处理tool_calls
                if message.tool_calls:
                    for tool_call in message.tool_calls:
                        if tool_call.type == "function":
                            self._log_debug(
                                LogType.FUNCTION_CALL,
                                format_function_call(tool_call.function)
                            )
                            
                            func_name = tool_call.function.name
                            func_args = json.loads(tool_call.function.arguments)
                            function_response = execute_function(
                                func_name,
                                func_args,
                                self.available_functions,
                                self.logger
                            )
                            
                            function_results.append({
                                'name': func_name,
                                'result': function_response
                            })
                
                response.function_results = function_results
            
            # 记录耗时
            self.execution_time = time.time() - start_time
            self._log_debug(LogType.TIMING, f"{self.execution_time:.2f} 秒")
            
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
            # 准备请求
            messages = prepare_messages(user_message, system_message, history)
            request_data = {
                **prepare_request_data(messages, self.functions, True, user_message),
                "tool_choice": "auto"  # 让模型自动选择是否调用函数
            }
            
            self.last_request = request_data
            self._log_debug(LogType.REQUEST, request_data)
            
            # 发送请求
            response = self.client.chat.completions.create(**request_data)
            response_data = response.model_dump()
            self.raw_response = response_data
            self._log_debug(LogType.RESPONSE, response_data)
            
            # 处理函数调用
            if response.choices and response.choices[0].message:
                message = response.choices[0].message
                
                # 处理tool_calls
                if message.tool_calls:
                    for tool_call in message.tool_calls:
                        handle_conversation_tool_call(
                            tool_call,
                            messages,
                            self.available_functions,
                            self.logger
                        )
                    
                    # 如果有函数调用结果，再次调用模型生成最终响应
                    final_response = self.client.chat.completions.create(
                        model=config.GPT4_DEPLOYMENT_NAME,
                        messages=messages
                    )
                    response = final_response
            
            # 记录耗时
            self.execution_time = time.time() - start_time
            self._log_debug(LogType.TIMING, f"{self.execution_time:.2f} 秒")
            
            return response
            
        except Exception as e:
            self._log_debug(LogType.ERROR, str(e))
            raise 
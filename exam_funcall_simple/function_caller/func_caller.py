import time
import json
from typing import Dict, List, Any, Optional

from exam_funcall_simple.function_caller.infra import GPTBase, logger, GPT_MODEL_NAME
from exam_funcall_simple.function_caller.func_utils import prepare_messages, prepare_request_data
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
        super().__init__()
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
        logger.user_input(user_message)
        
        try:
            # 准备请求
            messages = prepare_messages(user_message, system_message, history)
            request_data = prepare_request_data(messages, self.functions, force_function_call, user_message)
            # 确保 last_request 是可序列化的
            self.last_request = {
                "model": request_data["model"],
                "messages": request_data["messages"],
                "tools": request_data["tools"],
                "tool_choice": request_data.get("tool_choice", "auto")
            }
            logger.request_data(self.last_request)
            
            # 发送请求
            response = self.client.chat.completions.create(**request_data)
            response_data = response.model_dump()
            self.raw_response = response_data
            logger.api_response(response_data)
            
            # 处理函数调用
            if response.choices and response.choices[0].message:
                message = response.choices[0].message
                function_results = []
                
                # 处理tool_calls
                if message.tool_calls:
                    for tool_call in message.tool_calls:
                        if tool_call.type == "function":
                            logger.function_call(
                                tool_call.function.name,
                                tool_call.function.arguments
                            )
                            
                            func_name = tool_call.function.name
                            func_args = json.loads(tool_call.function.arguments)
                            function_response = execute_function(
                                func_name,
                                func_args,
                                self.available_functions,
                                logger
                            )
                            
                            function_results.append({
                                'name': func_name,
                                'result': function_response
                            })
                
                response.function_results = function_results
            
            # 记录耗时
            self.execution_time = time.time() - start_time
            logger.execution_time(self.execution_time)
            
            return response
            
        except Exception as e:
            logger.error(str(e))
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
        logger.user_input(user_message)
        
        try:
            # 准备请求
            messages = prepare_messages(user_message, system_message, history)
            request_data = {
                **prepare_request_data(messages, self.functions, True, user_message),
                "tool_choice": "auto"  # 让模型自动选择是否调用函数
            }
            
            # 确保 last_request 是可序列化的
            self.last_request = {
                "model": request_data["model"],
                "messages": request_data["messages"],
                "tools": request_data["tools"],
                "tool_choice": request_data.get("tool_choice", "auto")
            }
            logger.request_data(self.last_request)
            
            # 发送请求
            response = self.client.chat.completions.create(**request_data)
            response_data = response.model_dump()
            self.raw_response = response_data
            logger.api_response(response_data)
            
            # 处理函数调用
            if response.choices and response.choices[0].message:
                message = response.choices[0].message
                
                # 处理tool_calls
                while message.tool_calls:
                    for tool_call in message.tool_calls:
                        handle_conversation_tool_call(
                            tool_call,
                            messages,
                            self.available_functions,
                            logger
                        )
                    
                    # 生成新的响应
                    response = self.client.chat.completions.create(
                        model=GPT_MODEL_NAME,
                        messages=messages,
                        tools=[{"type": "function", "function": f} for f in self.functions],
                        tool_choice="auto"
                    )
                    
                    if response.choices and response.choices[0].message:
                        message = response.choices[0].message
                        if not message.tool_calls:
                            # 如果没有更多的函数调用，添加最终响应到消息历史
                            messages.append({
                                "role": "assistant",
                                "content": message.content,
                                "tool_calls": None
                            })
                    else:
                        break
            
            # 记录耗时
            self.execution_time = time.time() - start_time
            logger.execution_time(self.execution_time)
            
            # 返回最后一个响应，但保持tool_calls字段
            if response.choices and response.choices[0].message:
                message = response.choices[0].message
                if not message.tool_calls:
                    # 如果最后一个响应没有tool_calls，我们需要从历史中找到最后一个带有tool_calls的消息
                    for msg in reversed(messages):
                        if msg.get("role") == "assistant" and msg.get("tool_calls"):
                            response.choices[0].message.tool_calls = msg["tool_calls"]
                            break
            
            return response
            
        except Exception as e:
            logger.error(str(e))
            raise 
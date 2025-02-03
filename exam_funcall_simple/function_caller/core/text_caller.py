import time
from typing import Dict, List, Any, Optional

from exam_funcall_simple.function_caller.infra.config import GPT4_DEPLOYMENT_NAME
from exam_funcall_simple.function_caller.infra import GPTBase, LogType

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
                "model": GPT4_DEPLOYMENT_NAME,
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
            self.execution_time = time.time() - start_time
            self._log_debug(LogType.TIMING, f"{self.execution_time:.2f} 秒")
            
            return response
            
        except Exception as e:
            self._log_debug(LogType.ERROR, str(e))
            raise 
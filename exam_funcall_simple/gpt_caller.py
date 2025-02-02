from openai import AzureOpenAI
import json
from datetime import datetime
import time

from exam_funcall_simple import config
from exam_funcall_simple import func_simple

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
        
    def _log_debug(self, title: str, content: any):
        """输出调试信息"""
        if self.debug:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            print(f"\n=== {title} === [{timestamp}]")
            if isinstance(content, str):
                print(content)
            else:
                print(json.dumps(content, indent=2, ensure_ascii=False))
                
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
        self._log_debug("用户输入", user_message)
        
        # 准备请求
        messages = [{"role": "user", "content": user_message}]
        request_data = {
            "model": config.GPT4_DEPLOYMENT_NAME,
            "messages": messages,
            "functions": func_simple.FUNCTION_DESCRIPTIONS,
            "function_call": "auto"
        }
        self._log_debug("请求数据", request_data)
        
        # 发送请求
        try:
            response = self.client.chat.completions.create(**request_data)
            
            # 记录响应
            response_data = response.model_dump()
            self._log_debug("原始响应", response_data)
            
            # 提取并记录函数调用信息
            if response.choices and response.choices[0].message.function_call:
                self._log_debug(
                    "函数调用信息", 
                    self._format_function_call(response.choices[0].message.function_call)
                )
                
                # 执行函数调用
                func_name = response.choices[0].message.function_call.name
                func_args = json.loads(response.choices[0].message.function_call.arguments)
                
                if func_name in self.available_functions:
                    function_response = self.available_functions[func_name](**func_args)
                    self._log_debug("函数执行结果", str(function_response))
            
            # 记录完整耗时
            elapsed_time = time.time() - start_time
            self._log_debug("执行耗时", f"{elapsed_time:.2f} 秒")
            
            return response
            
        except Exception as e:
            self._log_debug("错误信息", str(e))
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
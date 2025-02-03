import os
from typing import Dict, List, Any, Optional, Tuple
from dotenv import load_dotenv
from openai import AzureOpenAI

# 加载环境变量
load_dotenv()

GPT_MODEL_NAME = "gpt-4o"

class AzureConfig:
    """Azure OpenAI配置"""
    ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    API_VERSION = os.getenv("AZURE_OPENAI_VERSION", "2024-02-15-preview")


    @classmethod
    def test_connection(cls) -> Tuple[bool, str]:
        """测试Azure OpenAI连接"""
        try:
            client = AzureOpenAI(
                api_key=cls.API_KEY,
                api_version=cls.API_VERSION,
                azure_endpoint=cls.ENDPOINT
            )
            response = client.chat.completions.create(
                model=GPT_MODEL_NAME,
                messages=[{"role": "user", "content": "Say 'Hello, World!'"}],
                max_tokens=30
            )
            return True, response.choices[0].message.content
        except Exception as e:
            return False, str(e)

class GPTBase:
    """GPT调用器基类"""
    
    def __init__(self):
        """初始化基类"""
        self.client = AzureOpenAI(
            api_key=AzureConfig.API_KEY,
            api_version=AzureConfig.API_VERSION,
            azure_endpoint=AzureConfig.ENDPOINT
        )
        self.last_request = None
        self.raw_response = None
        self.execution_time = 0.0
    
    def call(
            self,
            user_message: str,
            system_message: Optional[str] = None,
            history: Optional[List[Dict[str, str]]] = None
    ) -> Any:
        """基础调用方法"""
        raise NotImplementedError("Subclasses must implement call method")

if __name__ == "__main__":
    from exam_funcall.function_caller.infra.logger import logger

    # 测试Azure连接
    logger.test_header("Testing Azure OpenAI Connection")
    success, result = AzureConfig.test_connection()
    if success:
        logger.function_result("Connection successful: " + result)
    else:
        logger.error("Connection failed: " + result) 
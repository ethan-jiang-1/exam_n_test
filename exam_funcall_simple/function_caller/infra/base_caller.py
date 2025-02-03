from openai import AzureOpenAI
from typing import Dict, List, Any, Optional

from exam_funcall_simple.function_caller.infra.config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_VERSION,
    AZURE_OPENAI_ENDPOINT
)
from exam_funcall_simple.function_caller.infra.logger import LogType, setup_logger, log_debug

class GPTBase:
    """GPT调用器基类，提供基础功能"""
    
    def __init__(self, debug: bool = True):
        """初始化基类
        Args:
            debug: 是否启用调试模式
        """
        self.client = AzureOpenAI(
            api_key=AZURE_OPENAI_API_KEY,
            api_version=AZURE_OPENAI_VERSION,
            azure_endpoint=AZURE_OPENAI_ENDPOINT
        )
        
        self.debug = debug
        self.logger = setup_logger(debug)
        self.last_request = None
        self.raw_response = None
        self.execution_time = 0.0
    
    def _log_debug(self, log_type: LogType, content: any):
        """输出调试信息"""
        log_debug(self.logger, log_type, content)
    
    def call(
            self,
            user_message: str,
            system_message: Optional[str] = None,
            history: Optional[List[Dict[str, str]]] = None
    ) -> Any:
        """基础调用方法"""
        raise NotImplementedError("Subclasses must implement call method") 
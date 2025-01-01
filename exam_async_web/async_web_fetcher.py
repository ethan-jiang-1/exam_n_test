"""
异步网页内容获取器模块

这个模块提供了一个高性能的异步网页内容获取器，支持并发获取、超时控制、
自定义请求头和二进制内容获取。主要特性包括：
- 异步并发获取
- 可控制的并发数量
- 超时控制
- 自定义请求头
- 二进制内容支持
- 完善的错误处理
"""

import aiohttp
import asyncio
from typing import List, Dict, Optional, Union
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AsyncWebFetcher:
    """
    异步网页内容获取器类
    
    这个类实现了异步上下文管理器接口，可以自动管理资源的创建和释放。
    使用示例:
        async with AsyncWebFetcher() as fetcher:
            result = await fetcher.fetch_page("https://example.com")
    """

    def __init__(self, max_concurrent: int = 5, timeout: int = 30):
        """
        初始化异步获取器
        
        Args:
            max_concurrent: 最大并发获取数
            timeout: 请求超时时间（秒）
        """
        self.max_concurrent = max_concurrent
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self._session: Optional[aiohttp.ClientSession] = None
        self.semaphore: Optional[asyncio.Semaphore] = None

    async def __aenter__(self):
        """
        异步上下文管理器的进入方法
        创建 aiohttp 会话和并发控制信号量
        """
        self._session = aiohttp.ClientSession(timeout=self.timeout)
        self.semaphore = asyncio.Semaphore(self.max_concurrent)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        异步上下文管理器的退出方法
        确保 aiohttp 会话被正确关闭
        """
        if self._session:
            await self._session.close()

    async def fetch_page(
            self, url: str, headers: Optional[Dict] = None,
            as_binary: bool = False) -> Dict[str, Union[str, bytes]]:
        """
        获取单个页面内容
        
        Args:
            url: 目标URL
            headers: 自定义请求头
            as_binary: 是否以二进制形式返回内容
        
        Returns:
            包含获取结果的字典，格式为：
            {
                "url": str,          # 请求的URL
                "status": str,       # 状态码或状态（"200"/"error"/"timeout"）
                "content": Union[str, bytes],  # 响应内容
                "headers": Dict      # 响应头
            }
        """
        if not self._session:
            raise RuntimeError("Fetcher not initialized. Use async with.")
            
        async with self.semaphore:  # 使用信号量控制并发
            try:
                async with self._session.get(url, headers=headers) as response:
                    if as_binary:
                        content = await response.read()  # 二进制读取
                    else:
                        content = await response.text()  # 文本读取
                    return {
                        "url": url,
                        "status": str(response.status),
                        "content": content,
                        "headers": dict(response.headers)
                    }
            except asyncio.TimeoutError as e:
                # 处理超时错误
                logger.error(f"Timeout fetching {url}: {str(e)}")
                return {
                    "url": url,
                    "status": "timeout",
                    "content": str(e)
                }
            except Exception as e:
                # 处理其他所有错误
                logger.error(f"Error fetching {url}: {str(e)}")
                return {
                    "url": url,
                    "status": "error",
                    "content": str(e)
                }

    async def fetch_pages(
            self, urls: List[str], headers: Optional[Dict] = None,
            as_binary: bool = False) -> List[Dict[str, Union[str, bytes]]]:
        """
        并发获取多个页面内容
        
        Args:
            urls: URL列表
            headers: 自定义请求头
            as_binary: 是否以二进制形式返回内容
        
        Returns:
            获取结果列表，每个元素的格式同 fetch_page 的返回值
        """
        tasks = [self.fetch_page(url, headers, as_binary) for url in urls]
        return await asyncio.gather(*tasks)

async def download_urls(
        urls: List[str], max_concurrent: int = 5, timeout: int = 30,
        headers: Optional[Dict] = None,
        as_binary: bool = False) -> List[Dict[str, Union[str, bytes]]]:
    """
    便捷的获取函数，自动处理获取器的创建和清理
    
    这是推荐使用的主要接口，它会自动处理 AsyncWebFetcher 的生命周期。
    
    Args:
        urls: URL列表
        max_concurrent: 最大并发数
        timeout: 请求超时时间（秒）
        headers: 自定义请求头
        as_binary: 是否以二进制形式返回内容
    
    Returns:
        获取结果列表，每个元素的格式同 fetch_page 的返回值
    
    示例:
        results = await download_urls(
            ["https://example.com"],
            max_concurrent=3,
            timeout=30,
            headers={"User-Agent": "CustomBot/1.0"}
        )
    """
    async with AsyncWebFetcher(max_concurrent, timeout) as fetcher:
        return await fetcher.fetch_pages(urls, headers, as_binary) 
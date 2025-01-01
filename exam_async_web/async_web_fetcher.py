"""
异步网页内容获取器模块

提供简单的异步网页内容获取功能，支持并发获取、超时控制、自定义请求头和二进制内容获取。

主要函数：
- fetch_urls: 并发获取多个URL的内容
- fetch_url: 获取单个URL的内容
"""

import aiohttp
import asyncio
from typing import List, Dict, Optional, Union
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def fetch_url(
    url: str, *,
    headers: Optional[Dict] = None,
    timeout: int = 30,
    as_binary: bool = False
) -> Dict[str, Union[str, bytes]]:
    """
    获取单个URL的内容

    Args:
        url: 目标URL
        headers: 可选的请求头
        timeout: 超时时间（秒）
        as_binary: 是否以二进制形式返回内容

    Returns:
        包含获取结果的字典：
        {
            "url": str,          # 请求的URL
            "status": str,       # 状态码或状态（"200"/"error"/"timeout"）
            "content": Union[str, bytes],  # 响应内容
            "headers": Dict      # 响应头
        }
    """
    timeout_obj = aiohttp.ClientTimeout(total=timeout)
    try:
        async with aiohttp.ClientSession(timeout=timeout_obj) as session:
            async with session.get(url, headers=headers) as response:
                if as_binary:
                    content = await response.read()
                else:
                    content = await response.text()
                return {
                    "url": url,
                    "status": str(response.status),
                    "content": content,
                    "headers": dict(response.headers)
                }
    except asyncio.TimeoutError as e:
        logger.error(f"Timeout fetching {url}: {str(e)}")
        return {
            "url": url,
            "status": "timeout",
            "content": str(e)
        }
    except Exception as e:
        logger.error(f"Error fetching {url}: {str(e)}")
        return {
            "url": url,
            "status": "error",
            "content": str(e)
        }

async def fetch_urls(
    urls: List[str], *,
    max_concurrent: int = 5,
    headers: Optional[Dict] = None,
    timeout: int = 30,
    as_binary: bool = False
) -> List[Dict[str, Union[str, bytes]]]:
    """
    并发获取多个URL的内容

    Args:
        urls: URL列表
        max_concurrent: 最大并发数
        headers: 可选的请求头
        timeout: 超时时间（秒）
        as_binary: 是否以二进制形式返回内容

    Returns:
        获取结果列表，每个元素的格式同 fetch_url 的返回值

    示例:
        results = await fetch_urls(
            ["https://example.com"],
            max_concurrent=3,
            timeout=30,
            headers={"User-Agent": "CustomBot/1.0"}
        )
    """
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def fetch_with_semaphore(url: str) -> Dict[str, Union[str, bytes]]:
        async with semaphore:
            return await fetch_url(url, headers=headers, timeout=timeout, as_binary=as_binary)
    
    return await asyncio.gather(*[fetch_with_semaphore(url) for url in urls])

# 为了向后兼容，保留原来的函数名，但标记为弃用
async def download_urls(*args, **kwargs):
    """
    此函数已弃用，请使用 fetch_urls
    """
    import warnings
    warnings.warn(
        "download_urls is deprecated, use fetch_urls instead",
        DeprecationWarning,
        stacklevel=2
    )
    return await fetch_urls(*args, **kwargs) 
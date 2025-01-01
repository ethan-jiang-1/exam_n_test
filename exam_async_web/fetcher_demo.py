"""
异步网页内容获取器演示脚本

这个脚本演示了异步网页内容获取器的各种功能，包括：
1. 基本的并发获取
2. 自定义请求头的使用
3. 二进制内容获取
4. 错误处理机制
5. 超时控制
"""

import asyncio
import json
from async_web_fetcher import download_urls
import time

async def test_different_scenarios():
    """
    测试异步获取器的不同场景
    包含五个主要测试场景，每个场景演示不同的功能特性
    """
    
    # 测试场景1：普通网页获取
    # 演示基本的并发获取功能和性能
    print("\n1. 测试普通网页获取:")
    urls = [
        "https://httpbin.org/get",      # 基本GET请求
        "https://httpbin.org/ip",       # 获取IP信息
        "https://httpbin.org/user-agent"  # 获取User-Agent信息
    ]
    start = time.time()
    results = await download_urls(urls, max_concurrent=2)  # 限制并发数为2
    duration = time.time() - start
    print(f"获取 {len(urls)} 个页面耗时: {duration:.2f} 秒")
    for result in results:
        print(f"URL: {result['url']}")
        print(f"状态: {result['status']}")
        print("---")

    # 测试场景2：自定义请求头
    # 演示如何设置和验证自定义HTTP请求头
    print("\n2. 测试自定义请求头:")
    headers = {"User-Agent": "CustomBot/1.0", "Accept": "application/json"}
    result = (await download_urls(["https://httpbin.org/headers"], headers=headers))[0]
    print("发送的请求头:")
    print(json.loads(result["content"])["headers"])

    # 测试场景3：二进制内容获取
    # 演示获取二进制文件（如图片）的功能
    print("\n3. 测试二进制内容获取:")
    image_urls = ["https://httpbin.org/image/png"]
    results = await download_urls(image_urls, as_binary=True)
    for result in results:
        print(f"图片大小: {len(result['content'])} 字节")
        print(f"Content-Type: {result['headers'].get('Content-Type')}")

    # 测试场景4：错误处理
    # 演示各种错误情况的处理，包括：
    # - 正常请求
    # - 域名不存在
    # - 404错误
    print("\n4. 测试错误处理:")
    error_urls = [
        "https://httpbin.org/get",  # 正常URL
        "https://this-domain-does-not-exist-123.com",  # 不存在的域名
        "https://httpbin.org/status/404"  # 404错误
    ]
    results = await download_urls(error_urls)
    for result in results:
        print(f"URL: {result['url']}")
        print(f"状态: {result['status']}")
        print("---")

    # 测试场景5：超时处理
    # 演示请求超时的处理机制
    print("\n5. 测试超时处理:")
    timeout_urls = ["https://httpbin.org/delay/5"]  # 这个endpoint会延迟5秒
    results = await download_urls(timeout_urls, timeout=2)  # 设置2秒超时
    for result in results:
        print(f"URL: {result['url']}")
        print(f"状态: {result['status']}")
        print("---")

if __name__ == "__main__":
    # 运行所有测试场景
    asyncio.run(test_different_scenarios()) 
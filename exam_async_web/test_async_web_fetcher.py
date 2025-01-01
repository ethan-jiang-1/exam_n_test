"""
异步网页内容获取器的单元测试
"""
import pytest
import asyncio
from async_web_fetcher import AsyncWebFetcher, download_urls

@pytest.mark.asyncio
async def test_fetch_single_page():
    """测试单个页面获取"""
    async with AsyncWebFetcher() as fetcher:
        result = await fetcher.fetch_page("https://httpbin.org/get")
        assert result["status"] == "200"
        assert "content" in result
        assert "headers" in result
        assert isinstance(result["content"], str)

@pytest.mark.asyncio
async def test_fetch_multiple_pages():
    """测试多个页面并发获取"""
    urls = [
        "https://httpbin.org/get",
        "https://httpbin.org/ip",
        "https://httpbin.org/user-agent"
    ]
    results = await download_urls(urls, max_concurrent=2)
    assert len(results) == len(urls)
    for result in results:
        assert result["status"] == "200"
        assert "content" in result
        assert "headers" in result

@pytest.mark.asyncio
async def test_custom_headers():
    """测试自定义请求头"""
    headers = {"User-Agent": "TestBot/1.0", "Accept": "application/json"}
    async with AsyncWebFetcher() as fetcher:
        result = await fetcher.fetch_page("https://httpbin.org/headers", headers=headers)
        assert result["status"] == "200"
        content = eval(result["content"])
        assert "TestBot" in content["headers"]["User-Agent"]
        assert content["headers"]["Accept"] == "application/json"

@pytest.mark.asyncio
async def test_binary_content():
    """测试二进制内容获取"""
    async with AsyncWebFetcher() as fetcher:
        result = await fetcher.fetch_page("https://httpbin.org/image/png", as_binary=True)
        assert result["status"] == "200"
        assert isinstance(result["content"], bytes)
        assert result["headers"]["Content-Type"] == "image/png"

@pytest.mark.asyncio
async def test_error_handling():
    """测试错误处理"""
    async with AsyncWebFetcher() as fetcher:
        # 测试404错误
        result = await fetcher.fetch_page("https://httpbin.org/status/404")
        assert result["status"] == "404"

        # 测试无效域名
        result = await fetcher.fetch_page("https://this-domain-does-not-exist-123.com")
        assert result["status"] == "error"

@pytest.mark.asyncio
async def test_timeout():
    """测试超时处理"""
    async with AsyncWebFetcher(timeout=2) as fetcher:
        result = await fetcher.fetch_page("https://httpbin.org/delay/5")
        assert result["status"] == "timeout"

@pytest.mark.asyncio
async def test_concurrent_limit():
    """测试并发限制"""
    urls = ["https://httpbin.org/delay/1"] * 5
    start_time = asyncio.get_event_loop().time()
    
    async with AsyncWebFetcher(max_concurrent=2) as fetcher:
        results = await fetcher.fetch_pages(urls)
    
    duration = asyncio.get_event_loop().time() - start_time
    assert duration >= 2.5  # 由于并发限制为2，5个1秒的请求应该至少需要2.5秒
    assert len(results) == len(urls)
    for result in results:
        assert result["status"] == "200"

@pytest.mark.asyncio
async def test_session_management():
    """测试会话管理"""
    fetcher = AsyncWebFetcher()
    # 在进入上下文之前应该没有会话
    assert fetcher._session is None
    
    async with fetcher as f:
        # 进入上下文后应该有会话
        assert f._session is not None
        result = await f.fetch_page("https://httpbin.org/get")
        assert result["status"] == "200"
    
    # 退出上下文后会话应该被关闭
    assert fetcher._session.closed

@pytest.mark.asyncio
async def test_invalid_usage():
    """测试无效使用场景"""
    fetcher = AsyncWebFetcher()
    with pytest.raises(RuntimeError):
        # 不使用上下文管理器应该抛出异常
        await fetcher.fetch_page("https://httpbin.org/get") 
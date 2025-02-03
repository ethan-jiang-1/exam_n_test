"""
异步网页内容获取器的单元测试
"""
import pytest
import asyncio
from async_web_fetcher import fetch_url, fetch_urls

@pytest.mark.asyncio
async def test_fetch_single_url():
    """测试单个URL获取"""
    result = await fetch_url("https://httpbin.org/get")
    assert result["status"] == "200"
    assert "content" in result
    assert "headers" in result
    assert isinstance(result["content"], str)

@pytest.mark.asyncio
async def test_fetch_multiple_urls():
    """测试多个URL并发获取"""
    urls = [
        "https://httpbin.org/get",
        "https://httpbin.org/ip",
        "https://httpbin.org/user-agent"
    ]
    results = await fetch_urls(urls, max_concurrent=2)
    assert len(results) == len(urls)
    for result in results:
        assert result["status"] == "200"
        assert "content" in result
        assert "headers" in result

@pytest.mark.asyncio
async def test_custom_headers():
    """测试自定义请求头"""
    headers = {"User-Agent": "TestBot/1.0", "Accept": "application/json"}
    result = await fetch_url(
        "https://httpbin.org/headers",
        headers=headers
    )
    assert result["status"] == "200"
    content = eval(result["content"])
    assert "TestBot" in content["headers"]["User-Agent"]
    assert content["headers"]["Accept"] == "application/json"

@pytest.mark.asyncio
async def test_binary_content():
    """测试二进制内容获取"""
    result = await fetch_url(
        "https://httpbin.org/image/png",
        as_binary=True
    )
    assert result["status"] == "200"
    assert isinstance(result["content"], bytes)
    assert result["headers"]["Content-Type"] == "image/png"

@pytest.mark.asyncio
async def test_error_handling():
    """测试错误处理"""
    # 测试404错误
    result = await fetch_url("https://httpbin.org/status/404")
    assert result["status"] == "404"

    # 测试无效域名
    result = await fetch_url("https://this-domain-does-not-exist-123.com")
    assert result["status"] == "error"

@pytest.mark.asyncio
async def test_timeout():
    """测试超时处理"""
    result = await fetch_url(
        "https://httpbin.org/delay/5",
        timeout=2
    )
    assert result["status"] == "timeout"

@pytest.mark.asyncio
async def test_concurrent_limit():
    """测试并发限制"""
    urls = ["https://httpbin.org/delay/1"] * 5
    start_time = asyncio.get_event_loop().time()
    
    results = await fetch_urls(urls, max_concurrent=2)
    
    duration = asyncio.get_event_loop().time() - start_time
    assert duration >= 2.5  # 由于并发限制为2，5个1秒的请求应该至少需要2.5秒
    assert len(results) == len(urls)
    for result in results:
        assert result["status"] == "200"

@pytest.mark.asyncio
async def test_deprecated_download_urls():
    """测试弃用的download_urls函数"""
    import warnings
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = await fetch_url("https://httpbin.org/get")
        assert result["status"] == "200"
        
        # 确保使用旧函数名时会发出警告
        from async_web_fetcher import download_urls
        results = await download_urls(["https://httpbin.org/get"])
        assert len(results) == 1  # 验证结果
        assert len(w) == 1
        assert issubclass(w[-1].category, DeprecationWarning)
        assert "deprecated" in str(w[-1].message) 
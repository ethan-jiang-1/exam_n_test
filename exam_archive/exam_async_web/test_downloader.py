import pytest
import asyncio
from .downloader import AsyncWebDownloader, download_urls

@pytest.mark.asyncio
async def test_single_download():
    test_url = "https://httpbin.org/get"
    async with AsyncWebDownloader() as downloader:
        result = await downloader.download_page(test_url)
        assert result["status"] == "200"
        assert result["url"] == test_url
        assert "content" in result
        assert "headers" in result

@pytest.mark.asyncio
async def test_multiple_downloads():
    test_urls = [
        "https://httpbin.org/get",
        "https://httpbin.org/ip",
        "https://httpbin.org/user-agent"
    ]
    results = await download_urls(test_urls, max_concurrent=2)
    assert len(results) == len(test_urls)
    for result in results:
        assert result["status"] == "200"
        assert "content" in result
        assert "headers" in result

@pytest.mark.asyncio
async def test_error_handling():
    test_urls = [
        "https://httpbin.org/get",
        "https://invalid-domain-that-does-not-exist.com",
    ]
    results = await download_urls(test_urls)
    assert len(results) == len(test_urls)
    assert results[0]["status"] == "200"  # 第一个URL应该成功
    assert results[1]["status"] == "error"  # 第二个URL应该失败

@pytest.mark.asyncio
async def test_timeout():
    test_url = "https://httpbin.org/delay/5"  # 这个endpoint会延迟5秒
    async with AsyncWebDownloader(timeout=2) as downloader:  # 设置2秒超时
        result = await downloader.download_page(test_url)
        assert result["status"] == "timeout"

@pytest.mark.asyncio
async def test_custom_headers():
    custom_headers = {"User-Agent": "CustomBot/1.0"}
    test_url = "https://httpbin.org/headers"
    async with AsyncWebDownloader() as downloader:
        result = await downloader.download_page(test_url, headers=custom_headers)
        assert result["status"] == "200"
        # httpbin会返回请求头信息，我们可以验证自定义头是否生效
        content = eval(result["content"])  # 安全的环境下可以这样做
        assert "CustomBot" in content["headers"]["User-Agent"]

@pytest.mark.asyncio
async def test_binary_download():
    test_url = "https://httpbin.org/image/png"
    async with AsyncWebDownloader() as downloader:
        result = await downloader.download_page(test_url, as_binary=True)
        assert result["status"] == "200"
        assert isinstance(result["content"], bytes)
        assert result["headers"]["Content-Type"] == "image/png"

@pytest.mark.asyncio
async def test_concurrent_limit():
    # 创建5个URL，但限制并发为2
    test_urls = ["https://httpbin.org/delay/1"] * 5
    start_time = asyncio.get_event_loop().time()
    
    async with AsyncWebDownloader(max_concurrent=2) as downloader:
        results = await downloader.download_pages(test_urls)
    
    end_time = asyncio.get_event_loop().time()
    duration = end_time - start_time
    
    # 由于并发限制为2，且每个请求需要1秒
    # 5个请求应该至少需要3秒（向上取整）
    assert duration >= 2.5
    assert len(results) == len(test_urls)
    for result in results:
        assert result["status"] == "200" 
"""
测试简化的fetch接口
"""
import pytest
from exam_async_web import fetch

@pytest.mark.asyncio
async def test_fetch_single_url():
    """测试获取单个URL"""
    result = await fetch("https://httpbin.org/get")
    assert isinstance(result, dict)
    assert result["status"] == "200"
    assert "content" in result
    assert "headers" in result

@pytest.mark.asyncio
async def test_fetch_multiple_urls():
    """测试获取多个URL"""
    urls = [
        "https://httpbin.org/get",
        "https://httpbin.org/ip"
    ]
    results = await fetch(urls, max_concurrent=2)
    assert isinstance(results, list)
    assert len(results) == 2
    for result in results:
        assert result["status"] == "200"

@pytest.mark.asyncio
async def test_fetch_with_options():
    """测试带选项的获取"""
    # 测试自定义头部
    headers = {"User-Agent": "TestBot/1.0"}
    result = await fetch(
        "https://httpbin.org/headers",
        headers=headers
    )
    assert "TestBot" in result["content"]

    # 测试二进制内容
    result = await fetch(
        "https://httpbin.org/image/png",
        as_binary=True
    )
    assert isinstance(result["content"], bytes)

    # 测试超时
    result = await fetch(
        "https://httpbin.org/delay/5",
        timeout=2
    )
    assert result["status"] == "timeout" 
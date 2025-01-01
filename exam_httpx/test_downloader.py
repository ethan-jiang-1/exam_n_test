import pytest
import httpx
import respx
from downloader import WebDownloader, download_page
@pytest.fixture
def mock_webpage():
    return "<html><body>Test Content</body></html>"

@pytest.fixture
def temp_file(tmp_path):
    return tmp_path / "test.html"

@respx.mock
@pytest.mark.asyncio
async def test_download_page():
    test_url = "https://example.com"
    test_content = "<html><body>Test Content</body></html>"
    
    # Mock the HTTP request
    respx.get(test_url).mock(return_value=httpx.Response(200, text=test_content))
    
    # Test without saving
    downloader = WebDownloader()
    content = await downloader.download_page(test_url)
    assert content == test_content

@respx.mock
@pytest.mark.asyncio
async def test_download_and_save_page(temp_file):
    test_url = "https://example.com"
    test_content = "<html><body>Test Content</body></html>"
    
    # Mock the HTTP request
    respx.get(test_url).mock(return_value=httpx.Response(200, text=test_content))
    
    # Test with saving
    downloader = WebDownloader()
    content = await downloader.download_page(test_url, temp_file)
    
    # Verify content was saved correctly
    assert content == test_content
    assert temp_file.exists()
    assert temp_file.read_text(encoding='utf-8') == test_content

@respx.mock
@pytest.mark.asyncio
async def test_download_page_http_error():
    test_url = "https://example.com"
    
    # Mock a failed HTTP request
    respx.get(test_url).mock(return_value=httpx.Response(404))
    
    # Test error handling
    downloader = WebDownloader()
    with pytest.raises(httpx.HTTPError):
        await downloader.download_page(test_url)

@respx.mock
@pytest.mark.asyncio
async def test_convenience_function():
    test_url = "https://example.com"
    test_content = "<html><body>Test Content</body></html>"
    
    # Mock the HTTP request
    respx.get(test_url).mock(return_value=httpx.Response(200, text=test_content))
    
    # Test the convenience function
    content = await download_page(test_url)
    assert content == test_content 
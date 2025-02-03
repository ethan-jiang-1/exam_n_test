import httpx
from pathlib import Path
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebDownloader:
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
    
    async def download_page(self, url: str, save_path: Optional[Path] = None) -> str:
        """
        下载网页内容并可选择保存到文件
        
        Args:
            url: 要下载的网页URL
            save_path: 保存文件的路径，如果为None则不保存
            
        Returns:
            str: 网页内容
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
                response = await client.get(url)
                response.raise_for_status()
                content = response.text
                
                if save_path:
                    save_path = Path(save_path)
                    save_path.parent.mkdir(parents=True, exist_ok=True)
                    save_path.write_text(content, encoding='utf-8')
                    logger.info(f"Successfully saved content to {save_path}")
                
                return content
                
        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            raise
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise

async def download_page(url: str, save_path: Optional[Path] = None) -> str:
    """便捷的函数封装"""
    downloader = WebDownloader()
    return await downloader.download_page(url, save_path) 
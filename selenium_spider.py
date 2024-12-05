import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from urllib.parse import urljoin, urlparse
import requests

class BrowserCrawler:
    def __init__(self, base_url, output_folder="downloaded_site"):
        self.base_url = base_url
        self.output_folder = output_folder
        self.visited_urls = set()
        self.chrome_options = self.get_chrome_options()

        # 创建浏览器实例
        self.driver = webdriver.Chrome(service=Service("/path/to/chromedriver"), options=self.chrome_options)  # 替换为你的 ChromeDriver 路径

        # 创建输出目录
        if os.path.exists(self.output_folder):
            import shutil
            shutil.rmtree(self.output_folder)
        os.makedirs(self.output_folder, exist_ok=True)

    def get_chrome_options(self):
        """配置 Chrome 浏览器选项"""
        options = Options()
        options.add_argument("--headless")  # 无头模式
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920x1080")
        return options

    def save_html(self, url, html):
        """保存 HTML 文件"""
        parsed_url = urlparse(url)
        file_name = parsed_url.path.strip("/") or "index"
        if not file_name.endswith(".html"):
            file_name += ".html"
        file_path = os.path.join(self.output_folder, parsed_url.netloc, file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)
        logging.info(f"Saved HTML: {file_path}")
        return file_path

    def save_resource(self, resource_url):
        """下载静态资源并保存"""
        try:
            response = requests.get(resource_url, stream=True)
            response.raise_for_status()

            parsed_url = urlparse(resource_url)
            resource_path = os.path.join(
                self.output_folder, "static", parsed_url.path.strip("/") or os.path.basename(parsed_url.path)
            )
            os.makedirs(os.path.dirname(resource_path), exist_ok=True)

            with open(resource_path, "wb") as f:
                for chunk in response.iter_content(8192):
                    f.write(chunk)
            logging.info(f"Saved resource: {resource_path}")
        except Exception as e:
            logging.error(f"Failed to save resource {resource_url}: {e}")

    def crawl_page(self, url):
        """爬取单个页面"""
        if url in self.visited_urls:
            return
        self.visited_urls.add(url)

        logging.info(f"Crawling: {url}")
        self.driver.get(url)
        time.sleep(2)  # 等待页面加载

        # 保存 HTML 文件
        html = self.driver.page_source
        self.save_html(url, html)

        # 提取静态资源
        for tag in self.driver.find_elements(By.TAG_NAME, "img"):
            src = tag.get_attribute("src")
            if src:
                self.save_resource(urljoin(url, src))

        for tag in self.driver.find_elements(By.TAG_NAME, "link"):
            href = tag.get_attribute("href")
            if href:
                self.save_resource(urljoin(url, href))

        for tag in self.driver.find_elements(By.TAG_NAME, "script"):
            src = tag.get_attribute("src")
            if src:
                self.save_resource(urljoin(url, src))

        # 提取内部链接并递归爬取
        for tag in self.driver.find_elements(By.TAG_NAME, "a"):
            href = tag.get_attribute("href")
            if href and self.base_url in href and href not in self.visited_urls:
                self.crawl_page(href)

    def run(self):
        """启动爬虫"""
        try:
            self.crawl_page(self.base_url)
        finally:
            self.driver.quit()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    target_url = "https://www.promptingguide.ai/zh"  # 替换为你的目标网站
    output_directory = "_selenium_crawl"

    crawler = BrowserCrawler(target_url, output_directory)
    crawler.run()

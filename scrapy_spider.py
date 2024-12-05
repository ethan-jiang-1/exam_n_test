import os
import scrapy
from urllib.parse import urljoin, urlparse, urlunparse
import logging
import uuid
from scrapy.crawler import CrawlerProcess

class PageItem(scrapy.Item):
    url = scrapy.Field()           # 原始 URL
    file_path = scrapy.Field()     # 本地保存路径
    content_type = scrapy.Field()  # 文件类型（HTML/静态资源）

class EmbeddedSpider(scrapy.Spider):
    name = "embedded_spider"

    def __init__(self, base_url, output_folder="downloaded_site", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [base_url]
        self.base_url = base_url
        self.output_folder = output_folder
        self.visited_urls = set()
        if os.path.exists(self.output_folder):
            import shutil
            shutil.rmtree(self.output_folder)
        os.makedirs(self.output_folder, exist_ok=True)

    def normalize_url(self, url):
        """标准化 URL 去掉参数和锚点"""
        parsed = urlparse(url)
        return urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", "", ""))

    def resolve_conflict(self, path):
        """解决文件路径冲突"""
        if os.path.exists(path):
            base, ext = os.path.splitext(path)
            return f"{base}_{uuid.uuid4().hex[:8]}{ext}"
        return path

    def parse(self, response):
        # 保存 HTML 文件
        html_item = self.save_html(response)
        if html_item:
            yield html_item

        # 提取资源
        for resource in response.css("img::attr(src), script::attr(src), link::attr(href)"):
            resource_url = urljoin(response.url, resource.get())
            yield scrapy.Request(resource_url, callback=self.save_resource)

        # 提取内部链接并递归
        for link in response.css("a::attr(href)"):
            full_url = urljoin(response.url, link.get())
            norm_url = self.normalize_url(full_url)
            if self.base_url in norm_url and norm_url not in self.visited_urls:
                self.visited_urls.add(norm_url)
                yield scrapy.Request(full_url, callback=self.parse)

    def save_html(self, response):
        try:
            parsed_url = urlparse(response.url)
            file_name = parsed_url.path.strip("/") or "index"
            if not file_name.endswith(".html"):
                file_name += ".html"
            file_path = os.path.join(self.output_folder, parsed_url.netloc, file_name)
            file_path = self.resolve_conflict(file_path)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # 使用 Scrapy Selector 解析 HTML
            soup = scrapy.Selector(response)

            # 修改资源路径（静态资源和跳转链接）
            for tag in soup.css("img, script, link"):
                attr = "src" if tag.root.tag != "link" else "href"
                resource_url = tag.attrib.get(attr)
                if resource_url:
                    local_path = self.get_local_path(urljoin(response.url, resource_url))
                    tag.root.attrib[attr] = os.path.relpath(local_path, start=os.path.dirname(file_path))

            # 修改跳转链接路径
            for link in soup.css("a"):
                href = link.attrib.get("href")
                if href:
                    if href.startswith("javascript:") or href.startswith("#"):
                        # 跳过 JavaScript 链接或锚点链接
                        continue
                    elif href.startswith("/") or href.startswith(self.base_url):
                        # 本地化站内链接
                        full_url = urljoin(response.url, href)
                        normalized_url = self.normalize_url(full_url)
                        if normalized_url.startswith(self.base_url):
                            local_path = self.get_local_html_path(normalized_url)
                            link.root.attrib["href"] = os.path.relpath(local_path, start=os.path.dirname(file_path))
                    else:
                        # 外部链接保持原样
                        continue

            # 保存修改后的 HTML 文件
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(soup.get())
            self.log(f"Saved HTML: {file_path}")

            # 返回 PageItem
            return PageItem(url=response.url, file_path=file_path, content_type="HTML")
        except Exception as ex:
            logging.exception("Error saving HTML", exc_info=ex)
            return None

    def save_resource(self, response):
        """保存静态资源到本地"""
        try:
            parsed_url = urlparse(response.url)
            resource_path = os.path.join(
                self.output_folder, "static", parsed_url.path.strip("/") or os.path.basename(parsed_url.path)
            )
            resource_path = self.resolve_conflict(resource_path)
            os.makedirs(os.path.dirname(resource_path), exist_ok=True)

            with open(resource_path, "wb") as f:
                f.write(response.body)
            self.log(f"Saved resource: {resource_path}")

            # 返回 PageItem
            return PageItem(url=response.url, file_path=resource_path, content_type="Resource")
        except Exception as ex:
            logging.exception("Error saving resource", exc_info=ex)
            return None

    def get_local_path(self, url):
        """根据资源 URL 生成本地路径"""
        parsed_url = urlparse(url)
        return os.path.join(self.output_folder, "static", parsed_url.path.strip("/") or os.path.basename(parsed_url.path))

    def get_local_html_path(self, url):
        """根据页面 URL 生成本地 HTML 文件路径"""
        parsed_url = urlparse(url)
        file_name = parsed_url.path.strip("/") or "index"
        if not file_name.endswith(".html"):
            file_name += ".html"
        return os.path.join(self.output_folder, parsed_url.netloc, file_name)




def run_scrapy_spider(base_url, output_folder):
    process = CrawlerProcess(settings={
        "LOG_LEVEL": "INFO",  # 调整日志级别
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",  # 模拟 Chrome 浏览器
        "CONCURRENT_REQUESTS": 1,  # 并发请求数量
        "DOWNLOAD_DELAY": 0.5,      # 每次请求之间的延迟，防止被封禁
    })
    process.crawl(EmbeddedSpider, base_url=base_url, output_folder=output_folder)
    process.start()  # 阻塞，直到爬虫完成


# 示例调用
if __name__ == "__main__":
    target_url = "https://www.promptingguide.ai/zh"  # 替换为你的目标网站
    output_directory = "_data_prompting_guide"
    run_scrapy_spider(target_url, output_directory)

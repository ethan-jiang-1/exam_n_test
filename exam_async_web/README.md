# AsyncWebFetcher - 异步网页内容获取器

这是一个基于 Python `aiohttp` 的异步网页内容获取器，支持并发获取、超时控制、自定义请求头和二进制内容下载。

## 功能特性

- ✨ 异步并发获取
- 🔄 可控制的并发数量
- ⏱️ 超时控制
- 📝 自定义请求头
- 🖼️ 二进制内容支持（如图片下载）
- 🚦 完善的错误处理
- 📊 详细的获取状态

## 安装依赖

```bash
pip install aiohttp
```

## 使用方法

### 基本用法

```python
import asyncio
from async_web_fetcher import download_urls

async def main():
    urls = [
        "https://example.com",
        "https://example.org"
    ]
    results = await download_urls(urls)
    for result in results:
        print(f"URL: {result['url']}, Status: {result['status']}")

if __name__ == "__main__":
    asyncio.run(main())
```

### 高级用法

```python
async def main():
    # 自定义配置
    urls = ["https://example.com/image.png"]
    results = await download_urls(
        urls,
        max_concurrent=3,        # 最大并发数
        timeout=30,             # 超时时间（秒）
        headers={               # 自定义请求头
            "User-Agent": "CustomBot/1.0",
            "Accept": "image/png"
        },
        as_binary=True         # 下载二进制内容
    )
```

## API 文档

### AsyncWebFetcher 类

主要的内容获取器类，支持异步上下文管理器。

#### 初始化参数

- `max_concurrent` (int, 默认=5): 最大并发获取数
- `timeout` (int, 默认=30): 请求超时时间（秒）

#### 方法

##### async fetch_page(url: str, headers: Optional[Dict] = None, as_binary: bool = False)

获取单个页面内容。

参数:
- `url`: 目标URL
- `headers`: 可选的请求头字典
- `as_binary`: 是否以二进制模式获取

返回:
```python
{
    "url": str,          # 请求的URL
    "status": str,       # 状态码或状态（"200"/"error"/"timeout"）
    "content": Union[str, bytes],  # 响应内容
    "headers": Dict      # 响应头
}
```

##### async fetch_pages(urls: List[str], headers: Optional[Dict] = None, as_binary: bool = False)

并发获取多个页面内容。

参数:
- `urls`: URL列表
- `headers`: 可选的请求头字典
- `as_binary`: 是否以二进制模式获取

返回:
- 返回结果列表，每个元素格式同 `fetch_page`

### 便捷函数

#### async download_urls(...)

便捷的获取函数，自动处理获取器的创建和清理。

参数:
- `urls`: URL列表
- `max_concurrent`: 最大并发数（默认=5）
- `timeout`: 超时时间（默认=30秒）
- `headers`: 可选的请求头字典
- `as_binary`: 是否以二进制模式获取

## 错误处理

获取器会处理以下错误情况：
- 网络连接错误
- DNS解析错误
- 超时错误
- HTTP错误（如404）

所有错误都会被捕获并返回适当的状态，不会抛出异常。

## 示例

查看 `fetcher_demo.py` 获取完整的使用示例，包括：
1. 普通网页获取
2. 自定义请求头
3. 二进制内容获取
4. 错误处理
5. 超时处理

## 注意事项

1. 使用 `AsyncWebFetcher` 时必须使用异步上下文管理器（async with）
2. 设置合适的并发数和超时时间以避免服务器过载
3. 获取大文件时建议使用二进制模式（as_binary=True） 
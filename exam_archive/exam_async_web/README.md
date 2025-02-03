# Async Web Fetcher

一个简单高效的异步网页内容获取工具。

## 特性

- ✨ 异步并发获取
- 🔄 可控制的并发数量
- ⏱️ 超时控制
- 📝 自定义请求头
- 🖼️ 二进制内容支持
- 🚦 完善的错误处理

## 安装

```bash
pip install exam-async-web
```

## 快速开始

### 基本用法

```python
import asyncio
from exam_async_web import fetch

async def main():
    # 获取单个页面
    result = await fetch("https://example.com")
    print(result["content"])

asyncio.run(main())
```

### 获取多个页面

```python
async def main():
    urls = [
        "https://example.com",
        "https://example.org"
    ]
    results = await fetch(urls, max_concurrent=3)
    for result in results:
        print(f"{result['url']}: {result['status']}")
```

### 下载图片

```python
async def main():
    result = await fetch(
        "https://example.com/image.png",
        as_binary=True
    )
    with open("image.png", "wb") as f:
        f.write(result["content"])
```

### 自定义请求头

```python
async def main():
    result = await fetch(
        "https://api.example.com",
        headers={
            "User-Agent": "MyBot/1.0",
            "Accept": "application/json"
        }
    )
```

## API 参考

### fetch(urls, **options)

主要函数，用于获取一个或多个URL的内容。

参数:
- `urls`: 字符串或字符串列表，要获取的URL
- `max_concurrent`: 整数，最大并发数（默认：5）
- `headers`: 字典，自定义请求头
- `timeout`: 整数，超时时间（秒）（默认：30）
- `as_binary`: 布尔值，是否以二进制形式返回内容

返回值:
```python
# 单个URL时返回字典：
{
    "url": str,          # 请求的URL
    "status": str,       # 状态码或状态（"200"/"error"/"timeout"）
    "content": str/bytes, # 响应内容
    "headers": dict      # 响应头
}

# URL列表时返回字典列表
```

## 错误处理

```python
async def main():
    # 处理404错误
    result = await fetch("https://example.com/not-found")
    if result["status"] == "404":
        print("页面不存在")
    
    # 处理超时
    result = await fetch("https://slow-server.com", timeout=5)
    if result["status"] == "timeout":
        print("请求超时")
```

## 开发

1. 克隆仓库
```bash
git clone https://github.com/yourusername/exam-async-web.git
cd exam-async-web
```

2. 安装依赖
```bash
pip install -e .
```

3. 运行测试
```bash
pytest
```

## 许可证

MIT License 
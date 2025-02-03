# Async Web Fetcher

一个简单高效的异步网页内容获取工具。

## 特性

- ✨ 异步并发获取
- 🔄 可控制的并发数量
- ⏱️ 超时控制
- 📝 自定义请求头
- 🖼️ 二进制内容支持
- 🚦 完善的错误处理

## 快速开始

```python
import asyncio
from exam_async_web import fetch

async def main():
    # 获取单个页面
    result = await fetch("https://example.com")
    print(result["content"])

    # 获取多个页面
    results = await fetch([
        "https://example.com",
        "https://example.org"
    ], max_concurrent=3)
    
    for result in results:
        print(f"{result['url']}: {result['status']}")

asyncio.run(main())
```

## 为什么选择 Async Web Fetcher?

- **简单**: 一个函数搞定所有功能
- **高效**: 异步并发，性能出色
- **可靠**: 完善的错误处理和超时控制
- **灵活**: 支持文本和二进制内容
- **友好**: 详细的文档和示例 
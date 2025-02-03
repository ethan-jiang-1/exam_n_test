# 使用教程

## 基础用法

### 获取单个页面

```python
import asyncio
from exam_async_web import fetch

async def main():
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

## 高级用法

### 自定义请求头

```python
async def main():
    headers = {
        "User-Agent": "MyBot/1.0",
        "Accept": "application/json"
    }
    result = await fetch(
        "https://api.example.com",
        headers=headers
    )
```

### 下载二进制文件

```python
async def main():
    # 下载图片
    result = await fetch(
        "https://example.com/image.png",
        as_binary=True
    )
    
    # 保存到文件
    if result["status"] == "200":
        with open("image.png", "wb") as f:
            f.write(result["content"])
```

### 设置超时

```python
async def main():
    # 设置5秒超时
    result = await fetch(
        "https://slow-server.com",
        timeout=5
    )
    
    if result["status"] == "timeout":
        print("请求超时")
```

## 错误处理

### 处理常见错误

```python
async def main():
    result = await fetch("https://example.com/not-found")
    
    match result["status"]:
        case "200":
            print("成功")
            process_content(result["content"])
        case "404":
            print("页面不存在")
        case "timeout":
            print("请求超时")
        case "error":
            print(f"发生错误: {result['content']}")
```

### 批量请求错误处理

```python
async def main():
    urls = [
        "https://example.com",
        "https://invalid-domain.com",
        "https://example.org"
    ]
    
    results = await fetch(urls)
    
    # 分类处理结果
    successful = [r for r in results if r["status"] == "200"]
    failed = [r for r in results if r["status"] != "200"]
    
    print(f"成功: {len(successful)}, 失败: {len(failed)}")
```

## 性能优化

### 控制并发数

```python
async def main():
    urls = ["https://example.com"] * 100
    
    # 限制并发数为10
    results = await fetch(urls, max_concurrent=10)
```

### 批量处理大量URL

```python
async def process_urls(urls, batch_size=50):
    """分批处理大量URL"""
    for i in range(0, len(urls), batch_size):
        batch = urls[i:i + batch_size]
        results = await fetch(batch, max_concurrent=10)
        process_results(results)
```

## 最佳实践

1. **设置合适的并发数**
   - 建议值：5-20
   - 根据目标服务器的承受能力调整

2. **合理的超时设置**
   - 普通网页：30秒
   - API调用：5-10秒
   - 文件下载：根据文件大小调整

3. **友好的请求头**
   ```python
   headers = {
       "User-Agent": "MyBot/1.0 (your@email.com)",
       "Accept": "*/*",
       "Accept-Encoding": "gzip, deflate"
   }
   ```

4. **资源清理**
   ```python
   async def main():
       try:
           results = await fetch(urls)
           process_results(results)
       except Exception as e:
           logger.error(f"Error: {e}")
       finally:
           # 清理资源
           cleanup_resources()
   ``` 
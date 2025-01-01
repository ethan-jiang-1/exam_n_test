# 安装指南

## 系统要求

- Python 3.7 或更高版本
- 支持异步 IO 的操作系统（Windows、macOS、Linux）

## 使用 pip 安装

最简单的安装方式是使用 pip：

```bash
pip install exam-async-web
```

## 从源码安装

如果你想要最新的开发版本，可以从源码安装：

```bash
git clone https://github.com/yourusername/exam-async-web.git
cd exam-async-web
pip install -e .
```

## 验证安装

安装完成后，你可以在 Python 中验证安装：

```python
import asyncio
from exam_async_web import fetch

async def test():
    result = await fetch("https://example.com")
    print(f"Status: {result['status']}")

asyncio.run(test())
```

如果没有报错并且能看到状态码输出，说明安装成功。

## 可选依赖

- `pytest`: 如果你想运行测试
- `pytest-asyncio`: 用于异步测试

安装可选依赖：

```bash
pip install exam-async-web[test]
```

## 常见问题

### ImportError: No module named 'exam_async_web'

确保你已经正确安装了包：
```bash
pip list | grep exam-async-web
```

### RuntimeError: Event loop is closed

在 Windows 上可能会遇到这个错误，解决方法：

```python
import asyncio
import platform

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
``` 
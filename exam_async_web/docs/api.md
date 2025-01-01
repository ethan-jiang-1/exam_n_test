# API 参考

## fetch

```python
async def fetch(
    urls: Union[str, List[str]], *,
    max_concurrent: int = 5,
    headers: Optional[Dict] = None,
    timeout: int = 30,
    as_binary: bool = False
) -> Union[Dict, List[Dict]]
```

主要函数，用于获取一个或多个URL的内容。

### 参数

- **urls** (`str | List[str]`)
    - 要获取的URL或URL列表
    - 单个URL时传入字符串
    - 多个URL时传入字符串列表

- **max_concurrent** (`int`, 可选)
    - 最大并发请求数
    - 默认值：5
    - 仅在传入URL列表时有效

- **headers** (`Dict[str, str]`, 可选)
    - 自定义HTTP请求头
    - 默认值：None
    - 示例：`{"User-Agent": "MyBot/1.0"}`

- **timeout** (`int`, 可选)
    - 请求超时时间（秒）
    - 默认值：30
    - 建议根据实际需求调整

- **as_binary** (`bool`, 可选)
    - 是否以二进制形式返回内容
    - 默认值：False
    - 下载图片等二进制文件时设为True

### 返回值

当传入单个URL时，返回字典：
```python
{
    "url": str,          # 请求的URL
    "status": str,       # 状态码或状态
    "content": str/bytes, # 响应内容
    "headers": dict      # 响应头
}
```

当传入URL列表时，返回字典列表，每个字典格式同上。

### 状态码

- `"200"`: 请求成功
- `"404"`: 页面不存在
- `"timeout"`: 请求超时
- `"error"`: 其他错误

### 异常处理

该函数不会抛出异常，所有错误都会在返回的字典中通过status字段表示。

### 示例

#### 基本用法

```python
# 获取单个页面
result = await fetch("https://example.com")
print(result["content"])

# 获取多个页面
results = await fetch([
    "https://example.com",
    "https://example.org"
])
```

#### 自定义选项

```python
# 设置请求头和超时
result = await fetch(
    "https://api.example.com",
    headers={"Accept": "application/json"},
    timeout=5
)

# 下载图片
result = await fetch(
    "https://example.com/image.png",
    as_binary=True
)
```

#### 错误处理

```python
result = await fetch("https://example.com")
match result["status"]:
    case "200":
        process_content(result["content"])
    case "404":
        handle_not_found()
    case "timeout":
        handle_timeout()
    case "error":
        handle_error(result["content"])
```

### 注意事项

1. **资源管理**
   - 函数会自动管理HTTP会话
   - 不需要手动关闭连接

2. **并发控制**
   - `max_concurrent`参数防止过度并发
   - 建议根据目标服务器调整

3. **内存使用**
   - 获取大文件时注意内存使用
   - 考虑分批处理大量URL

4. **错误处理**
   - 检查返回的status字段
   - 所有错误都有对应的错误信息 
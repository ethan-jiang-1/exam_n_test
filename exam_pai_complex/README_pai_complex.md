# PydanticAI Complex Examples

这个目录包含了一些 PydanticAI 的进阶用法示例。主要展示了三个方面：
1. System Prompt 的不同实现方式
2. 依赖注入的使用模式
3. 复杂工具链的调用方式

## 文件说明

### System Prompt 相关
- `system_prompt_static.py`: 最基础的用法，通过装饰器添加静态的 prompt
  ```python
  @agent.system_prompt
  def add_the_date() -> str:  
      return f'The date is {date.today()}.'
  ```

- `system_prompt_dynamic_http.py`: 从 HTTP 接口动态获取 prompt
  ```python
  @agent.system_prompt  
  async def get_system_prompt(ctx: RunContext[MyDeps]) -> str:  
      response = await ctx.deps.http_client.get('https://example.com')
      return f'Prompt: {response.text}'
  ```

- `system_prompt_type_check.py`: 演示类型检查和错误处理
  ```python
  agent = Agent(
      model,
      deps_type=User,  # 输入类型
      result_type=bool,  # 返回类型
  )
  ```

### 依赖注入相关
- `unused_dependencies.py`: 展示如何处理可选依赖
  ```python
  @dataclass
  class MyDeps:
      name: str       # 会被使用
      api_key: str    # 不会被使用
      http_client: httpx.AsyncClient  # 不会被使用
  ```

### 工具链调用
- `weather_agent.py`: 完整的工具链调用示例
  ```python
  # 第一个工具：获取经纬度
  @weather_agent.tool
  async def get_lat_lng(ctx: RunContext[Deps], location: str) -> dict:
      return {'lat': data[0]['lat'], 'lng': data[0]['lon']}

  # 第二个工具：获取天气
  @weather_agent.tool
  async def get_weather(ctx: RunContext[Deps], lat: float, lng: float) -> dict:
      return {'temperature': '21°C', 'description': 'Sunny'}
  ```

### 基础设施
- `async_model.py`: 模型初始化和配置
  ```python
  def get_gpt_model():
      return AzureOpenAI(...)

  def get_qwen_model():
      return QwenAI(...)
  ```

## 环境配置
```bash
# Azure OpenAI
export AZURE_OPENAI_ENDPOINT=xxx
export AZURE_OPENAI_API_KEY=xxx

# 天气 API（可选）
export WEATHER_API_KEY=xxx
export GEO_API_KEY=xxx
```

## 运行示例
```bash
# 基础示例
python system_prompt_static.py

# 工具链示例
python weather_agent.py
```

## 注意事项
1. 所有异步代码都需要在 async 函数中运行
2. 工具调用支持重试机制
3. 类型检查在运行时执行 
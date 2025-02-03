# GPT Function Caller

这是一个用于测试 GPT 函数调用功能的项目。项目采用简单直通的测试方式，无需复杂的测试框架。

## 架构设计

项目采用清晰的分层架构，将函数调用机制与具体函数实现分离：

### 核心架构
```
exam_funcall_simple/
├── function_caller/           # 所有内部实现
│   ├── __init__.py           # 只暴露 GPTFunctionCaller
│   ├── func_caller.py        # 主调用器实现
│   ├── func_handlers.py      # 函数调用处理
│   ├── func_utils.py         # 工具函数
│   ├── infra/               # 基础设施目录
│   │   ├── logger.py        # 日志功能
│   │   ├── base_caller.py   # 基础调用器
│   │   └── config.py        # 配置
│   └── core/                # 核心功能目录
│       └── text_caller.py   # 文本调用器
│
├── func_simple.py            # 简单函数实现
├── func_advanced.py          # 高级函数实现
├── test_*.py                # 所有测试文件
└── run_all_tests.py         # 测试运行器
```

### 设计理念
1. **关注点分离**
   - 核心调用机制封装在 `function_caller` 目录中
   - 具体函数实现在外部定义
   - 测试代码独立维护

2. **清晰的接口**
   - 对外只暴露 `GPTFunctionCaller` 类
   - 内部实现细节对外部不可见
   - 使用绝对导入保证依赖关系清晰

3. **易于扩展**
   - 添加新函数不需要修改核心代码
   - 基础设施代码集中管理
   - 测试用例可以独立添加

4. **使用示例**
```python
from exam_funcall_simple.function_caller import GPTFunctionCaller

# 创建调用器实例
caller = GPTFunctionCaller(functions, function_map)

# 使用调用器
response = caller.call_single_function("计算圆的面积")
```

## 测试设计理念

我们采用简单直通的测试方式，每个测试文件都是一个可以直接运行的Python脚本。这种方式的优点是：
1. 测试逻辑清晰直观
2. 无需学习测试框架
3. 运行结果一目了然
4. 便于调试和修改

### 单步测试文件
- 每个文件只允许一次LLM调用（即只能有一个`caller.call_with_functions`调用）
- 文件名清晰表明测试内容
- 测试代码简单直观
- 运行结果格式化输出
- 示例：`test_simple_time_query.py`, `test_advanced_single_weather.py`

### 多步骤测试文件
- 用于测试需要多次LLM调用的场景
- 文件名以`test_multisteps_`开头
- 允许多次调用`caller.call_with_functions`
- 每个步骤都有清晰的注释和说明
- 适用于：多轮对话、组合功能等
- 示例：`test_multisteps_mixed_functions.py`

## 功能说明

### 简单函数
- 时间查询：获取当前系统时间
- 圆面积计算：计算指定半径的圆的面积

### 高级函数
- 天气查询：获取指定城市的天气信息
- 货币转换：在不同货币之间进行金额转换
- 日程提醒：创建和管理日程提醒
- 餐厅搜索：根据条件搜索餐厅信息

## 运行测试

我们采用直接运行 Python 脚本的方式执行测试，不使用 unittest 或 pytest 等测试框架。这种方式简单直观，便于理解和调试。

### 运行单个测试
直接使用 Python 解释器运行测试文件：
```bash
# 运行单个测试文件
python3 exam_funcall_simple/test_simple_time_query.py
python3 exam_funcall_simple/test_advanced_single_weather.py
python3 exam_funcall_simple/test_multisteps_mixed_functions.py
```

### 运行所有测试
使用 `run_failed_tests.py` 运行所有失败的测试：
```bash
python3 exam_funcall_simple/run_failed_tests.py
```

### 测试结果查看
- 每个测试文件运行时会打印详细的执行过程
- 包括输入、API 调用、函数执行和输出结果
- 如果测试通过，程序正常退出
- 如果测试失败，会显示具体的错误信息和失败原因

### 调试测试
由于是直接运行 Python 脚本，可以：
- 使用 print 语句输出调试信息
- 在 IDE 中设置断点进行调试
- 修改代码后直接重新运行
- 不需要记忆或使用测试框架的特殊命令

## 配置说明

使用前需要在项目根目录创建 `.env` 文件：
```env
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_VERSION=2024-02-15-preview
```

## 测试规范

1. 文件命名规范
   - 单步测试：`test_simple_*.py`, `test_advanced_*.py`
   - 多步骤测试：`test_multisteps_*.py`

2. 代码规范
   - 单步测试文件只能包含一个`caller.call_with_functions`调用
   - 多步骤测试文件中的每个`call_with_functions`调用都要有明确的目的说明
   - 测试代码应该简单明了
   - 关键步骤要有注释说明
   - 使用utils_test中的函数格式化输出

3. 输出规范
   - 测试开始时显示测试名称
   - 清晰显示每个步骤的输入输出
   - 显示API调用的详细信息
   - 显示执行时间 
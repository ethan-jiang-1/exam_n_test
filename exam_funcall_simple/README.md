# GPT Function Caller

这是一个用于测试 GPT 函数调用功能的项目。项目采用简单直通的测试方式，无需复杂的测试框架。

## 项目结构

```
exam_funcall_simple/
├── gpt_caller.py          # GPT函数调用器核心实现
├── func_simple.py         # 简单函数实现
├── func_advanced.py       # 高级函数实现
├── config.py             # 配置文件
├── utils_test.py         # 测试辅助函数
├── test_simple_*.py      # 简单函数单步测试
├── test_advanced_*.py    # 高级函数单步测试
├── test_multisteps_*.py  # 多步骤测试场景
└── run_*.py             # 测试运行脚本
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

所有测试文件都可以直接运行：
```bash
# 运行单个测试
python test_simple_time_query.py
python test_advanced_single_weather.py
python test_multisteps_mixed_functions.py

# 运行所有测试
python run_all_tests.py
```

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
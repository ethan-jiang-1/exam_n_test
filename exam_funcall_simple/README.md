# GPT Function Caller

这是一个用于测试 GPT 函数调用功能的项目。项目包含简单函数和高级函数的实现及测试。

## 项目结构

```
exam_funcall_simple/
├── gpt_caller.py          # GPT函数调用器核心实现
├── func_simple.py         # 简单函数实现
├── func_advanced.py       # 高级函数实现
├── config.py             # 配置文件
├── test_simple_*.py      # 简单函数测试文件
├── test_advanced_*.py    # 高级函数测试文件
├── test_mixed_*.py       # 混合函数测试文件
└── run_*.py             # 测试运行器
```

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

1. 运行所有测试：
```bash
python -m exam_funcall_simple.run_all_tests
```

2. 只运行简单函数测试：
```bash
python -m exam_funcall_simple.run_simple_tests
```

3. 只运行高级函数测试：
```bash
python -m exam_funcall_simple.run_advanced_tests
```

4. 运行特定测试：
```bash
python -m exam_funcall_simple.test_simple_time_query
python -m exam_funcall_simple.test_advanced_weather
python -m exam_funcall_simple.test_mixed_functions
```

## 配置说明

使用前需要在项目根目录创建 `.env` 文件，包含以下配置：

```env
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_VERSION=2024-02-15-preview
```

## 注意事项

1. 所有测试文件都可以独立运行
2. 每个测试文件都包含多个测试场景
3. 日志输出采用彩色格式，便于查看
4. 所有函数都有详细的文档字符串 
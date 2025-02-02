from exam_funcall_simple.gpt_caller import GPTFunctionCaller
from exam_funcall_simple import func_simple
from exam_funcall_simple import func_advanced
from exam_funcall_simple.base_logger import print_test_header, print_user_input, print_request_data, print_api_response, print_execution_time, TestLogger
import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict
import math

@dataclass
class CirclePrice:
    """圆形桌子价格计算场景"""
    radius: float = 0.8
    amount: float = 230
    currency: tuple[str, str] = ("EUR", "欧元")
    target_currency: tuple[str, str] = ("CNY", "人民币")
    
    def __post_init__(self):
        self.prompt = (
            f"一张圆形餐桌半径是{self.radius}米，"
            f"这张桌子在欧洲的价格是{self.amount}{self.currency[1]}，"
            f"请帮我计算桌子的面积，并把价格转换成{self.target_currency[1]}。"
        )
        
        self.system_message = (
            "你是一个专业的助手，可以帮助用户进行各种计算。"
            "你可以使用calculate_circle_area计算圆形面积，"
            "使用currency_convert进行货币转换。"
            "请根据用户的需求调用合适的函数，并以清晰易懂的方式展示结果。"
        )

def test_singlestep_circle_price():
    """测试圆形桌子面积计算和价格转换"""
    print_test_header("测试圆形桌子面积计算和价格转换")
    
    # 初始化测试场景
    case = CirclePrice()
    print_user_input(case.prompt)
    
    # 设置函数调用
    caller = GPTFunctionCaller(
        functions=[
            func_simple.FUNCTION_DESCRIPTIONS[1],  # calculate_circle_area
            func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS[1]  # currency_convert
        ],
        function_map={
            "calculate_circle_area": func_simple.calculate_circle_area,
            "currency_convert": func_advanced.currency_convert
        }
    )
    
    # 执行调用
    response = caller.call_with_functions(case.prompt, system_message=case.system_message)
    print_request_data(caller.last_request)
    print_api_response(response.model_dump())
    print_execution_time(caller.execution_time)
    
    # 处理结果
    logger = TestLogger()
    if not (response.choices and response.choices[0].message.tool_calls):
        logger.print_error("函数调用失败")
        return
        
    # 执行函数调用并收集结果
    results = {}
    function_map = {
        "calculate_circle_area": func_simple.calculate_circle_area,
        "currency_convert": func_advanced.currency_convert
    }
    
    for tool_call in response.choices[0].message.tool_calls:
        results[tool_call.function.name] = function_map[tool_call.function.name](
            **json.loads(tool_call.function.arguments)
        )
    
    # 让模型生成最终结果展示
    if len(results) == 2:  # 两个函数都调用成功
        result_prompt = (
            f"请将计算结果整理成易于理解的格式：\n"
            f"1. 圆形面积计算结果：{results['calculate_circle_area']}\n"
            f"2. 货币转换结果：{json.dumps(results['currency_convert'], ensure_ascii=False)}"
        )
        
        format_response = caller.call_with_functions(result_prompt)
        if format_response.choices and format_response.choices[0].message.content:
            logger.print_panel("最终结果", format_response.choices[0].message.content, "green")
            logger.print_success("所有计算已完成")
        else:
            logger.print_error("结果格式化失败")
    else:
        logger.print_error("无法获取完整的计算结果")

def calculate_circle_area(radius: float) -> float:
    """计算圆形面积"""
    return math.pi * radius ** 2

def currency_convert(amount: float, from_currency: str, to_currency: str) -> Dict[str, Any]:
    """模拟货币转换功能"""
    rates = {
        "EUR": {"CNY": 7.874},
        "CNY": {"EUR": 1/7.874}
    }
    
    rate = rates[from_currency][to_currency]
    converted_amount = amount * rate
    
    return {
        "original_amount": amount,
        "converted_amount": converted_amount,
        "from_currency": from_currency,
        "to_currency": to_currency,
        "rate": rate,
        "timestamp": datetime.now().isoformat()
    }

def run_test() -> None:
    """运行圆形桌子面积计算和价格转换测试"""
    
    # 1. 准备测试数据
    radius = 0.8  # 半径（米）
    price_eur = 230  # 价格（欧元）
    
    # 2. 调用函数计算
    area = calculate_circle_area(radius=radius)
    conversion = currency_convert(
        amount=price_eur,
        from_currency="EUR",
        to_currency="CNY"
    )
    
    # 3. 格式化结果
    result = format_results(area, conversion)
    
    # 4. 输出结果
    print("\n" + "─" * 50 + " 测试结果 " + "─" * 50 + "\n")
    print(result)
    print("\n" + "─" * 120 + "\n")

def format_results(area: float, conversion: Dict[str, Any]) -> str:
    """格式化计算结果为易读的文本"""
    timestamp = datetime.fromisoformat(conversion['timestamp'].replace('Z', '+00:00'))
    
    return f"""计算结果：

1. 圆形桌子面积
   - 面积：{area:.2f} 平方米

2. 价格转换
   - 原始价格：{conversion['original_amount']} {conversion['from_currency']}
   - 转换价格：{conversion['converted_amount']:.2f} {conversion['to_currency']}
   - 使用汇率：1 {conversion['from_currency']} = {conversion['rate']:.3f} {conversion['to_currency']}
   - 计算时间：{timestamp.strftime('%Y年%m月%d日 %H:%M:%S')}"""

if __name__ == "__main__":
    test_singlestep_circle_price()
    run_test() 
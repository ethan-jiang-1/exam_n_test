from exam_funcall_simple.gpt_caller import GPTFunctionCaller
from exam_funcall_simple import func_simple
from exam_funcall_simple import func_advanced
from exam_funcall_simple.base_logger import print_test_header, print_user_input, print_request_data, print_api_response, print_execution_time, TestLogger
import json
from dataclasses import dataclass

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
            f"这是一个多函数调用测试。请在一次调用中完成以下任务：\n"
            f"1) 使用calculate_circle_area计算半径为{self.radius}米的圆形桌子面积\n"
            f"2) 使用currency_convert将{self.amount}{self.currency[0]}转换为{self.target_currency[0]}"
        )
    
    def format_result(self, area: float, price: dict) -> str:
        return (
            f"计算结果：\n"
            f"1. 圆形餐桌面积：{area:.2f} 平方米\n"
            f"2. 价格转换：{price['original_amount']} {self.currency[1]} = "
            f"{price['converted_amount']:.2f} {self.target_currency[1]}\n"
            f"   (使用汇率：1 {self.currency[1]} = {price['rate']:.3f} {self.target_currency[1]})"
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
        
    results = {}
    function_map = {
        "calculate_circle_area": func_simple.calculate_circle_area,
        "currency_convert": func_advanced.currency_convert
    }
    
    for tool_call in response.choices[0].message.tool_calls:
        results[tool_call.function.name] = function_map[tool_call.function.name](
            **json.loads(tool_call.function.arguments)
        )
    
    if len(results) == 2:  # 两个函数都调用成功
        logger.print_panel(
            "最终结果",
            case.format_result(
                results["calculate_circle_area"],
                results["currency_convert"]
            ),
            "green"
        )
        logger.print_success("所有计算已完成")
    else:
        logger.print_error("无法获取完整的计算结果")

if __name__ == "__main__":
    test_singlestep_circle_price() 
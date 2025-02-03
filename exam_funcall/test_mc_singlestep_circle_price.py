from exam_funcall.func_simple import calculate_circle_area, FUNCTION_DESCRIPTIONS as functions
from exam_funcall.function_caller import GPTFunctionCaller
from exam_funcall import func_advanced
from exam_funcall.function_caller.infra import (
    print_test_header,
    print_user_input,
    print_request_data,
    print_api_response,
    print_execution_time
)
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
            "你是一位精通数学和金融计算的专业助手。"
            "用户的问题涉及几何计算和货币转换，"
            "请思考如何高效地完成这些计算并给出清晰的解释。"
            "记住，一个专业的回答应该简洁、准确、一步到位。"
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
            functions[1],  # calculate_circle_area
            func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS[1]  # currency_convert
        ],
        function_map={
            "calculate_circle_area": calculate_circle_area,
            "currency_convert": func_advanced.currency_convert
        }
    )
    
    # 执行调用
    response = caller.call_single_function(
        case.prompt,
        system_message=case.system_message
    )
    
    print_request_data(caller.last_request)
    print_api_response(response.model_dump())
    print_execution_time(caller.execution_time)
    
    # 验证结果
    assert response.choices[0].message.tool_calls is not None, "没有函数调用"
    tool_calls = response.choices[0].message.tool_calls
    assert len(tool_calls) == 2, "应该有2个函数调用"
    
    # 验证函数调用顺序和参数
    assert tool_calls[0].function.name == "calculate_circle_area", "第一个调用应该是calculate_circle_area"
    assert tool_calls[1].function.name == "currency_convert", "第二个调用应该是currency_convert"
    
    # 验证参数
    import json
    circle_call = json.loads(tool_calls[0].function.arguments)
    currency_call = json.loads(tool_calls[1].function.arguments)
    
    assert circle_call["radius"] == case.radius, "圆形面积计算的半径不正确"
    assert currency_call["amount"] == case.amount, "货币转换的金额不正确"
    assert currency_call["from_currency"] == case.currency[0], "源货币不正确"
    assert currency_call["to_currency"] == case.target_currency[0], "目标货币不正确"

if __name__ == "__main__":
    test_singlestep_circle_price() 
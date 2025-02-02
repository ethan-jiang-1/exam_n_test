from exam_funcall_simple.gpt_caller import GPTFunctionCaller
from exam_funcall_simple import func_simple
from exam_funcall_simple import func_advanced
from exam_funcall_simple.base_logger import print_test_header, print_user_input, print_request_data, print_api_response, print_execution_time, TestLogger
import json
from string import Template

# 模板定义
TEMPLATES = {
    "system_message": Template("""
这是一个多函数调用测试。请在一次调用中完成以下任务：
1) 使用calculate_circle_area计算半径为${radius}米的圆形桌子面积
2) 使用currency_convert将${amount}${from_currency}转换为${to_currency}
""".strip()),

    "result_message": Template("""计算结果：
1. 圆形餐桌面积：${area} 平方米
2. 价格转换：${original_amount} ${from_currency} = ${converted_amount} ${to_currency}
   (使用汇率：1 ${from_currency} = ${rate} ${to_currency})""")
}

def test_singlestep_circle_price():
    """测试圆形桌子面积计算和价格转换"""
    print_test_header("测试圆形桌子面积计算和价格转换")
    
    # 测试参数
    test_params = {
        "radius": 0.8,
        "amount": 230,
        "from_currency": "EUR",
        "to_currency": "CNY",
        "from_currency_name": "欧元",
        "to_currency_name": "人民币"
    }
    
    # 初始化函数调用器
    function_map = {
        "calculate_circle_area": func_simple.calculate_circle_area,
        "currency_convert": func_advanced.currency_convert
    }
    
    caller = GPTFunctionCaller(
        functions=[
            func_simple.FUNCTION_DESCRIPTIONS[1],  # calculate_circle_area
            func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS[1]  # currency_convert
        ],
        function_map=function_map
    )
    
    # 测试输入
    user_input = f"一张圆形餐桌半径是{test_params['radius']}米，这张桌子在欧洲的价格是{test_params['amount']}{test_params['from_currency_name']}，请帮我计算桌子的面积，并把价格转换成{test_params['to_currency_name']}。"
    print_user_input(user_input)
    
    # 生成系统消息
    system_message = TEMPLATES["system_message"].substitute(
        radius=test_params["radius"],
        amount=test_params["amount"],
        from_currency=test_params["from_currency"],
        to_currency=test_params["to_currency"]
    )
    
    # 执行调用
    response = caller.call_with_functions(
        user_input,
        system_message=system_message
    )
    
    # 输出结果
    print_request_data(caller.last_request)
    print_api_response(response.model_dump())
    print_execution_time(caller.execution_time)
    
    # 合成并展示最终结果
    logger = TestLogger()
    
    # 从响应中提取函数调用结果
    if response.choices and response.choices[0].message.tool_calls:
        area_result = None
        price_result = None
        
        for tool_call in response.choices[0].message.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)
            
            if func_name == "calculate_circle_area":
                area_result = function_map[func_name](**func_args)
            elif func_name == "currency_convert":
                price_result = function_map[func_name](**func_args)
        
        if area_result is not None and price_result is not None:
            # 使用模板格式化结果消息
            result_message = TEMPLATES["result_message"].substitute(
                area=f"{area_result:.2f}",
                original_amount=price_result["original_amount"],
                from_currency=test_params["from_currency_name"],
                converted_amount=f"{price_result['converted_amount']:.2f}",
                to_currency=test_params["to_currency_name"],
                rate=f"{price_result['rate']:.3f}"
            )
            logger.print_panel("最终结果", result_message, "green")
            logger.print_success("所有计算已完成")
        else:
            logger.print_error("无法获取完整的计算结果")
    else:
        logger.print_error("函数调用失败")

if __name__ == "__main__":
    test_singlestep_circle_price() 
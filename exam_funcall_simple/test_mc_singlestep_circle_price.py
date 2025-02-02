from exam_funcall_simple.gpt_caller import GPTFunctionCaller
from exam_funcall_simple import func_simple
from exam_funcall_simple import func_advanced
from exam_funcall_simple.base_logger import print_test_header, print_user_input, print_request_data, print_api_response, print_execution_time, TestLogger
import json

def test_singlestep_circle_price():
    """测试圆形桌子面积计算和价格转换"""
    print_test_header("测试圆形桌子面积计算和价格转换")
    
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
    user_input = "一张圆形餐桌半径是0.8米，这张桌子在欧洲的价格是230欧元，请帮我计算桌子的面积，并把价格转换成人民币。"
    print_user_input(user_input)
    
    # 执行调用
    response = caller.call_with_functions(
        user_input,
        system_message="这是一个多函数调用测试。请在一次调用中完成以下任务：1) 使用calculate_circle_area计算圆形桌子的面积；2) 使用currency_convert将230欧元转换为人民币"
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
            # 格式化结果消息
            result_message = (
                f"计算结果：\n"
                f"1. 圆形餐桌面积：{area_result:.2f}平方米\n"
                f"2. 价格转换：{price_result['original_amount']}欧元 = {price_result['converted_amount']}人民币\n"
                f"   (使用汇率：1欧元 = {price_result['rate']}人民币)"
            )
            logger.print_panel("最终结果", result_message, "green")
            logger.print_success("所有计算已完成")
        else:
            logger.print_error("无法获取完整的计算结果")
    else:
        logger.print_error("函数调用失败")

if __name__ == "__main__":
    test_singlestep_circle_price() 
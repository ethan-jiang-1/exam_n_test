from exam_funcall_simple.gpt_caller import GPTFunctionCaller
from exam_funcall_simple import func_simple
from exam_funcall_simple import func_advanced
from exam_funcall_simple.utils_test import print_test_header, print_user_input, print_request_data, print_api_response, print_execution_time

def test_singlestep_circle_price():
    """测试圆形桌子面积计算和价格转换"""
    print_test_header("测试圆形桌子面积计算和价格转换")
    
    # 初始化函数调用器
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
    
    # 测试输入
    user_input = "一张圆形餐桌半径是0.8米，这张桌子在欧洲的价格是230欧元，请帮我计算桌子的面积，并把价格转换成人民币。"
    print_user_input(user_input)
    
    # 执行调用
    caller.call_with_functions(
        user_input,
        system_message="这是一个多函数调用测试。请在一次调用中完成以下任务：1) 使用calculate_circle_area计算圆形桌子的面积；2) 使用currency_convert将230欧元转换为人民币"
    )
    
    # 输出结果
    print_request_data(caller.last_request)
    print_api_response(caller.raw_response)
    print_execution_time(caller.execution_time)

if __name__ == "__main__":
    test_singlestep_circle_price() 
from exam_funcall_simple.gpt_caller import GPTFunctionCaller
from exam_funcall_simple import func_simple
from exam_funcall_simple import func_advanced
from exam_funcall_simple.utils_test import print_test_header, print_user_input, print_request_data, print_api_response, print_execution_time

def test_singlestep_circle_price():
    """测试在单个步骤中计算圆形面积和价格转换的场景"""
    print_test_header("测试圆桌面积和价格计算")
    
    # 初始化函数调用器，只包含需要的函数
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
    user_input = "一个半径为5米的圆形桌子价值500欧元，请计算它的面积和对应的人民币价格"
    print_user_input(user_input)
    
    # 在一次调用中请求多个函数执行
    caller.call_with_multiple_functions(
        user_input,
        system_message="这是一个多函数调用测试。请在一次调用中完成以下任务：1) 使用calculate_circle_area计算半径5米的圆的面积；2) 使用currency_convert将500欧元转换为人民币"
    )
    
    print_request_data(caller.last_request)
    print_api_response(caller.raw_response)
    print_execution_time(caller.execution_time)

if __name__ == "__main__":
    test_singlestep_circle_price() 
#import json
from exam_funcall_simple.gpt_caller import GPTFunctionCaller
from exam_funcall_simple import func_advanced
from exam_funcall_simple.test_utils import print_test_header, print_user_input, print_request_data, print_api_response, print_function_result, print_execution_time

def test_currency_conversion():
    """测试货币转换功能"""
    print_test_header("货币转换功能")
    
    caller = GPTFunctionCaller(
        functions=[func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS[1]],  # 只使用货币转换函数
        function_map={
            "currency_convert": func_advanced.currency_convert
        }
    )
    
    # 测试美元到人民币转换
    print("\n>>> 测试美元到人民币转换\n")
    user_input = "把100美元换算成人民币"
    print_user_input(user_input)
    
    response = caller.call_with_functions(user_input)
    
    print_request_data(caller.last_request)
    print_api_response(caller.raw_response)
    
    if response.choices and response.choices[0].message.function_call:
        print_function_result(response.choices[0].message.function_call)
    
    print_execution_time(caller.execution_time)
    
    # 测试欧元到日元转换
    print("\n>>> 测试欧元到日元转换\n")
    user_input = "将50欧元换成日元"
    print_user_input(user_input)
    
    response = caller.call_with_functions(user_input)
    
    print_request_data(caller.last_request)
    print_api_response(caller.raw_response)
    
    if response.choices and response.choices[0].message.function_call:
        print_function_result(response.choices[0].message.function_call)
    
    print_execution_time(caller.execution_time)
    
    print("\n✓ 货币转换测试完成\n")

if __name__ == "__main__":
    test_currency_conversion() 
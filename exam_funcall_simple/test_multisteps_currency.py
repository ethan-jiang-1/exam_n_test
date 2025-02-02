from exam_funcall_simple.gpt_caller import GPTFunctionCaller
from exam_funcall_simple import func_advanced
from exam_funcall_simple.utils_test import print_test_header, print_user_input, print_request_data, print_api_response, print_function_result, print_execution_time

def test_multisteps_currency():
    """测试货币转换的多步骤场景"""
    print_test_header("测试货币转换的多步骤场景")
    
    # 初始化函数调用器
    caller = GPTFunctionCaller(
        functions=[func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS[1]],  # 只使用货币转换函数
        function_map={"currency_convert": func_advanced.currency_convert}
    )
    
    # 场景1：美元到人民币转换
    print_test_header("场景1：美元到人民币转换", level=2)
    user_input = "把100美元换算成人民币"
    print_user_input(user_input)
    
    response = caller.call_with_functions(
        user_input,
        system_message="请使用currency_convert函数将100美元转换为人民币。"
    )
    
    print_request_data(caller.last_request)
    print_api_response(caller.raw_response)
    
    if response.choices and response.choices[0].message and response.choices[0].message.function_call:
        print_function_result(response.choices[0].message.function_call)
    
    print_execution_time(caller.last_execution_time)
    
    # 场景2：欧元到日元转换
    print_test_header("场景2：欧元到日元转换", level=2)
    user_input = "将50欧元换成日元"
    print_user_input(user_input)
    
    response = caller.call_with_functions(
        user_input,
        system_message="请使用currency_convert函数将50欧元转换为日元。"
    )
    
    print_request_data(caller.last_request)
    print_api_response(caller.raw_response)
    
    if response.choices and response.choices[0].message and response.choices[0].message.function_call:
        print_function_result(response.choices[0].message.function_call)
    
    print_execution_time(caller.last_execution_time)

if __name__ == "__main__":
    test_multisteps_currency() 
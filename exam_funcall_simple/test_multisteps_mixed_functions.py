from exam_funcall_simple.gpt_caller import GPTFunctionCaller
from exam_funcall_simple import func_simple
from exam_funcall_simple import func_advanced
from exam_funcall_simple.base_utils_test import print_test_header, print_user_input, print_request_data, print_api_response, print_function_result, print_execution_time

def test_multisteps_mixed_functions():
    """测试混合函数的多步骤调用场景"""
    print_test_header("测试混合函数的多步骤调用")
    
    # 初始化混合函数调用器
    caller = GPTFunctionCaller(
        functions=func_simple.FUNCTION_DESCRIPTIONS + func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS,
        function_map={
            **{
                "get_current_time": func_simple.get_current_time,
                "calculate_circle_area": func_simple.calculate_circle_area
            },
            **{
                "get_weather": func_advanced.get_weather,
                "currency_convert": func_advanced.currency_convert,
                "schedule_reminder": func_advanced.schedule_reminder,
                "search_restaurants": func_advanced.search_restaurants
            }
        }
    )
    
    # 场景1：时间和天气多步骤查询
    print_test_header("场景1：时间和天气多步骤查询")
    user_input = "现在几点了？顺便帮我查查北京的天气"
    print_user_input(user_input)
    
    # 步骤1.1：获取当前时间
    print_test_header("步骤1.1：获取当前时间")
    response = caller.call_with_functions(
        user_input,
        system_message="请使用get_current_time函数获取当前时间。不要使用其他函数。"
    )
    
    print_request_data(caller.last_request)
    print_api_response(caller.raw_response)
    
    if response.choices and response.choices[0].message and response.choices[0].message.function_call:
        print_function_result(response.choices[0].message.function_call)
    
    print_execution_time(caller.execution_time)
    
    # 步骤1.2：查询北京天气
    print_test_header("步骤1.2：查询北京天气")
    response = caller.call_with_functions(
        user_input,
        system_message="请使用get_weather函数查询北京的天气。不要使用其他函数。"
    )
    
    print_request_data(caller.last_request)
    print_api_response(caller.raw_response)
    
    if response.choices and response.choices[0].message and response.choices[0].message.function_call:
        print_function_result(response.choices[0].message.function_call)
    
    print_execution_time(caller.execution_time)
    
    # 场景2：圆面积和货币转换多步骤查询
    print_test_header("场景2：圆面积和货币转换多步骤查询")
    user_input = "一个半径为10厘米的圆形桌子价值100美元，请告诉我它的面积和人民币价格"
    print_user_input(user_input)
    
    # 步骤2.1：计算圆面积
    print_test_header("步骤2.1：计算圆面积")
    response = caller.call_with_functions(
        user_input,
        system_message="请使用calculate_circle_area函数计算半径为10的圆的面积。不要使用其他函数。"
    )
    
    print_request_data(caller.last_request)
    print_api_response(caller.raw_response)
    
    if response.choices and response.choices[0].message and response.choices[0].message.function_call:
        print_function_result(response.choices[0].message.function_call)
    
    print_execution_time(caller.execution_time)
    
    # 步骤2.2：进行货币转换
    print_test_header("步骤2.2：进行货币转换")
    response = caller.call_with_functions(
        user_input,
        system_message="请使用currency_convert函数将100美元转换为人民币。不要使用其他函数。"
    )
    
    print_request_data(caller.last_request)
    print_api_response(caller.raw_response)
    
    if response.choices and response.choices[0].message and response.choices[0].message.function_call:
        print_function_result(response.choices[0].message.function_call)
    
    print_execution_time(caller.execution_time)

if __name__ == "__main__":
    test_multisteps_mixed_functions() 
from exam_funcall_simple.gpt_caller import GPTFunctionCaller
from exam_funcall_simple import func_simple
from exam_funcall_simple import func_advanced
from exam_funcall_simple.test_utils import print_test_header, print_user_input, print_request_data, print_api_response, print_function_result, print_execution_time

def test_mixed_functions():
    """测试混合函数集"""
    print_test_header("测试混合函数集")
    
    # 合并所有函数
    all_functions = func_simple.FUNCTION_DESCRIPTIONS + func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS
    all_function_map = {
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
    
    # 初始化混合函数调用器
    caller = GPTFunctionCaller(
        functions=all_functions,
        function_map=all_function_map
    )
    
    # 测试混合场景 - 时间和天气
    print_test_header("测试时间和天气混合查询", level=2)
    user_input = "现在几点了？顺便帮我查查北京的天气"
    print_user_input(user_input)
    
    response = caller.call_with_functions(
        user_input,
        system_message="请尽可能多地调用相关函数来回答问题"
    )
    
    print_request_data(caller.last_request)
    print_api_response(response)
    print_function_result(caller.last_function_calls)
    print_execution_time(caller.last_execution_time)
    
    # 测试混合场景 - 圆面积和货币转换
    print_test_header("测试圆面积和货币转换混合查询", level=2)
    user_input = "一个半径为10厘米的圆形桌子价值100美元，请告诉我它的面积和人民币价格"
    print_user_input(user_input)
    
    response = caller.call_with_functions(
        user_input,
        system_message="请依次计算面积和价格"
    )
    
    print_request_data(caller.last_request)
    print_api_response(response)
    print_function_result(caller.last_function_calls)
    print_execution_time(caller.last_execution_time)

if __name__ == "__main__":
    test_mixed_functions() 
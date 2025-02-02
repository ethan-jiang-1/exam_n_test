from exam_funcall_simple.gpt_caller import GPTFunctionCaller
from exam_funcall_simple import func_advanced
from exam_funcall_simple.test_utils import print_test_header, print_user_input, print_request_data, print_api_response, print_function_result, print_execution_time

def test_weather_query():
    """测试天气查询功能"""
    print_test_header("天气查询功能")
    
    caller = GPTFunctionCaller(
        functions=[func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS[0]],  # 只使用天气相关函数
        function_map={
            "get_weather": func_advanced.get_weather
        }
    )
    
    # 测试基本天气查询
    print("\n>>> 测试基本天气查询\n")
    user_input = "北京今天天气怎么样？"
    print_user_input(user_input)
    
    response = caller.call_with_functions(user_input)
    
    print_request_data(caller.last_request)
    print_api_response(caller.raw_response)
    
    if response.choices and response.choices[0].message.function_call:
        print_function_result(response.choices[0].message.function_call)
    
    print_execution_time(caller.execution_time)
    
    # 测试带国家代码的查询
    print("\n>>> 测试带国家代码的查询\n")
    user_input = "查询东京(JP)的天气"
    print_user_input(user_input)
    
    response = caller.call_with_functions(user_input)
    
    print_request_data(caller.last_request)
    print_api_response(caller.raw_response)
    
    if response.choices and response.choices[0].message.function_call:
        print_function_result(response.choices[0].message.function_call)
    
    print_execution_time(caller.execution_time)
    
    print("\n✓ 天气查询测试完成\n")

if __name__ == "__main__":
    test_weather_query() 
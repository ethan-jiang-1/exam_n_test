from exam_funcall_simple.gpt_caller import GPTFunctionCaller
from exam_funcall_simple import func_simple
from exam_funcall_simple.base_logger import print_test_header, print_user_input, print_request_data, print_api_response, print_function_result, print_execution_time

def test_time_query():
    """测试场景：基本时间查询功能"""
    print_test_header("时间查询功能测试")
    
    # 初始化函数调用器
    caller = GPTFunctionCaller(
        functions=func_simple.FUNCTION_DESCRIPTIONS,
        function_map={
            "get_current_time": func_simple.get_current_time,
            "calculate_circle_area": func_simple.calculate_circle_area
        }
    )
    
    # 测试输入
    user_input = "现在几点了？"
    print_user_input(user_input)
    
    # 执行调用
    response = caller.call_with_functions(user_input)
    
    # 输出结果
    print_request_data(caller.last_request)
    print_api_response(caller.raw_response)
    
    if response.choices and response.choices[0].message.function_call:
        print_function_result(response.choices[0].message.function_call)
    
    print_execution_time(caller.execution_time)

if __name__ == "__main__":
    test_time_query() 
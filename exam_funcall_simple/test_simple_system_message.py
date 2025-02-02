from exam_funcall_simple.gpt_caller import GPTFunctionCaller
from exam_funcall_simple import func_simple
from exam_funcall_simple.utils_test import print_test_header, print_user_input, print_request_data, print_api_response, print_function_result, print_execution_time, print_system_message

def test_with_system_message():
    """测试带系统消息的调用"""
    print_test_header("带系统消息的调用")
    
    system_message = "请用详细的步骤解释计算过程"
    print_system_message(system_message)
    
    user_input = "计算一个半径为10厘米的圆的面积"
    print_user_input(user_input)
    
    caller = GPTFunctionCaller(
        functions=func_simple.FUNCTION_DESCRIPTIONS,
        function_map={
            "get_current_time": func_simple.get_current_time,
            "calculate_circle_area": func_simple.calculate_circle_area
        }
    )
    
    response = caller.call_with_functions(
        user_input,
        system_message=system_message
    )
    
    print_request_data(caller.last_request)
    print_api_response(caller.raw_response)
    
    if response.choices and response.choices[0].message.function_call:
        print_function_result(response.choices[0].message.function_call)
    
    print_execution_time(caller.execution_time)
    print("\n✓ 带系统消息的调用测试完成\n")

if __name__ == "__main__":
    test_with_system_message() 
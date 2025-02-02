from exam_funcall_simple.gpt_caller import GPTFunctionCaller
from exam_funcall_simple import func_simple
from exam_funcall_simple.test_utils import print_test_header, print_user_input, print_request_data, print_api_response, print_function_result, print_execution_time, print_conversation_history

def test_with_history():
    """测试带历史记录的对话"""
    print_test_header("带历史记录的对话")
    
    history = [
        {"role": "user", "content": "我想计算一个圆的面积"},
        {"role": "assistant", "content": "好的，请告诉我圆的半径"},
    ]
    print_conversation_history(history)
    
    user_input = "半径是7厘米"
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
        history=history
    )
    
    print_request_data(caller.last_request)
    print_api_response(caller.raw_response)
    
    if response.choices and response.choices[0].message.function_call:
        print_function_result(response.choices[0].message.function_call)
    
    print_execution_time(caller.execution_time)
    print("\n✓ 带历史记录的对话测试完成\n")

if __name__ == "__main__":
    test_with_history() 
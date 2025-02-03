from exam_funcall.func_simple import get_current_time, calculate_circle_area, FUNCTION_DESCRIPTIONS as functions
from exam_funcall.function_caller import GPTFunctionCaller
from exam_funcall.function_caller.infra import (
    print_test_header,
    print_user_input,
    #print_system_message,
    print_request_data,
    print_api_response,
    print_function_result,
    print_execution_time,
    print_conversation_history,
    #log_function_call,
    #TestLogger
)

def test_with_history():
    """测试场景：基于对话历史的圆面积计算"""
    print_test_header("带对话历史的圆面积计算测试")
    
    # 初始化函数调用器
    caller = GPTFunctionCaller(
        functions=functions,
        function_map={
            "get_current_time": get_current_time,
            "calculate_circle_area": calculate_circle_area
        }
    )
    
    # 测试输入
    history = [
        {"role": "user", "content": "我想计算一个圆的面积"},
        {"role": "assistant", "content": "好的，请告诉我圆的半径"},
    ]
    print_conversation_history(history)
    
    user_input = "半径是7厘米"
    print_user_input(user_input)
    
    # 执行调用
    response = caller.call_single_function(
        user_input,
        history=history
    )
    
    # 输出结果
    print_request_data(caller.last_request)
    print_api_response(caller.raw_response)
    
    if response.choices and response.choices[0].message.function_call:
        print_function_result(response.choices[0].message.function_call)
    
    print_execution_time(caller.execution_time)

if __name__ == "__main__":
    test_with_history() 
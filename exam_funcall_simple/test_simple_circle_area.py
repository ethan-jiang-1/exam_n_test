from exam_funcall_simple.func_simple import get_current_time, calculate_circle_area, FUNCTION_DESCRIPTIONS as functions
from exam_funcall_simple.function_caller import GPTFunctionCaller
from exam_funcall_simple.function_caller.infra import (
    print_test_header,
    print_user_input,
    print_request_data,
    print_api_response,
    print_function_result,
    print_execution_time
)

def test_circle_area():
    """测试场景：计算指定半径圆的面积"""
    print_test_header("圆面积计算功能测试")
    
    # 初始化函数调用器
    caller = GPTFunctionCaller(
        functions=functions,
        function_map={
            "get_current_time": get_current_time,
            "calculate_circle_area": calculate_circle_area
        }
    )
    
    # 测试输入
    user_input = "计算半径为5的圆的面积"
    print_user_input(user_input)
    
    # 执行调用
    response = caller.call_single_function(user_input)
    
    # 输出结果
    print_request_data(caller.last_request)
    print_api_response(caller.raw_response)
    
    if response.choices and response.choices[0].message.function_call:
        print_function_result(response.choices[0].message.function_call)
    
    print_execution_time(caller.execution_time)

if __name__ == "__main__":
    test_circle_area() 
from exam_funcall_simple.function_caller import GPTFunctionCaller
from exam_funcall_simple.func_simple import get_current_time
from exam_funcall_simple.function_caller.infra import (
    print_test_header,
    print_user_input,
    print_request_data,
    print_api_response,
    print_function_result,
    print_execution_time
)

def test_time_query():
    """测试时间查询功能"""
    print_test_header("测试时间查询功能")
    
    # 准备函数
    functions = [
        {
            "name": "get_current_time",
            "description": "获取当前系统时间",
            "parameters": {"type": "object", "properties": {}}
        }
    ]
    function_map = {
        "get_current_time": get_current_time
    }
    
    # 创建调用器
    caller = GPTFunctionCaller(functions, function_map)
    
    # 执行调用
    user_message = "现在几点了？"
    print_user_input(user_message)
    
    response = caller.call_single_function(user_message)
    
    # 输出结果
    print_request_data(caller.last_request)
    print_api_response(caller.raw_response)
    if hasattr(response, 'function_results'):
        for result in response.function_results:
            print_function_result(result)
    print_execution_time(caller.execution_time)

if __name__ == "__main__":
    test_time_query() 
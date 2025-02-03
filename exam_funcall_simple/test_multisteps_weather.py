from exam_funcall_simple.function_caller import GPTFunctionCaller
from exam_funcall_simple import func_advanced
from exam_funcall_simple.function_caller.infra import (
    print_test_header,
    print_user_input,
    print_system_message,
    print_request_data,
    print_api_response,
    print_function_result,
    print_execution_time,
    print_conversation_history,
    log_function_call,
    TestLogger
)

def test_multisteps_weather():
    """测试天气查询的多步骤场景"""
    print_test_header("测试天气查询的多步骤场景")
    
    # 初始化函数调用器
    caller = GPTFunctionCaller(
        functions=[func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS[0]],  # 只使用天气查询函数
        function_map={"get_weather": func_advanced.get_weather}
    )
    
    # 场景1：查询国内城市天气
    print_test_header("场景1：查询国内城市天气")
    user_input = "北京今天天气怎么样？"
    print_user_input(user_input)
    
    response = caller.call_single_function(
        user_input,
        system_message="请使用get_weather函数查询北京的天气。"
    )
    
    print_request_data(caller.last_request)
    print_api_response(caller.raw_response)
    
    if response.choices and response.choices[0].message and response.choices[0].message.function_call:
        print_function_result(response.choices[0].message.function_call)
    
    print_execution_time(caller.execution_time)
    
    # 场景2：查询国外城市天气
    print_test_header("场景2：查询国外城市天气")
    user_input = "查询东京(JP)的天气"
    print_user_input(user_input)
    
    response = caller.call_single_function(
        user_input,
        system_message="请使用get_weather函数查询东京的天气，注意使用正确的国家代码。"
    )
    
    print_request_data(caller.last_request)
    print_api_response(caller.raw_response)
    
    if response.choices and response.choices[0].message and response.choices[0].message.function_call:
        print_function_result(response.choices[0].message.function_call)
    
    print_execution_time(caller.execution_time)

if __name__ == "__main__":
    test_multisteps_weather() 
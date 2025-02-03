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

def test_advanced_single_reminder():
    """测试场景：创建基本的团队会议提醒"""
    print_test_header("日程提醒功能测试")
    
    # 初始化函数调用器
    caller = GPTFunctionCaller(
        functions=[func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS[2]],  # 只使用日程提醒函数
        function_map={"schedule_reminder": func_advanced.schedule_reminder}
    )
    
    # 测试输入
    system_message = "请直接使用schedule_reminder函数创建提醒，对于未提供的参数使用默认值。不要询问更多信息。"
    print_system_message(system_message)
    
    user_input = "帮我设置一个2小时后的团队会议提醒"
    print_user_input(user_input)
    
    # 执行调用
    response = caller.call_single_function(
        user_input,
        system_message=system_message
    )
    
    # 输出结果
    print_request_data(caller.last_request)
    print_api_response(caller.raw_response)
    
    if response.choices and response.choices[0].message and response.choices[0].message.function_call:
        print_function_result(response.choices[0].message.function_call)
    
    # 输出函数执行结果
    if hasattr(response, 'function_results'):
        for result in response.function_results:
            print("\n函数执行结果:")
            print(f"函数名称: {result['name']}")
            print(f"执行结果: {result['result']}")
    
    print_execution_time(caller.execution_time)

if __name__ == "__main__":
    test_advanced_single_reminder() 
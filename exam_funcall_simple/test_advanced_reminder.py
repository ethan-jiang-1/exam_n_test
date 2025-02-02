from exam_funcall_simple.gpt_caller import GPTFunctionCaller
from exam_funcall_simple import func_advanced
from exam_funcall_simple.utils_test import print_test_header, print_user_input, print_request_data, print_api_response, print_function_result, print_execution_time, print_system_message

def test_reminder():
    """测试日程提醒功能"""
    print_test_header("日程提醒功能")
    
    caller = GPTFunctionCaller(
        functions=[func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS[2]],  # 只使用日程提醒函数
        function_map={
            "schedule_reminder": func_advanced.schedule_reminder
        }
    )
    
    # 测试基本提醒设置
    print("\n>>> 测试基本提醒设置\n")
    system_message = "当前时间是2024年2月2日"
    print_system_message(system_message)
    
    user_input = "帮我设置一个明天下午3点的团队会议提醒"
    print_user_input(user_input)
    
    response = caller.call_with_functions(
        user_input,
        system_message=system_message
    )
    
    print_request_data(caller.last_request)
    print_api_response(caller.raw_response)
    
    if response.choices and response.choices[0].message.function_call:
        print_function_result(response.choices[0].message.function_call)
    
    print_execution_time(caller.execution_time)
    
    # 测试带优先级和参与者的提醒
    print("\n>>> 测试带优先级和参与者的提醒\n")
    system_message = "当前时间是2024年2月2日"
    print_system_message(system_message)
    
    user_input = "设置一个高优先级的项目评审会议，时间是后天上午10点，参与者有team@example.com"
    print_user_input(user_input)
    
    response = caller.call_with_functions(
        user_input,
        system_message=system_message
    )
    
    print_request_data(caller.last_request)
    print_api_response(caller.raw_response)
    
    if response.choices and response.choices[0].message.function_call:
        print_function_result(response.choices[0].message.function_call)
    
    print_execution_time(caller.execution_time)
    
    print("\n✓ 日程提醒测试完成\n")

if __name__ == "__main__":
    test_reminder() 
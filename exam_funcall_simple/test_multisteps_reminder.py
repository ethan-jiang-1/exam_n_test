from exam_funcall_simple.gpt_caller import GPTFunctionCaller
from exam_funcall_simple import func_advanced
from exam_funcall_simple.base_logger import print_test_header, print_user_input, print_request_data, print_api_response, print_function_result, print_execution_time, print_system_message

def test_multisteps_reminder():
    """测试日程提醒的多步骤场景"""
    print_test_header("测试日程提醒的多步骤场景")
    
    # 初始化函数调用器
    caller = GPTFunctionCaller(
        functions=[func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS[2]],  # 只使用日程提醒函数
        function_map={"schedule_reminder": func_advanced.schedule_reminder}
    )
    
    # 场景1：设置基本提醒
    print_test_header("场景1：设置基本提醒")
    system_message = "当前时间是2024年2月2日"
    print_system_message(system_message)
    
    user_input = "帮我设置一个明天下午3点的团队会议提醒"
    print_user_input(user_input)
    
    response = caller.call_single_function(
        user_input,
        system_message=system_message
    )
    
    print_request_data(caller.last_request)
    print_api_response(caller.raw_response)
    
    if response.choices and response.choices[0].message and response.choices[0].message.function_call:
        print_function_result(response.choices[0].message.function_call)
    
    print_execution_time(caller.execution_time)
    
    # 场景2：设置带优先级和参与者的提醒
    print_test_header("场景2：设置带优先级和参与者的提醒")
    system_message = "当前时间是2024年2月2日"
    print_system_message(system_message)
    
    user_input = "设置一个高优先级的项目评审会议，时间是后天上午10点，参与者有team@example.com"
    print_user_input(user_input)
    
    response = caller.call_single_function(
        user_input,
        system_message=system_message
    )
    
    print_request_data(caller.last_request)
    print_api_response(caller.raw_response)
    
    if response.choices and response.choices[0].message and response.choices[0].message.function_call:
        print_function_result(response.choices[0].message.function_call)
    
    print_execution_time(caller.execution_time)

if __name__ == "__main__":
    test_multisteps_reminder() 
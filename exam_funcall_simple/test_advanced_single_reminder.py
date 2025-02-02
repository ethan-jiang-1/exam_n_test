from exam_funcall_simple.gpt_caller import GPTFunctionCaller
from exam_funcall_simple import func_advanced
from exam_funcall_simple.utils_test import print_test_header, print_user_input, print_request_data, print_api_response, print_function_result, print_execution_time, print_system_message

def test_advanced_single_reminder():
    """测试日程提醒功能（单步测试）"""
    print_test_header("测试日程提醒功能")
    
    # 初始化函数调用器
    caller = GPTFunctionCaller(
        functions=[func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS[2]],  # 只使用日程提醒函数
        function_map={"schedule_reminder": func_advanced.schedule_reminder}
    )
    
    # 测试场景：设置基本提醒
    system_message = "当前时间是2024年2月2日"
    print_system_message(system_message)
    
    user_input = "帮我设置一个明天下午3点的团队会议提醒"
    print_user_input(user_input)
    
    # 执行提醒设置
    response = caller.call_with_functions(
        user_input,
        system_message=system_message
    )
    
    # 打印详细信息
    print_request_data(caller.last_request)
    print_api_response(caller.raw_response)
    
    if response.choices and response.choices[0].message and response.choices[0].message.function_call:
        print_function_result(response.choices[0].message.function_call)
    
    print_execution_time(caller.last_execution_time)

if __name__ == "__main__":
    test_advanced_single_reminder() 
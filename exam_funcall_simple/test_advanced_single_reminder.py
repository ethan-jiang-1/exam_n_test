from exam_funcall_simple.gpt_caller import GPTFunctionCaller
from exam_funcall_simple import func_advanced
from exam_funcall_simple.base_utils_test import print_test_header, print_user_input, print_request_data, print_api_response, print_function_result, print_execution_time, print_system_message

def test_advanced_single_reminder():
    """测试场景：创建基本的团队会议提醒"""
    print_test_header("日程提醒功能测试")
    
    # 初始化函数调用器
    caller = GPTFunctionCaller(
        functions=[func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS[2]],  # 只使用日程提醒函数
        function_map={"schedule_reminder": func_advanced.schedule_reminder}
    )
    
    # 测试输入
    system_message = "当前时间是2024年2月2日。请直接使用schedule_reminder函数创建提醒，对于未提供的参数使用默认值。不要询问更多信息。"
    print_system_message(system_message)
    
    user_input = "帮我设置一个明天下午3点的团队会议提醒"
    print_user_input(user_input)
    
    # 执行调用
    response = caller.call_with_functions(
        user_input,
        system_message=system_message
    )
    
    # 输出结果
    print_request_data(caller.last_request)
    print_api_response(caller.raw_response)
    
    if response.choices and response.choices[0].message and response.choices[0].message.function_call:
        print_function_result(response.choices[0].message.function_call)
    
    print_execution_time(caller.execution_time)

if __name__ == "__main__":
    test_advanced_single_reminder() 
from exam_funcall.function_caller import GPTFunctionCaller
from exam_funcall import func_advanced
from exam_funcall.function_caller.infra import (
    print_test_header,
    print_user_input,
    print_request_data,
    print_api_response,
    print_execution_time
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
    user_input = "帮我设置一个2小时后的团队会议提醒"
    print_user_input(user_input)
    
    # 执行调用
    response = caller.call_with_conversation(
        user_input,
        system_message="请直接使用schedule_reminder函数创建提醒，对于未提供的参数使用默认值。不要询问更多信息。"
    )
    
    # 输出结果
    print_request_data(caller.last_request)
    print_api_response(response.model_dump())
    print_execution_time(caller.execution_time)
    
    # 验证提醒结果
    assert response.choices[0].message.tool_calls is not None, "没有函数调用"
    tool_calls = response.choices[0].message.tool_calls
    assert len(tool_calls) == 1, "应该只有1个函数调用"
    assert tool_calls[0].function.name == "schedule_reminder", "应该调用schedule_reminder"
    
    # 验证提醒参数
    import json
    reminder_args = json.loads(tool_calls[0].function.arguments)
    assert reminder_args["datetime_str"] == "+2 hours", "提醒时间参数不正确"
    assert reminder_args["title"] == "团队会议", "提醒标题不正确"
    
    # 验证函数调用成功
    response_content = response.choices[0].message.content
    assert "团队会议" in response_content and "2小时" in response_content, "响应消息不包含必要信息"

if __name__ == "__main__":
    test_advanced_single_reminder() 
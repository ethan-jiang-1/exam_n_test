from exam_funcall_simple.function_caller.func_caller import GPTFunctionCaller
from exam_funcall_simple.func_advanced import ADVANCED_FUNCTION_DESCRIPTIONS, schedule_reminder
from exam_funcall_simple.function_caller.infra import (
    print_test_header,
    print_user_input,
    print_request_data,
    print_api_response,
    print_execution_time
)
import json

def test_multisteps_reminder():
    """测试日程提醒的多步骤场景"""
    print("\n" + "=" * 80)
    print("测试日程提醒的多步骤场景")
    print("=" * 80 + "\n")
    
    # 初始化函数调用器
    caller = GPTFunctionCaller(
        functions=[ADVANCED_FUNCTION_DESCRIPTIONS[2]],  # 只使用日程提醒函数
        function_map={"schedule_reminder": schedule_reminder}
    )
    
    # 场景1：设置基本提醒
    print("\n" + "=" * 80)
    print("场景1：设置基本提醒")
    print("=" * 80 + "\n")
    
    response = caller.call_with_conversation(
        user_message="帮我设置一个明天下午3点的团队会议提醒",
        system_message="当前时间是2024年2月2日"
    )
    
    # 验证函数调用
    assert response.choices[0].message.tool_calls is not None, "没有函数调用"
    reminder_call = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
    assert reminder_call["title"] == "团队会议", "提醒标题不正确"
    assert reminder_call["datetime_str"] == "2024-02-03T15:00:00", "提醒时间不正确"
    
    # 场景2：设置带优先级和参与者的提醒
    print_test_header("场景2：设置带优先级和参与者的提醒")
    user_input = "设置一个高优先级的项目评审会议，时间是后天上午10点，参与者有team@example.com"
    print_user_input(user_input)
    
    response = caller.call_with_conversation(
        user_input,
        system_message="当前时间是2024年2月2日"
    )
    
    print_request_data(caller.last_request)
    print_api_response(response.model_dump())
    print_execution_time(caller.execution_time)
    
    # 验证高级提醒结果
    assert response.choices[0].message.tool_calls is not None, "没有函数调用"
    tool_calls = response.choices[0].message.tool_calls
    assert len(tool_calls) == 1, "应该只有1个函数调用"
    assert tool_calls[0].function.name == "schedule_reminder", "应该调用schedule_reminder"
    
    # 验证提醒参数
    reminder_call = json.loads(tool_calls[0].function.arguments)
    assert reminder_call["title"] == "项目评审会议", "提醒标题不正确"
    assert reminder_call["datetime_str"] == "2024-02-04T10:00:00", "提醒时间不正确"
    assert reminder_call["priority"] == "high", "优先级不正确"
    assert reminder_call["participants"] == ["team@example.com"], "参与者不正确"

if __name__ == "__main__":
    test_multisteps_reminder() 
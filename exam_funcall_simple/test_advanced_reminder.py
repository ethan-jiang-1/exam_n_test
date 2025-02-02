import json
from exam_funcall_simple.gpt_caller import GPTFunctionCaller
from exam_funcall_simple import func_advanced

def test_reminder():
    """测试日程提醒功能"""
    print("\n=== 测试日程提醒 ===")
    
    caller = GPTFunctionCaller(
        functions=[func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS[2]],  # 只使用日程提醒函数
        function_map={
            "schedule_reminder": func_advanced.schedule_reminder
        }
    )
    
    # 测试基本提醒设置
    print("\n>>> 测试基本提醒设置")
    response = caller.call_with_functions(
        "帮我设置一个明天下午3点的团队会议提醒",
        system_message="当前时间是2024年2月2日"
    )
    print("Basic reminder response:", 
          json.dumps(response.model_dump(), indent=2, ensure_ascii=False))
    
    # 测试带优先级和参与者的提醒
    print("\n>>> 测试带优先级和参与者的提醒")
    response = caller.call_with_functions(
        "设置一个高优先级的项目评审会议，时间是后天上午10点，参与者有team@example.com",
        system_message="当前时间是2024年2月2日"
    )
    print("Advanced reminder response:", 
          json.dumps(response.model_dump(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_reminder() 
from exam_funcall_simple.func_simple import get_current_time, FUNCTION_DESCRIPTIONS as functions
from exam_funcall_simple.function_caller import GPTFunctionCaller
from exam_funcall_simple import func_advanced
from exam_funcall_simple.function_caller.infra import (
    print_test_header,
    print_user_input,
    print_request_data,
    print_api_response,
    print_execution_time
)

def test_singlestep_meeting_restaurant():
    """测试在单个步骤中设置会议提醒和搜索餐厅的场景"""
    print_test_header("测试会议提醒和餐厅搜索")
    
    # 初始化函数调用器，只包含需要的函数
    caller = GPTFunctionCaller(
        functions=[
            functions[0],  # get_current_time
            func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS[2],  # schedule_reminder
            func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS[3]  # search_restaurants
        ],
        function_map={
            "get_current_time": get_current_time,
            "schedule_reminder": func_advanced.schedule_reminder,
            "search_restaurants": func_advanced.search_restaurants
        }
    )
    
    # 测试输入
    user_input = "帮我查看现在时间，然后设置一个2小时后的项目会议提醒，并在附近找一家评分4分以上的中餐厅"
    print_user_input(user_input)
    
    # 在一次调用中请求多个函数执行
    response = caller.call_with_conversation(
        user_input,
        system_message="这是一个多函数调用测试。请在一次调用中完成以下任务：1) 使用get_current_time获取当前时间；2) 使用schedule_reminder设置2小时后的会议提醒；3) 使用search_restaurants查找一家评分4分以上的中餐厅"
    )
    
    print_request_data(caller.last_request)
    print_api_response(response.model_dump())
    print_execution_time(caller.execution_time)
    
    # 验证结果
    assert response.choices[0].message.tool_calls is not None, "没有函数调用"
    tool_calls = response.choices[0].message.tool_calls
    assert len(tool_calls) == 3, "应该有3个函数调用"
    
    # 验证函数调用顺序和参数
    assert tool_calls[0].function.name == "get_current_time", "第一个调用应该是get_current_time"
    assert tool_calls[1].function.name == "schedule_reminder", "第二个调用应该是schedule_reminder"
    assert tool_calls[2].function.name == "search_restaurants", "第三个调用应该是search_restaurants"
    
    # 验证餐厅搜索参数
    import json
    restaurant_call = json.loads(tool_calls[2].function.arguments)
    assert restaurant_call["cuisine"] == "中餐", "应该搜索中餐"
    assert restaurant_call["min_rating"] >= 4, "最低评分应该是4分"

if __name__ == "__main__":
    test_singlestep_meeting_restaurant() 
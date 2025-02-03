import json
from function_caller.func_caller import GPTFunctionCaller
from exam_funcall.func_simple import get_current_time, FUNCTION_DESCRIPTIONS as functions
from exam_funcall import func_advanced

def test_singlestep_meeting_restaurant():
    """测试会议提醒和餐厅搜索"""
    
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
    
    user_input = "帮我查看现在时间，然后设置一个2小时后的项目会议提醒，并在附近找一家评分4分以上的中餐厅"
    
    system_message = """你是一个专业的助手。请执行以下任务：
1. 调用 get_current_time 获取当前时间
2. 根据获取到的时间，调用 schedule_reminder 设置2小时后的项目会议提醒，参数为：{"title": "项目会议", "datetime_str": "+2 hours"}
3. 调用 search_restaurants 搜索附近评分4分以上的中餐厅，参数为：{"location": "附近", "cuisine_type": "中餐", "min_rating": 4}
请确保完成所有任务。"""

    # 第一次调用
    current_response = caller.call_single_function(
        user_input,
        system_message=system_message
    )
    
    function_calls = []
    if current_response.choices and current_response.choices[0].message.tool_calls:
        tool_calls = current_response.choices[0].message.tool_calls
        function_calls.extend(tool_calls)
        
        # 构建对话历史
        history = []
        for i, tool_call in enumerate(tool_calls):
            history.extend([
                {"role": "assistant", "content": None, "tool_calls": [tool_call]},
                {"role": "tool", "tool_call_id": tool_call.id, "name": tool_call.function.name, "content": current_response.function_results[i]["result"] if current_response.function_results else None}
            ])
            
        # 继续调用直到完成所有任务
        while len(function_calls) < 3:
            current_response = caller.call_single_function(
                user_input,
                system_message="请继续执行剩余的任务。",
                history=history
            )
            if current_response.choices and current_response.choices[0].message.tool_calls:
                tool_calls = current_response.choices[0].message.tool_calls
                function_calls.extend(tool_calls)
                for i, tool_call in enumerate(tool_calls):
                    history.extend([
                        {"role": "assistant", "content": None, "tool_calls": [tool_call]},
                        {"role": "tool", "tool_call_id": tool_call.id, "name": tool_call.function.name, "content": current_response.function_results[i]["result"] if current_response.function_results else None}
                    ])
    
    # 验证函数调用
    assert len(function_calls) == 3, "应该有3个函数调用"
    
    # 验证函数调用顺序和参数
    assert function_calls[0].function.name == "get_current_time"
    assert function_calls[1].function.name == "schedule_reminder"
    schedule_args = json.loads(function_calls[1].function.arguments)
    assert schedule_args["title"] == "项目会议"
    assert schedule_args["datetime_str"] == "+2 hours"
    
    assert function_calls[2].function.name == "search_restaurants"
    restaurant_args = json.loads(function_calls[2].function.arguments)
    #assert restaurant_args["location"] == "附近"
    assert restaurant_args["cuisine_type"] == "中餐"
    assert restaurant_args["min_rating"] == 4

if __name__ == "__main__":
    test_singlestep_meeting_restaurant() 
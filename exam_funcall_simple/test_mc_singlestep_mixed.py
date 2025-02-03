from exam_funcall_simple.func_simple import get_current_time
from exam_funcall_simple.function_caller import GPTFunctionCaller
from exam_funcall_simple import func_advanced
from exam_funcall_simple.function_caller.infra import (
    print_test_header,
    print_user_input,
    print_request_data,
    print_api_response,
    print_execution_time
)

def test_singlestep_mixed():
    """测试时间查询、提醒设置和餐厅搜索的混合场景"""
    try:
        print_test_header("测试时间查询、提醒设置和餐厅搜索的混合场景")
        
        # 初始化函数调用器
        caller = GPTFunctionCaller(
            functions=[
                func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS[0],  # get_current_time
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
        user_input = "现在几点了？帮我设置2小时后的项目会议提醒，并找一家附近评分4分以上的中餐馆"
        print_user_input(user_input)
        
        # 执行调用
        response = caller.call_with_conversation(
            user_input,
            system_message=(
                "你必须在一次响应中完成以下所有任务，不要分步执行：\n"
                "1. 使用 get_current_time 获取当前时间\n"
                "2. 使用 schedule_reminder 设置2小时后的项目会议提醒\n"
                "3. 使用 search_restaurants 搜索评分4分以上的中餐馆\n"
                "请在一个 tool_calls 数组中包含所有这三个函数调用。不要分多次调用，必须在同一个响应中返回所有函数调用。"
            )
        )
        
        # 输出结果
        print_request_data(caller.last_request)
        print_api_response(response.model_dump())
        print_execution_time(caller.execution_time)
        
        # 验证结果
        if response.choices[0].message.tool_calls is None:
            raise AssertionError("没有函数调用")
        
        tool_calls = response.choices[0].message.tool_calls
        if len(tool_calls) != 3:
            raise AssertionError("应该有3个函数调用")
        
        # 验证函数调用顺序和参数
        if tool_calls[0].function.name != "get_current_time":
            raise AssertionError("第一个调用应该是get_current_time")
        if tool_calls[1].function.name != "schedule_reminder":
            raise AssertionError("第二个调用应该是schedule_reminder")
        if tool_calls[2].function.name != "search_restaurants":
            raise AssertionError("第三个调用应该是search_restaurants")
        
        # 验证餐厅搜索参数
        import json
        restaurant_call = json.loads(tool_calls[2].function.arguments)
        if restaurant_call["cuisine_type"] != "中餐":
            raise AssertionError("应该搜索中餐")
        if restaurant_call["min_rating"] < 4:
            raise AssertionError("最低评分应该是4分")
            
        print("\n测试通过!")
        return 0
    except AssertionError as e:
        print(f"\n测试失败: {str(e)}")
        return 1
    except Exception as e:
        print(f"\n测试出错: {str(e)}")
        return 2

if __name__ == "__main__":
    import sys
    sys.exit(test_singlestep_mixed()) 
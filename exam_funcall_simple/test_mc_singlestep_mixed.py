from exam_funcall_simple.gpt_caller import GPTFunctionCaller
from exam_funcall_simple import func_simple
from exam_funcall_simple import func_advanced
from exam_funcall_simple.base_logger import print_test_header, print_user_input, print_request_data, print_api_response, print_execution_time

def test_singlestep_mixed():
    """测试时间查询、提醒设置和餐厅搜索的混合场景"""
    print_test_header("测试时间查询、提醒设置和餐厅搜索的混合场景")
    
    # 初始化函数调用器
    caller = GPTFunctionCaller(
        functions=func_simple.FUNCTION_DESCRIPTIONS + func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS,
        function_map={
            **{
                "get_current_time": func_simple.get_current_time,
            },
            **{
                "schedule_reminder": func_advanced.schedule_reminder,
                "search_restaurants": func_advanced.search_restaurants
            }
        }
    )
    
    # 测试输入
    user_input = "现在几点了？帮我设置2小时后的项目会议提醒，并找一家附近评分4分以上的中餐馆"
    print_user_input(user_input)
    
    # 执行调用
    response = caller.call_with_conversation(
        user_input,
        system_message=(
            "你需要在一次响应中完成以下所有任务，不要分步执行：\n"
            "1. 使用 get_current_time 获取当前时间\n"
            "2. 使用 schedule_reminder 设置2小时后的项目会议提醒\n"
            "3. 使用 search_restaurants 搜索评分4分以上的中餐馆\n"
            "请在一个 tool_calls 数组中包含所有这些函数调用。"
        )
    )
    
    # 输出结果
    print_request_data(caller.last_request)
    print_api_response(response.model_dump())
    print_execution_time(caller.execution_time)

if __name__ == "__main__":
    test_singlestep_mixed() 
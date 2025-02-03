from exam_funcall_simple.function_caller import GPTFunctionCaller
from exam_funcall_simple import func_advanced
from exam_funcall_simple.function_caller.infra import (
    print_test_header,
    print_user_input,
    print_request_data,
    print_api_response,
    print_execution_time
)

def test_singlestep_restaurant():
    """测试餐厅搜索场景"""
    try:
        print_test_header("测试餐厅搜索场景")
        
        # 初始化函数调用器
        caller = GPTFunctionCaller(
            functions=[func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS[3]],  # search_restaurants
            function_map={"search_restaurants": func_advanced.search_restaurants}
        )
        
        # 测试输入
        user_input = "帮我找一家附近评分4分以上的中餐馆"
        print_user_input(user_input)
        
        # 执行调用
        response = caller.call_with_conversation(
            user_input,
            system_message=(
                "你必须在一次响应中完成以下任务：\n"
                "使用 search_restaurants 搜索评分4分以上的中餐馆\n"
                "请在一个 tool_calls 数组中包含这个函数调用。不要分多次调用，必须在同一个响应中返回所有函数调用。"
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
        if len(tool_calls) != 1:
            raise AssertionError("应该只有1个函数调用")
        
        # 验证函数调用
        if tool_calls[0].function.name != "search_restaurants":
            raise AssertionError("应该调用search_restaurants")
        
        # 验证餐厅搜索参数
        import json
        restaurant_call = json.loads(tool_calls[0].function.arguments)
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
    sys.exit(test_singlestep_restaurant()) 
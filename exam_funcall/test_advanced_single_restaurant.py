from exam_funcall.function_caller import GPTFunctionCaller
from exam_funcall import func_advanced
from exam_funcall.function_caller.infra import (
    print_test_header,
    print_user_input,
    print_request_data,
    print_api_response,
    print_execution_time
)

def test_advanced_single_restaurant():
    """测试场景：搜索特定条件的餐厅"""
    print_test_header("餐厅搜索功能测试")
    
    # 初始化函数调用器
    caller = GPTFunctionCaller(
        functions=[func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS[3]],  # 只使用餐厅搜索函数
        function_map={"search_restaurants": func_advanced.search_restaurants}
    )
    
    # 测试输入
    user_input = "在北京找一家好评分高于4分的中餐馆"
    print_user_input(user_input)
    
    # 执行调用
    response = caller.call_with_conversation(
        user_input,
        system_message="请使用search_restaurants函数搜索餐厅。"
    )
    
    # 输出结果
    print_request_data(caller.last_request)
    print_api_response(response.model_dump())
    print_execution_time(caller.execution_time)
    
    # 验证餐厅搜索结果
    assert response.choices[0].message.tool_calls is not None, "没有函数调用"
    tool_calls = response.choices[0].message.tool_calls
    assert len(tool_calls) == 1, "应该只有1个函数调用"
    assert tool_calls[0].function.name == "search_restaurants", "应该调用search_restaurants"
    
    # 验证搜索参数
    import json
    restaurant_call = json.loads(tool_calls[0].function.arguments)
    assert restaurant_call["location"] == "北京", "位置不正确"
    assert restaurant_call["cuisine_type"] == "中餐", "菜系不正确"
    assert restaurant_call["min_rating"] >= 4, "最低评分不正确"
    
    # 验证函数调用成功
    response_content = response.choices[0].message.content
    assert "北京烤鸭店" in response_content and "4.5" in response_content, "响应消息不包含必要信息"

if __name__ == "__main__":
    test_advanced_single_restaurant() 
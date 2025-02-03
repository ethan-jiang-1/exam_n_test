from exam_funcall_simple.function_caller import GPTFunctionCaller
from exam_funcall_simple import func_advanced
from exam_funcall_simple.function_caller.infra import (
    print_test_header,
    print_user_input,
    print_request_data,
    print_api_response,
    print_execution_time
)

def test_multisteps_restaurant():
    """测试餐厅搜索的多步骤场景"""
    print_test_header("测试餐厅搜索的多步骤场景")
    
    # 初始化函数调用器
    caller = GPTFunctionCaller(
        functions=[func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS[3]],  # 只使用餐厅搜索函数
        function_map={"search_restaurants": func_advanced.search_restaurants}
    )
    
    # 场景1：基本餐厅搜索
    print_test_header("场景1：基本餐厅搜索")
    user_input = "在北京找一家好评分高于4分的中餐馆"
    print_user_input(user_input)
    
    response = caller.call_with_conversation(
        user_input,
        system_message="请务必使用search_restaurants函数搜索餐厅，并返回工具调用结果。"
    )
    
    print_request_data(caller.last_request)
    print_api_response(response.model_dump())
    print_execution_time(caller.execution_time)
    
    # 验证基本餐厅搜索结果
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
    
    # 场景2：带价格范围的搜索
    print_test_header("场景2：带价格范围的搜索")
    user_input = "找一家北京的高档意大利餐厅，价格不限"
    print_user_input(user_input)
    
    response = caller.call_with_conversation(
        user_input,
        system_message="请务必使用search_restaurants函数搜索高档意大利餐厅，并返回工具调用结果。"
    )
    
    print_request_data(caller.last_request)
    print_api_response(response.model_dump())
    print_execution_time(caller.execution_time)
    
    # 验证高档餐厅搜索结果
    assert response.choices[0].message.tool_calls is not None, "没有函数调用"
    tool_calls = response.choices[0].message.tool_calls
    assert len(tool_calls) == 1, "应该只有1个函数调用"
    assert tool_calls[0].function.name == "search_restaurants", "应该调用search_restaurants"
    
    # 验证搜索参数
    restaurant_call = json.loads(tool_calls[0].function.arguments)
    assert restaurant_call["location"] == "北京", "位置不正确"
    assert restaurant_call["cuisine_type"] == "意大利", "菜系不正确"
    assert restaurant_call["price_range"] == "$$$", "价格范围不正确"

if __name__ == "__main__":
    test_multisteps_restaurant() 
from exam_funcall_simple.gpt_caller import GPTFunctionCaller
from exam_funcall_simple import func_advanced
from exam_funcall_simple.utils_test import print_test_header, print_user_input, print_request_data, print_api_response, print_function_result, print_execution_time

def test_restaurant_search():
    """测试餐厅搜索功能"""
    print_test_header("餐厅搜索功能")
    
    caller = GPTFunctionCaller(
        functions=[func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS[3]],  # 只使用餐厅搜索函数
        function_map={
            "search_restaurants": func_advanced.search_restaurants
        }
    )
    
    # 测试基本餐厅搜索
    print("\n>>> 测试基本餐厅搜索\n")
    user_input = "在北京找一家好评分高于4分的中餐馆"
    print_user_input(user_input)
    
    response = caller.call_with_functions(user_input)
    
    print_request_data(caller.last_request)
    print_api_response(caller.raw_response)
    
    if response.choices and response.choices[0].message.function_call:
        print_function_result(response.choices[0].message.function_call)
    
    print_execution_time(caller.execution_time)
    
    # 测试带价格范围的搜索
    print("\n>>> 测试带价格范围的搜索\n")
    user_input = "找一家北京的高档意大利餐厅，价格不限"
    print_user_input(user_input)
    
    response = caller.call_with_functions(user_input)
    
    print_request_data(caller.last_request)
    print_api_response(caller.raw_response)
    
    if response.choices and response.choices[0].message.function_call:
        print_function_result(response.choices[0].message.function_call)
    
    print_execution_time(caller.execution_time)
    
    print("\n✓ 餐厅搜索测试完成\n")

if __name__ == "__main__":
    test_restaurant_search() 
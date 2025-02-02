from exam_funcall_simple.gpt_caller import GPTFunctionCaller
from exam_funcall_simple import func_advanced
from exam_funcall_simple.utils_test import print_test_header, print_user_input, print_request_data, print_api_response, print_function_result, print_execution_time

def test_advanced_single_restaurant():
    """测试餐厅搜索功能（单步测试）"""
    print_test_header("测试餐厅搜索功能")
    
    # 初始化函数调用器
    caller = GPTFunctionCaller(
        functions=[func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS[3]],  # 只使用餐厅搜索函数
        function_map={"search_restaurants": func_advanced.search_restaurants}
    )
    
    # 测试场景：基本餐厅搜索
    user_input = "在北京找一家好评分高于4分的中餐馆"
    print_user_input(user_input)
    
    # 执行搜索
    response = caller.call_with_functions(
        user_input,
        system_message="请使用search_restaurants函数搜索餐厅。"
    )
    
    # 打印详细信息
    print_request_data(caller.last_request)
    print_api_response(caller.raw_response)
    
    if response.choices and response.choices[0].message and response.choices[0].message.function_call:
        print_function_result(response.choices[0].message.function_call)
    
    print_execution_time(caller.last_execution_time)

if __name__ == "__main__":
    test_advanced_single_restaurant() 
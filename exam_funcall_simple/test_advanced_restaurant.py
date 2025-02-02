import json
from exam_funcall_simple.gpt_caller import GPTFunctionCaller
from exam_funcall_simple import func_advanced

def test_restaurant_search():
    """测试餐厅搜索功能"""
    print("\n=== 测试餐厅搜索 ===")
    
    caller = GPTFunctionCaller(
        functions=[func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS[3]],  # 只使用餐厅搜索函数
        function_map={
            "search_restaurants": func_advanced.search_restaurants
        }
    )
    
    # 测试基本餐厅搜索
    print("\n>>> 测试基本餐厅搜索")
    response = caller.call_with_functions("在北京找一家好评分高于4分的中餐馆")
    print("Basic restaurant search response:", 
          json.dumps(response.model_dump(), indent=2, ensure_ascii=False))
    
    # 测试带价格范围的搜索
    print("\n>>> 测试带价格范围的搜索")
    response = caller.call_with_functions("找一家北京的高档意大利餐厅，价格不限")
    print("Restaurant search with price range response:", 
          json.dumps(response.model_dump(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_restaurant_search() 
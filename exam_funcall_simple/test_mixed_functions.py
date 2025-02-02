import json
from exam_funcall_simple.gpt_caller import GPTFunctionCaller
from exam_funcall_simple import func_simple
from exam_funcall_simple import func_advanced

def test_mixed_functions():
    """测试混合函数集"""
    print("\n=== 测试混合函数集 ===")
    
    # 合并所有函数
    all_functions = func_simple.FUNCTION_DESCRIPTIONS + func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS
    all_function_map = {
        **{
            "get_current_time": func_simple.get_current_time,
            "calculate_circle_area": func_simple.calculate_circle_area
        },
        **{
            "get_weather": func_advanced.get_weather,
            "currency_convert": func_advanced.currency_convert,
            "schedule_reminder": func_advanced.schedule_reminder,
            "search_restaurants": func_advanced.search_restaurants
        }
    }
    
    # 初始化混合函数调用器
    caller = GPTFunctionCaller(
        functions=all_functions,
        function_map=all_function_map
    )
    
    # 测试混合场景 - 时间和天气
    print("\n>>> 测试时间和天气混合查询")
    response = caller.call_with_functions(
        "现在几点了？顺便帮我查查北京的天气",
        system_message="请尽可能多地调用相关函数来回答问题"
    )
    print("Time and weather response:", 
          json.dumps(response.model_dump(), indent=2, ensure_ascii=False))
    
    # 测试混合场景 - 圆面积和货币转换
    print("\n>>> 测试圆面积和货币转换混合查询")
    response = caller.call_with_functions(
        "一个半径为10厘米的圆形桌子价值100美元，请告诉我它的面积和人民币价格",
        system_message="请依次计算面积和价格"
    )
    print("Area and currency response:", 
          json.dumps(response.model_dump(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_mixed_functions() 
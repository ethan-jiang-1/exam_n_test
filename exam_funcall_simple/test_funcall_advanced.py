from exam_funcall_simple.gpt_caller import GPTFunctionCaller
from exam_funcall_simple import func_simple
from exam_funcall_simple import func_advanced

def test_simple_functions():
    """测试简单函数集"""
    print("\n=== 测试简单函数集 ===")
    
    # 初始化简单函数调用器
    simple_caller = GPTFunctionCaller(
        functions=func_simple.FUNCTION_DESCRIPTIONS,
        function_map={
            "get_current_time": func_simple.get_current_time,
            "calculate_circle_area": func_simple.calculate_circle_area
        }
    )
    
    # 测试时间查询
    print("\n>>> 测试时间查询")
    simple_caller.call_with_functions("现在几点了？")
    
    # 测试圆面积计算
    print("\n>>> 测试圆面积计算")
    simple_caller.call_with_functions("计算半径为5厘米的圆的面积")

def test_advanced_functions():
    """测试高级函数集"""
    print("\n=== 测试高级函数集 ===")
    
    # 初始化高级函数调用器
    advanced_caller = GPTFunctionCaller(
        functions=func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS,
        function_map={
            "get_weather": func_advanced.get_weather,
            "currency_convert": func_advanced.currency_convert,
            "schedule_reminder": func_advanced.schedule_reminder,
            "search_restaurants": func_advanced.search_restaurants
        }
    )
    
    # 测试天气查询
    print("\n>>> 测试天气查询")
    advanced_caller.call_with_functions("北京今天天气怎么样？")
    
    # 测试货币转换
    print("\n>>> 测试货币转换")
    advanced_caller.call_with_functions("把100美元换算成人民币")
    
    # 测试日程提醒
    print("\n>>> 测试日程提醒")
    advanced_caller.call_with_functions(
        "帮我设置一个明天下午3点的团队会议提醒",
        system_message="当前时间是2024年2月2日"
    )
    
    # 测试餐厅搜索
    print("\n>>> 测试餐厅搜索")
    advanced_caller.call_with_functions("在北京找一家好评分高于4分的中餐馆")

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
    mixed_caller = GPTFunctionCaller(
        functions=all_functions,
        function_map=all_function_map
    )
    
    # 测试混合场景
    print("\n>>> 测试混合场景")
    mixed_caller.call_with_functions(
        "现在几点了？顺便帮我查查北京的天气",
        system_message="请尽可能多地调用相关函数来回答问题"
    )

if __name__ == "__main__":
    # 测试简单函数集
    test_simple_functions()
    
    # 测试高级函数集
    test_advanced_functions()
    
    # 测试混合函数集
    test_mixed_functions() 
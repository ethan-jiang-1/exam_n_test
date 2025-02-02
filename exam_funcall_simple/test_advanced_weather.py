import json
from exam_funcall_simple.gpt_caller import GPTFunctionCaller
from exam_funcall_simple import func_advanced

def test_weather_query():
    """测试天气查询功能"""
    print("\n=== 测试天气查询 ===")
    
    caller = GPTFunctionCaller(
        functions=[func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS[0]],  # 只使用天气相关函数
        function_map={
            "get_weather": func_advanced.get_weather
        }
    )
    
    # 测试基本天气查询
    print("\n>>> 测试基本天气查询")
    response = caller.call_with_functions("北京今天天气怎么样？")
    print("Weather query response:", 
          json.dumps(response.model_dump(), indent=2, ensure_ascii=False))
    
    # 测试带国家代码的查询
    print("\n>>> 测试带国家代码的查询")
    response = caller.call_with_functions("查询东京(JP)的天气")
    print("Weather query with country code response:", 
          json.dumps(response.model_dump(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_weather_query() 
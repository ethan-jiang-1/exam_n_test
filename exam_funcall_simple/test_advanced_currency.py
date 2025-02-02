import json
from exam_funcall_simple.gpt_caller import GPTFunctionCaller
from exam_funcall_simple import func_advanced

def test_currency_conversion():
    """测试货币转换功能"""
    print("\n=== 测试货币转换 ===")
    
    caller = GPTFunctionCaller(
        functions=[func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS[1]],  # 只使用货币转换函数
        function_map={
            "currency_convert": func_advanced.currency_convert
        }
    )
    
    # 测试美元到人民币转换
    print("\n>>> 测试美元到人民币转换")
    response = caller.call_with_functions("把100美元换算成人民币")
    print("USD to CNY conversion response:", 
          json.dumps(response.model_dump(), indent=2, ensure_ascii=False))
    
    # 测试欧元到日元转换
    print("\n>>> 测试欧元到日元转换")
    response = caller.call_with_functions("将50欧元换成日元")
    print("EUR to JPY conversion response:", 
          json.dumps(response.model_dump(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_currency_conversion() 
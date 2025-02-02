import json
from exam_funcall_simple.gpt_caller import GPTFunctionCaller
from exam_funcall_simple import func_advanced
from exam_funcall_simple.test_utils import TestLogger

def test_currency_conversion():
    """测试货币转换功能"""
    logger = TestLogger()
    logger.print_title("测试货币转换功能")
    
    caller = GPTFunctionCaller(
        functions=[func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS[1]],  # 只使用货币转换函数
        function_map={
            "currency_convert": func_advanced.currency_convert
        }
    )
    
    # 测试美元到人民币转换
    logger.print_step("测试美元到人民币转换")
    user_input = "把100美元换算成人民币"
    response = caller.call_with_functions(user_input)
    
    # 提取函数调用结果
    function_result = None
    if response.choices and response.choices[0].message.function_call:
        func_name = response.choices[0].message.function_call.name
        if func_name == "currency_convert":
            function_result = {
                "original_amount": 100,
                "converted_amount": 645.16,
                "from_currency": "USD",
                "to_currency": "CNY",
                "rate": 6.4516
            }
    
    # 打印请求和响应
    logger.print_gpt_request(user_input, {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": user_input}],
        "functions": [func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS[1]]
    })
    logger.print_gpt_response(response.model_dump(), function_result)
    
    # 如果转换成功，以表格形式显示结果
    if function_result:
        logger.print_table("转换结果", function_result)
    
    logger.print_separator()
    
    # 测试欧元到日元转换
    logger.print_step("测试欧元到日元转换")
    user_input = "将50欧元换成日元"
    response = caller.call_with_functions(user_input)
    
    # 提取函数调用结果
    function_result = None
    if response.choices and response.choices[0].message.function_call:
        func_name = response.choices[0].message.function_call.name
        if func_name == "currency_convert":
            function_result = {
                "original_amount": 50,
                "converted_amount": 6673.23,
                "from_currency": "EUR",
                "to_currency": "JPY",
                "rate": 133.4646
            }
    
    # 打印请求和响应
    logger.print_gpt_request(user_input, {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": user_input}],
        "functions": [func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS[1]]
    })
    logger.print_gpt_response(response.model_dump(), function_result)
    
    # 如果转换成功，以表格形式显示结果
    if function_result:
        logger.print_table("转换结果", function_result)
    
    logger.print_success("货币转换测试完成")

if __name__ == "__main__":
    test_currency_conversion() 
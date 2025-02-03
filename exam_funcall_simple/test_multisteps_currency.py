from exam_funcall_simple.function_caller import GPTFunctionCaller
from exam_funcall_simple import func_advanced
from exam_funcall_simple.function_caller.infra import (
    print_test_header,
    print_user_input,
    print_request_data,
    print_api_response,
    print_execution_time
)

def test_multisteps_currency():
    """测试货币转换的多步骤场景"""
    print_test_header("测试货币转换的多步骤场景")
    
    # 初始化函数调用器
    caller = GPTFunctionCaller(
        functions=[func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS[1]],  # 只使用货币转换函数
        function_map={"currency_convert": func_advanced.currency_convert}
    )
    
    # 场景1：美元到人民币转换
    print_test_header("场景1：美元到人民币转换")
    user_input = "把100美元换算成人民币"
    print_user_input(user_input)
    
    response = caller.call_with_conversation(
        user_input,
        system_message="请使用currency_convert函数将100美元转换为人民币。"
    )
    
    print_request_data(caller.last_request)
    print_api_response(response.model_dump())
    print_execution_time(caller.execution_time)
    
    # 验证美元到人民币转换结果
    assert response.choices[0].message.tool_calls is not None, "没有函数调用"
    tool_calls = response.choices[0].message.tool_calls
    assert len(tool_calls) == 1, "应该只有1个函数调用"
    assert tool_calls[0].function.name == "currency_convert", "应该调用currency_convert"
    
    # 验证转换参数
    import json
    currency_call = json.loads(tool_calls[0].function.arguments)
    assert currency_call["amount"] == 100, "金额不正确"
    assert currency_call["from_currency"] == "USD", "源货币不正确"
    assert currency_call["to_currency"] == "CNY", "目标货币不正确"
    
    # 场景2：欧元到日元转换
    print_test_header("场景2：欧元到日元转换")
    user_input = "将50欧元换成日元"
    print_user_input(user_input)
    
    response = caller.call_with_conversation(
        user_input,
        system_message="请使用currency_convert函数将50欧元转换为日元。"
    )
    
    print_request_data(caller.last_request)
    print_api_response(response.model_dump())
    print_execution_time(caller.execution_time)
    
    # 验证欧元到日元转换结果
    assert response.choices[0].message.tool_calls is not None, "没有函数调用"
    tool_calls = response.choices[0].message.tool_calls
    assert len(tool_calls) == 1, "应该只有1个函数调用"
    assert tool_calls[0].function.name == "currency_convert", "应该调用currency_convert"
    
    # 验证转换参数
    currency_call = json.loads(tool_calls[0].function.arguments)
    assert currency_call["amount"] == 50, "金额不正确"
    assert currency_call["from_currency"] == "EUR", "源货币不正确"
    assert currency_call["to_currency"] == "JPY", "目标货币不正确"

if __name__ == "__main__":
    test_multisteps_currency() 
from exam_funcall.func_simple import get_current_time, calculate_circle_area, FUNCTION_DESCRIPTIONS as functions
from exam_funcall.function_caller import GPTFunctionCaller
from exam_funcall import func_advanced
from exam_funcall.function_caller.infra import (
    print_test_header,
    print_user_input,
    print_request_data,
    print_api_response,
    print_execution_time
)

def test_multisteps_mixed_functions():
    """测试混合函数的多步骤调用场景"""
    print_test_header("测试混合函数的多步骤调用")
    
    # 初始化混合函数调用器
    caller = GPTFunctionCaller(
        functions=[
            functions[0],  # get_current_time
            functions[1],  # calculate_circle_area
            func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS[0],  # get_weather
            func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS[1],  # currency_convert
            func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS[2],  # schedule_reminder
            func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS[3]   # search_restaurants
        ],
        function_map={
            "get_current_time": get_current_time,
            "calculate_circle_area": calculate_circle_area,
            "get_weather": func_advanced.get_weather,
            "currency_convert": func_advanced.currency_convert,
            "schedule_reminder": func_advanced.schedule_reminder,
            "search_restaurants": func_advanced.search_restaurants
        }
    )
    
    # 场景1：时间和天气多步骤查询
    print_test_header("场景1：时间和天气多步骤查询")
    user_input = "现在几点了？"
    print_user_input(user_input)
    
    # 步骤1.1：获取当前时间
    print_test_header("步骤1.1：获取当前时间")
    response = caller.call_with_conversation(
        user_input,
        system_message="请使用get_current_time函数获取当前时间。不要使用其他函数。"
    )
    
    print_request_data(caller.last_request)
    print_api_response(response.model_dump())
    print_execution_time(caller.execution_time)
    
    # 验证时间查询结果
    assert response.choices[0].message.tool_calls is not None, "没有函数调用"
    tool_calls = response.choices[0].message.tool_calls
    assert len(tool_calls) == 1, "应该只有1个函数调用"
    assert tool_calls[0].function.name == "get_current_time", "应该调用get_current_time"
    
    # 步骤1.2：查询北京天气
    print_test_header("步骤1.2：查询北京天气")
    user_input = "查查北京的天气"
    print_user_input(user_input)
    response = caller.call_with_conversation(
        user_input,
        system_message="请使用get_weather函数查询北京的天气。不要使用其他函数。"
    )
    
    print_request_data(caller.last_request)
    print_api_response(response.model_dump())
    print_execution_time(caller.execution_time)
    
    # 验证天气查询结果
    assert response.choices[0].message.tool_calls is not None, "没有函数调用"
    tool_calls = response.choices[0].message.tool_calls
    assert len(tool_calls) == 1, "应该只有1个函数调用"
    assert tool_calls[0].function.name == "get_weather", "应该调用get_weather"
    
    # 验证天气查询参数
    import json
    weather_call = json.loads(tool_calls[0].function.arguments)
    assert weather_call["city"] == "北京", "天气查询应该是北京"
    
    # 场景2：圆面积和货币转换多步骤查询
    print_test_header("场景2：圆面积和货币转换多步骤查询")
    user_input = "计算一个半径为10厘米的圆形桌子的面积"
    print_user_input(user_input)
    
    # 步骤2.1：计算圆面积
    print_test_header("步骤2.1：计算圆面积")
    response = caller.call_with_conversation(
        user_input,
        system_message="请使用calculate_circle_area函数计算半径为10的圆的面积。不要使用其他函数。"
    )
    
    print_request_data(caller.last_request)
    print_api_response(response.model_dump())
    print_execution_time(caller.execution_time)
    
    # 验证圆面积计算结果
    assert response.choices[0].message.tool_calls is not None, "没有函数调用"
    tool_calls = response.choices[0].message.tool_calls
    assert len(tool_calls) == 1, "应该只有1个函数调用"
    assert tool_calls[0].function.name == "calculate_circle_area", "应该调用calculate_circle_area"
    
    # 验证圆面积计算参数
    circle_call = json.loads(tool_calls[0].function.arguments)
    assert circle_call["radius"] == 10, "圆的半径应该是10"
    
    # 步骤2.2：进行货币转换
    print_test_header("步骤2.2：进行货币转换")
    user_input = "这个桌子价值100美元，请换算成人民币"
    print_user_input(user_input)
    response = caller.call_with_conversation(
        user_input,
        system_message="请使用currency_convert函数将100美元转换为人民币。不要使用其他函数。"
    )
    
    print_request_data(caller.last_request)
    print_api_response(response.model_dump())
    print_execution_time(caller.execution_time)
    
    # 验证货币转换结果
    assert response.choices[0].message.tool_calls is not None, "没有函数调用"
    tool_calls = response.choices[0].message.tool_calls
    assert len(tool_calls) == 1, "应该只有1个函数调用"
    assert tool_calls[0].function.name == "currency_convert", "应该调用currency_convert"
    
    # 验证货币转换参数
    currency_call = json.loads(tool_calls[0].function.arguments)
    assert currency_call["amount"] == 100, "金额应该是100"
    assert currency_call["from_currency"] == "USD", "源货币应该是USD"
    assert currency_call["to_currency"] == "CNY", "目标货币应该是CNY"

if __name__ == "__main__":
    test_multisteps_mixed_functions() 
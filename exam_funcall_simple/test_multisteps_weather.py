from exam_funcall_simple.function_caller import GPTFunctionCaller
from exam_funcall_simple import func_advanced
from exam_funcall_simple.function_caller.infra import (
    print_test_header,
    print_user_input,
    print_request_data,
    print_api_response,
    print_execution_time
)

def test_multisteps_weather():
    """测试天气查询的多步骤场景"""
    print_test_header("测试天气查询的多步骤场景")
    
    # 初始化函数调用器
    caller = GPTFunctionCaller(
        functions=[func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS[0]],  # 只使用天气查询函数
        function_map={"get_weather": func_advanced.get_weather}
    )
    
    # 场景1：查询国内城市天气
    print_test_header("场景1：查询国内城市天气")
    user_input = "北京今天天气怎么样？"
    print_user_input(user_input)
    
    # 第一次调用，使用tool_choice强制使用函数
    response = caller.call_with_conversation(
        user_input,
        system_message="请使用get_weather函数查询北京的天气。",
        tool_choice={"type": "function", "function": {"name": "get_weather"}}
    )
    
    print_request_data(caller.last_request)
    print_api_response(response.model_dump())
    print_execution_time(caller.execution_time)
    
    # 验证国内城市天气查询结果
    assert response.choices[0].message.tool_calls is not None, "没有函数调用"
    tool_calls = response.choices[0].message.tool_calls
    assert len(tool_calls) == 1, "应该只有1个函数调用"
    assert tool_calls[0].function.name == "get_weather", "应该调用get_weather"
    
    # 验证查询参数
    import json
    weather_call = json.loads(tool_calls[0].function.arguments)
    assert weather_call["city"] == "北京", "城市不正确"
    assert weather_call.get("country", "CN") == "CN", "国家代码不正确"
    
    # 场景2：查询国外城市天气
    print_test_header("场景2：查询国外城市天气")
    user_input = "查询东京(JP)的天气"
    print_user_input(user_input)
    
    # 第二次调用，使用tool_choice强制使用函数
    response = caller.call_with_conversation(
        user_input,
        system_message="请使用get_weather函数查询东京的天气。",
        tool_choice={"type": "function", "function": {"name": "get_weather"}}
    )
    
    print_request_data(caller.last_request)
    print_api_response(response.model_dump())
    print_execution_time(caller.execution_time)
    
    # 验证国外城市天气查询结果
    assert response.choices[0].message.tool_calls is not None, "没有函数调用"
    tool_calls = response.choices[0].message.tool_calls
    assert len(tool_calls) == 1, "应该只有1个函数调用"
    assert tool_calls[0].function.name == "get_weather", "应该调用get_weather"
    
    # 验证查询参数
    weather_call = json.loads(tool_calls[0].function.arguments)
    assert weather_call["city"] == "东京", "城市不正确"
    assert weather_call.get("country", "CN") == "JP", "国家代码不正确"

if __name__ == "__main__":
    test_multisteps_weather() 
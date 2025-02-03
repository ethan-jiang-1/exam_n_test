from exam_funcall_simple.func_simple import get_current_time, FUNCTION_DESCRIPTIONS as functions
from exam_funcall_simple.function_caller import GPTFunctionCaller
from exam_funcall_simple import func_advanced
from exam_funcall_simple.function_caller.infra import (
    print_test_header,
    print_user_input,
    print_request_data,
    print_api_response,
    print_execution_time
)

def test_singlestep_time_weather():
    """测试在单个步骤中查询时间和天气的场景"""
    print_test_header("测试时间和天气组合查询")
    
    # 初始化函数调用器，只包含需要的函数
    caller = GPTFunctionCaller(
        functions=[
            functions[0],  # get_current_time
            func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS[0]  # get_weather
        ],
        function_map={
            "get_current_time": get_current_time,
            "get_weather": func_advanced.get_weather
        }
    )
    
    # 测试输入
    user_input = "现在几点了？北京和东京的天气怎么样？"
    print_user_input(user_input)
    
    # 在一次调用中请求多个函数执行
    response = caller.call_with_conversation(
        user_input,
        system_message="这是一个多函数调用测试。请在一次调用中完成以下任务：1) 使用get_current_time获取当前时间；2) 使用get_weather查询北京的天气；3) 使用get_weather查询东京的天气，注意设置country参数为JP"
    )
    
    print_request_data(caller.last_request)
    print_api_response(response.model_dump())
    print_execution_time(caller.execution_time)
    
    # 验证结果
    assert response.choices[0].message.tool_calls is not None, "没有函数调用"
    tool_calls = response.choices[0].message.tool_calls
    assert len(tool_calls) == 3, "应该有3个函数调用"
    
    # 验证函数调用顺序和参数
    assert tool_calls[0].function.name == "get_current_time", "第一个调用应该是get_current_time"
    assert tool_calls[1].function.name == "get_weather", "第二个调用应该是get_weather"
    assert tool_calls[2].function.name == "get_weather", "第三个调用应该是get_weather"
    
    # 验证天气查询参数
    import json
    weather_call_1 = json.loads(tool_calls[1].function.arguments)
    weather_call_2 = json.loads(tool_calls[2].function.arguments)
    assert weather_call_1["city"] == "北京", "第一个天气查询应该是北京"
    assert weather_call_2["city"] == "东京" and weather_call_2["country"] == "JP", "第二个天气查询应该是东京，国家代码为JP"

if __name__ == "__main__":
    test_singlestep_time_weather() 
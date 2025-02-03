from exam_funcall.func_simple import get_current_time
from exam_funcall.function_caller import GPTFunctionCaller
from exam_funcall import func_advanced
from exam_funcall.function_caller.infra import (
    print_test_header,
    print_user_input,
    print_request_data,
    print_api_response,
    print_execution_time
)

def test_singlestep_time_weather():
    """测试时间和天气查询的单步场景"""
    try:
        print_test_header("测试时间和天气查询的单步场景")
        
        # 初始化函数调用器
        caller = GPTFunctionCaller(
            functions=[
                func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS[0],  # get_current_time
                func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS[1]  # get_weather
            ],
            function_map={
                "get_current_time": get_current_time,
                "get_weather": func_advanced.get_weather
            }
        )
        
        # 测试输入
        user_input = "现在几点了？北京和东京的天气怎么样？"
        print_user_input(user_input)
        
        # 执行调用
        response = caller.call_with_conversation(
            user_input,
            system_message="""你必须在一个响应中完成所有任务。你的响应必须是一个JSON对象，包含以下格式：
{
    "content": null,
    "tool_calls": [
        {
            "type": "function",
            "function": {
                "name": "get_current_time",
                "arguments": "{}"
            }
        },
        {
            "type": "function", 
            "function": {
                "name": "get_weather",
                "arguments": "{\"city\": \"北京\"}"
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "arguments": "{\"city\": \"东京\", \"country\": \"JP\"}"
            }
        }
    ]
}

你需要：
1. 使用 get_current_time 获取当前时间
2. 使用 get_weather 获取北京的天气
3. 使用 get_weather 获取东京的天气，注意设置country参数为JP

这三个函数调用必须在同一个响应的tool_calls数组中一起返回。
不要尝试使用parallel或其他并行执行方式。
每个函数调用都必须包含type字段，值为"function"。
你的响应必须是一个有效的JSON对象。"""
        )
        
        # 输出结果
        print_request_data(caller.last_request)
        print_api_response(response.model_dump())
        print_execution_time(caller.execution_time)
        
        # 验证结果
        if response.choices[0].message.tool_calls is None:
            raise AssertionError("没有函数调用")
        
        tool_calls = response.choices[0].message.tool_calls
        if len(tool_calls) != 3:
            raise AssertionError("应该有3个函数调用")
        
        # 验证函数调用顺序和参数
        if tool_calls[0].function.name != "get_current_time":
            raise AssertionError("第一个调用应该是get_current_time")
        if tool_calls[1].function.name != "get_weather":
            raise AssertionError("第二个调用应该是get_weather")
        if tool_calls[2].function.name != "get_weather":
            raise AssertionError("第三个调用应该是get_weather")
        
        # 验证天气查询参数
        import json
        weather_call_1 = json.loads(tool_calls[1].function.arguments)
        weather_call_2 = json.loads(tool_calls[2].function.arguments)
        if weather_call_1["city"] != "北京":
            raise AssertionError("第一个天气查询应该是北京")
        if weather_call_2["city"] != "东京" or weather_call_2["country"] != "JP":
            raise AssertionError("第二个天气查询应该是东京，国家代码为JP")
            
        print("\n测试通过!")
        return 0
    except AssertionError as e:
        print(f"\n测试失败: {str(e)}")
        return 1
    except Exception as e:
        print(f"\n测试出错: {str(e)}")
        return 2

if __name__ == "__main__":
    import sys
    sys.exit(test_singlestep_time_weather()) 
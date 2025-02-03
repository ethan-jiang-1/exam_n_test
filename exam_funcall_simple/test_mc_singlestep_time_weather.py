from exam_funcall_simple.func_simple import get_current_time, FUNCTION_DESCRIPTIONS as functions
from exam_funcall_simple.function_caller import GPTFunctionCaller
from exam_funcall_simple import func_advanced
from exam_funcall_simple.function_caller.infra import (
    print_test_header,
    print_user_input,
    print_system_message,
    print_request_data,
    print_api_response,
    print_function_result,
    print_execution_time,
    print_conversation_history,
    log_function_call,
    TestLogger
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
    caller.call_with_conversation(
        user_input,
        system_message="这是一个多函数调用测试。请在一次调用中完成以下任务：1) 使用get_current_time获取当前时间；2) 使用get_weather查询北京的天气；3) 使用get_weather查询东京的天气，注意设置country参数为JP"
    )
    
    print_request_data(caller.last_request)
    print_api_response(caller.raw_response)
    print_execution_time(caller.execution_time)

if __name__ == "__main__":
    test_singlestep_time_weather() 
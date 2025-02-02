from exam_funcall_simple.gpt_caller import GPTFunctionCaller
from exam_funcall_simple import func_simple
from exam_funcall_simple import func_advanced
from exam_funcall_simple.base_utils_test import print_test_header, print_user_input, print_request_data, print_api_response, print_execution_time

def test_singlestep_time_weather():
    """测试时间和天气组合查询"""
    print_test_header("测试时间和天气组合查询")
    
    # 初始化函数调用器
    caller = GPTFunctionCaller(
        functions=[
            func_simple.FUNCTION_DESCRIPTIONS[0],  # get_current_time
            func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS[0]  # get_weather
        ],
        function_map={
            "get_current_time": func_simple.get_current_time,
            "get_weather": func_advanced.get_weather
        }
    )
    
    # 测试输入
    user_input = "现在几点了？北京和东京的天气怎么样？"
    print_user_input(user_input)
    
    # 执行调用
    caller.call_with_functions(
        user_input,
        system_message="这是一个多函数调用测试。请在一次调用中完成以下任务：1) 使用get_current_time获取当前时间；2) 使用get_weather查询北京的天气；3) 使用get_weather查询东京的天气，注意设置country参数为JP"
    )
    
    # 输出结果
    print_request_data(caller.last_request)
    print_api_response(caller.raw_response)
    print_execution_time(caller.execution_time)

if __name__ == "__main__":
    test_singlestep_time_weather() 
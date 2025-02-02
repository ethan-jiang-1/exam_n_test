import json
from exam_funcall_simple.gpt_caller import GPTFunctionCaller
from exam_funcall_simple import func_simple

def test_time_query():
    """测试时间查询功能"""
    print("\n=== 测试时间查询 ===")
    
    caller = GPTFunctionCaller(
        functions=func_simple.FUNCTION_DESCRIPTIONS,
        function_map={
            "get_current_time": func_simple.get_current_time,
            "calculate_circle_area": func_simple.calculate_circle_area
        }
    )
    response = caller.call_with_functions("现在几点了？")
    print("Time query response:", json.dumps(response.model_dump(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_time_query() 
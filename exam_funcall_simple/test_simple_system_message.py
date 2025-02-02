import json
from exam_funcall_simple.gpt_caller import GPTFunctionCaller
from exam_funcall_simple import func_simple

def test_with_system_message():
    """测试带系统消息的调用"""
    print("\n=== 测试带系统消息的调用 ===")
    
    caller = GPTFunctionCaller(
        functions=func_simple.FUNCTION_DESCRIPTIONS,
        function_map={
            "get_current_time": func_simple.get_current_time,
            "calculate_circle_area": func_simple.calculate_circle_area
        }
    )
    response = caller.call_with_functions(
        "计算一个半径为10厘米的圆的面积",
        system_message="请用详细的步骤解释计算过程"
    )
    print("With system message response:", 
          json.dumps(response.model_dump(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_with_system_message() 
import json
from exam_funcall_simple.gpt_caller import GPTFunctionCaller
from exam_funcall_simple import func_simple

def test_with_history():
    """测试带历史记录的对话"""
    print("\n=== 测试带历史记录的对话 ===")
    
    caller = GPTFunctionCaller(
        functions=func_simple.FUNCTION_DESCRIPTIONS,
        function_map={
            "get_current_time": func_simple.get_current_time,
            "calculate_circle_area": func_simple.calculate_circle_area
        }
    )
    
    history = [
        {"role": "user", "content": "我想计算一个圆的面积"},
        {"role": "assistant", "content": "好的，请告诉我圆的半径"},
    ]
    
    response = caller.call_with_functions(
        "半径是7厘米",
        history=history
    )
    print("With history response:", 
          json.dumps(response.model_dump(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_with_history() 
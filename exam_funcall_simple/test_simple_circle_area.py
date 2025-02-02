import json
from exam_funcall_simple.gpt_caller import GPTFunctionCaller
from exam_funcall_simple import func_simple

def test_circle_area():
    """测试圆面积计算功能"""
    print("\n=== 测试圆面积计算 ===")
    
    caller = GPTFunctionCaller(
        functions=func_simple.FUNCTION_DESCRIPTIONS,
        function_map={
            "get_current_time": func_simple.get_current_time,
            "calculate_circle_area": func_simple.calculate_circle_area
        }
    )
    response = caller.call_with_functions("计算半径为5的圆的面积")
    print("Circle area response:", json.dumps(response.model_dump(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_circle_area() 
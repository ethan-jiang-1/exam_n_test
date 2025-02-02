import json
from exam_funcall_simple.gpt_caller import GPTFunctionCaller
from exam_funcall_simple import func_simple

def test_time_query():
    """测试时间查询功能"""
    caller = GPTFunctionCaller(
        functions=func_simple.FUNCTION_DESCRIPTIONS,
        function_map={
            "get_current_time": func_simple.get_current_time,
            "calculate_circle_area": func_simple.calculate_circle_area
        }
    )
    response = caller.call_with_functions("现在几点了？")
    print("Time query response:", json.dumps(response.model_dump(), indent=2, ensure_ascii=False))

def test_circle_area():
    """测试圆面积计算功能"""
    caller = GPTFunctionCaller(
        functions=func_simple.FUNCTION_DESCRIPTIONS,
        function_map={
            "get_current_time": func_simple.get_current_time,
            "calculate_circle_area": func_simple.calculate_circle_area
        }
    )
    response = caller.call_with_functions("计算半径为5的圆的面积")
    print("Circle area response:", json.dumps(response.model_dump(), indent=2, ensure_ascii=False))

def test_with_system_message():
    """测试带系统消息的调用"""
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

def test_with_history():
    """测试带历史记录的对话"""
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

def main():
    """运行所有测试"""
    print("\n=== Testing time query ===")
    test_time_query()
    
    print("\n=== Testing circle area calculation ===")
    test_circle_area()
    
    print("\n=== Testing with system message ===")
    test_with_system_message()
    
    print("\n=== Testing with history ===")
    test_with_history()

if __name__ == "__main__":
    main() 
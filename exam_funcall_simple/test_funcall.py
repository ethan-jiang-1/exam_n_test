import json
from exam_funcall_simple.gpt_caller import GPTFunctionCaller

def test_time_query():
    gpt_caller = GPTFunctionCaller()
    response = gpt_caller.call_with_functions("现在几点了？")
    print("Time query response:", json.dumps(response.model_dump(), indent=2, ensure_ascii=False))

def test_circle_area():
    gpt_caller = GPTFunctionCaller()
    response = gpt_caller.call_with_functions("计算半径为5的圆的面积")
    print("Circle area response:", json.dumps(response.model_dump(), indent=2, ensure_ascii=False))

def main():
    print("=== Testing time query ===")
    test_time_query()
    print("\n=== Testing circle area calculation ===")
    test_circle_area()

if __name__ == "__main__":
    main() 
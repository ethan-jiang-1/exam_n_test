from datetime import datetime
import math
from exam_funcall_simple.function_caller.infra import log_function_call

@log_function_call()
def get_current_time():
    """获取当前时间"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@log_function_call()
def calculate_circle_area(radius: float) -> float:
    """计算圆的面积"""
    return math.pi * radius * radius

# 函数描述，用于GPT function calling
FUNCTION_DESCRIPTIONS = [
    {
        "name": "get_current_time",
        "description": "获取当前的系统时间",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "calculate_circle_area",
        "description": "计算圆的面积",
        "parameters": {
            "type": "object",
            "properties": {
                "radius": {
                    "type": "number",
                    "description": "圆的半径"
                }
            },
            "required": ["radius"]
        }
    }
]

if __name__ == "__main__":
    # 测试函数功能
    print("Current time:", get_current_time())
    test_radius = 5
    print(f"Area of circle with radius {test_radius}:", calculate_circle_area(test_radius)) 
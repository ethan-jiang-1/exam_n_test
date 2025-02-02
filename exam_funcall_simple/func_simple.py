from datetime import datetime
import math
import colorlog
import logging
import functools
import json
from typing import Callable

def setup_logger():
    """设置彩色日志"""
    logger = colorlog.getLogger('function_logger')
    if not logger.handlers:
        handler = colorlog.StreamHandler()
        handler.setFormatter(colorlog.ColoredFormatter(
            '%(log_color)s[%(asctime)s] %(message)s%(reset)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        ))
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    return logger

logger = setup_logger()

def log_function_call(func: Callable) -> Callable:
    """记录函数调用的装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 记录函数调用
        func_name = func.__name__
        params = {
            "args": args,
            "kwargs": kwargs
        }
        logger.info("┌──────────── 函数调用 ────────────")
        logger.info(f"│ 函数名称: {func_name}")
        logger.info(f"│ 调用参数: {json.dumps(params, ensure_ascii=False)}")
        
        try:
            # 执行函数
            result = func(*args, **kwargs)
            # 记录返回值
            logger.info(f"│ 返回结果: {result}")
            logger.info("└─────────────────────────────")
            return result
        except Exception as e:
            logger.error(f"│ 执行错误: {str(e)}")
            logger.error("└─────────────────────────────")
            raise
    return wrapper

@log_function_call
def get_current_time():
    """获取当前时间"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@log_function_call
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
import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# 导入所有测试模块
from exam_funcall_simple.test_simple_time_query import test_simple_time_query
from exam_funcall_simple.test_simple_circle_area import test_simple_circle_area
from exam_funcall_simple.test_simple_conversation_history import test_simple_conversation_history
from exam_funcall_simple.test_simple_system_message import test_simple_system_message

from exam_funcall_simple.test_advanced_single_weather import test_advanced_single_weather
# TODO: 添加其他单步测试

from exam_funcall_simple.test_multisteps_mixed_functions import test_multisteps_mixed_functions
# TODO: 添加其他多步骤测试

def run_all_tests():
    """运行所有测试"""
    print("\n=== 运行简单函数单步测试 ===")
    test_simple_time_query()
    test_simple_circle_area()
    test_simple_conversation_history()
    test_simple_system_message()
    
    print("\n=== 运行高级函数单步测试 ===")
    test_advanced_single_weather()
    # TODO: 运行其他单步测试
    
    print("\n=== 运行多步骤测试 ===")
    test_multisteps_mixed_functions()
    # TODO: 运行其他多步骤测试

if __name__ == "__main__":
    run_all_tests() 
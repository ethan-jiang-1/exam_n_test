import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# 导入所有测试模块
# 简单函数单步测试
from exam_funcall_simple.test_simple_time_query import test_simple_time_query
from exam_funcall_simple.test_simple_circle_area import test_simple_circle_area
from exam_funcall_simple.test_simple_conversation_history import test_simple_conversation_history
from exam_funcall_simple.test_simple_system_message import test_simple_system_message

# 高级函数单步测试
from exam_funcall_simple.test_advanced_single_weather import test_advanced_single_weather
from exam_funcall_simple.test_advanced_single_currency import test_advanced_single_currency
from exam_funcall_simple.test_advanced_single_reminder import test_advanced_single_reminder
from exam_funcall_simple.test_advanced_single_restaurant import test_advanced_single_restaurant

# 多步骤测试
from exam_funcall_simple.test_multisteps_mixed_functions import test_multisteps_mixed_functions
from exam_funcall_simple.test_multisteps_weather import test_multisteps_weather
from exam_funcall_simple.test_multisteps_currency import test_multisteps_currency
from exam_funcall_simple.test_multisteps_reminder import test_multisteps_reminder
from exam_funcall_simple.test_multisteps_restaurant import test_multisteps_restaurant

def run_all_tests():
    """运行所有测试"""
    print("\n=== 运行简单函数单步测试 ===")
    test_simple_time_query()
    test_simple_circle_area()
    test_simple_conversation_history()
    test_simple_system_message()
    
    print("\n=== 运行高级函数单步测试 ===")
    test_advanced_single_weather()
    test_advanced_single_currency()
    test_advanced_single_reminder()
    test_advanced_single_restaurant()
    
    print("\n=== 运行多步骤测试 ===")
    test_multisteps_mixed_functions()
    test_multisteps_weather()
    test_multisteps_currency()
    test_multisteps_reminder()
    test_multisteps_restaurant()

if __name__ == "__main__":
    run_all_tests() 
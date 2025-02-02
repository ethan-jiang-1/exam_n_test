from exam_funcall_simple.test_simple_time_query import test_time_query
from exam_funcall_simple.test_simple_circle_area import test_circle_area
from exam_funcall_simple.test_simple_system_message import test_with_system_message
from exam_funcall_simple.test_simple_conversation_history import test_with_history

def run_all_simple_tests():
    """运行所有简单函数测试"""
    print("\n=== 运行所有简单函数测试 ===\n")
    
    # 运行时间查询测试
    test_time_query()
    
    # 运行圆面积计算测试
    test_circle_area()
    
    # 运行系统消息测试
    test_with_system_message()
    
    # 运行对话历史测试
    test_with_history()
    
    print("\n=== 所有简单函数测试完成 ===")

if __name__ == "__main__":
    run_all_simple_tests() 
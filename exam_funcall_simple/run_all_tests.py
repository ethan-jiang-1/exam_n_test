from exam_funcall_simple.run_simple_tests import run_all_simple_tests
from exam_funcall_simple.run_advanced_tests import run_all_advanced_tests
from exam_funcall_simple.test_mixed_functions import test_mixed_functions

def run_all_tests():
    """运行所有测试，包括简单函数、高级函数和混合函数测试"""
    print("\n" + "="*50)
    print("开始运行所有测试")
    print("="*50)
    
    # 运行简单函数测试
    print("\n" + "-"*30)
    print("运行简单函数测试")
    print("-"*30)
    run_all_simple_tests()
    
    # 运行高级函数测试
    print("\n" + "-"*30)
    print("运行高级函数测试")
    print("-"*30)
    run_all_advanced_tests()
    
    # 运行混合函数测试
    print("\n" + "-"*30)
    print("运行混合函数测试")
    print("-"*30)
    test_mixed_functions()
    
    print("\n" + "="*50)
    print("所有测试运行完成")
    print("="*50)

if __name__ == "__main__":
    run_all_tests() 
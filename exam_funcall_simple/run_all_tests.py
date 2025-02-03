"""运行所有测试"""
import os
import importlib
import traceback
from exam_funcall_simple.function_caller.infra import print_test_header

def run_all_tests():
    """运行所有测试文件"""
    print_test_header("运行所有测试")
    
    # 获取所有测试文件
    test_files = [
        f[:-3] for f in os.listdir(os.path.dirname(__file__))
        if f.startswith('test_') and f.endswith('.py')
    ]
    
    # 运行每个测试
    success = 0
    failed = 0
    for test_file in sorted(test_files):
        try:
            print(f"\n运行测试: {test_file}")
            module = importlib.import_module(f"exam_funcall_simple.{test_file}")
            
            # 查找并运行测试函数
            test_funcs = [
                f for f in dir(module)
                if f.startswith('test_') and callable(getattr(module, f))
            ]
            
            for func_name in test_funcs:
                test_func = getattr(module, func_name)
                test_func()
                success += 1
                
        except Exception as e:
            print(f"测试失败: {test_file}")
            print(f"错误信息: {str(e)}")
            print(traceback.format_exc())
            failed += 1
    
    # 打印统计信息
    print("\n测试完成!")
    print(f"成功: {success}")
    print(f"失败: {failed}")
    print(f"总计: {success + failed}")

if __name__ == "__main__":
    run_all_tests() 
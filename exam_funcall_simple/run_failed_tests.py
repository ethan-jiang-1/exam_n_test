import sys
from exam_funcall_simple.test_multisteps_reminder import test_multisteps_reminder
from exam_funcall_simple.test_multisteps_restaurant import test_multisteps_restaurant
from exam_funcall_simple.test_multisteps_weather import test_multisteps_weather
from exam_funcall_simple.test_advanced_single_reminder import test_advanced_single_reminder
from exam_funcall_simple.test_advanced_single_restaurant import test_advanced_single_restaurant
from exam_funcall_simple.test_mc_singlestep_circle_price import test_singlestep_circle_price
from exam_funcall_simple.test_mc_singlestep_meeting_restaurant import test_singlestep_meeting_restaurant
from exam_funcall_simple.test_mc_singlestep_mixed import test_singlestep_mixed
from exam_funcall_simple.test_mc_singlestep_time_weather import test_singlestep_time_weather
from exam_funcall_simple.test_multisteps_mixed_functions import test_multisteps_mixed_functions

def run_failed_tests():
    """运行失败的测试用例"""
    print("\n运行失败的测试用例:")
    print("=" * 80)
    
    failed_tests = [
        # (测试名称, 测试函数, 是否启用)
        ("test_multisteps_reminder", test_multisteps_reminder, False),  # 已通过，禁用
        ("test_multisteps_restaurant", test_multisteps_restaurant, False),  # 已通过，禁用
        ("test_multisteps_weather", test_multisteps_weather, True),
        ("test_advanced_single_reminder", test_advanced_single_reminder, True),
        ("test_advanced_single_restaurant", test_advanced_single_restaurant, True),
        ("test_mc_singlestep_circle_price", test_singlestep_circle_price, True),
        ("test_mc_singlestep_meeting_restaurant", test_singlestep_meeting_restaurant, True),
        ("test_mc_singlestep_mixed", test_singlestep_mixed, True),
        ("test_mc_singlestep_time_weather", test_singlestep_time_weather, True),
        ("test_multisteps_mixed_functions", test_multisteps_mixed_functions, True)
    ]
    
    success = 0
    failure = 0
    
    for test_name, test_func, enabled in failed_tests:
        if not enabled:
            print(f"\n跳过测试: {test_name} (已禁用)")
            continue
            
        print(f"\n运行测试: {test_name}")
        print("=" * 80 + "\n")
        try:
            test_func()
            success += 1
            print(f"\n测试成功: {test_name}")
        except AssertionError as e:
            failure += 1
            print(f"\n测试失败: {test_name}")
            print(f"错误信息: {str(e)}")
            print("Traceback:")
            import traceback
            traceback.print_exc()
        except Exception as e:
            failure += 1
            print(f"\n测试失败: {test_name}")
            print(f"错误信息: {str(e)}")
            print("Traceback:")
            import traceback
            traceback.print_exc()
    
    print("\n测试完成!")
    print(f"成功: {success}")
    print(f"失败: {failure}")
    print(f"总计: {success + failure}")
    
    return failure

if __name__ == "__main__":
    sys.exit(run_failed_tests()) 
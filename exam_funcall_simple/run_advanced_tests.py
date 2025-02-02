from exam_funcall_simple.test_advanced_weather import test_weather_query
from exam_funcall_simple.test_advanced_currency import test_currency_conversion
from exam_funcall_simple.test_advanced_reminder import test_reminder
from exam_funcall_simple.test_advanced_restaurant import test_restaurant_search

def run_all_advanced_tests():
    """运行所有高级函数测试"""
    print("\n=== 运行所有高级函数测试 ===\n")
    
    # 运行天气查询测试
    test_weather_query()
    
    # 运行货币转换测试
    test_currency_conversion()
    
    # 运行日程提醒测试
    test_reminder()
    
    # 运行餐厅搜索测试
    test_restaurant_search()
    
    print("\n=== 所有高级函数测试完成 ===")

if __name__ == "__main__":
    run_all_advanced_tests() 
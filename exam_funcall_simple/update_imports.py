"""更新所有测试文件的导入语句"""
import os
import re

def update_imports(file_path: str):
    """更新单个文件的导入语句"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 更新导入语句
    content = re.sub(
        r'from exam_funcall_simple.gpt_caller import GPTFunctionCaller',
        'from exam_funcall_simple.function_caller import GPTFunctionCaller',
        content
    )
    
    content = re.sub(
        r'from exam_funcall_simple.base_logger import .*',
        'from exam_funcall_simple.function_caller.infra import (\n'
        '    print_test_header,\n'
        '    print_user_input,\n'
        '    print_system_message,\n'
        '    print_request_data,\n'
        '    print_api_response,\n'
        '    print_function_result,\n'
        '    print_execution_time,\n'
        '    print_conversation_history,\n'
        '    log_function_call,\n'
        '    TestLogger\n'
        ')',
        content
    )
    
    # 更新函数调用
    content = re.sub(
        r'func_simple\.FUNCTION_DESCRIPTIONS',
        'functions',
        content
    )
    
    content = re.sub(
        r'func_simple\.get_current_time',
        'get_current_time',
        content
    )
    
    content = re.sub(
        r'func_simple\.calculate_circle_area',
        'calculate_circle_area',
        content
    )
    
    # 更新导入函数
    if 'get_current_time' in content and 'from exam_funcall_simple.func_simple import' not in content:
        content = 'from exam_funcall_simple.func_simple import get_current_time\n' + content
    
    if 'calculate_circle_area' in content and 'from exam_funcall_simple.func_simple import' not in content:
        content = 'from exam_funcall_simple.func_simple import calculate_circle_area\n' + content
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    """更新所有测试文件"""
    # 获取所有测试文件
    test_files = [f for f in os.listdir('.') if f.startswith('test_') and f.endswith('.py')]
    
    # 更新每个文件
    for file in test_files:
        print(f"Updating {file}...")
        update_imports(file)
        print(f"Updated {file}")

if __name__ == '__main__':
    main() 
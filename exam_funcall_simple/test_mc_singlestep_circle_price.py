from exam_funcall_simple.gpt_caller import GPTFunctionCaller
from exam_funcall_simple import func_simple
from exam_funcall_simple import func_advanced
from exam_funcall_simple.base_logger import print_test_header, print_user_input, print_request_data, print_api_response, print_execution_time, TestLogger
import json
from dataclasses import dataclass
from typing import Dict, Any, Protocol

class ContentTemplate(Protocol):
    """内容模板协议"""
    def render(self, **kwargs) -> str:
        """渲染模板"""
        ...

@dataclass
class SimpleTemplate:
    """简单的内容模板"""
    template: str

    def render(self, **kwargs) -> str:
        return self.template.format(**kwargs)

class CirclePriceContent:
    """圆形桌子价格相关的内容模板"""
    
    # 用户输入模板
    user_input = SimpleTemplate(
        "一张圆形餐桌半径是{radius}米，"
        "这张桌子在欧洲的价格是{amount}{currency_name}，"
        "请帮我计算桌子的面积，并把价格转换成{target_currency_name}。"
    )
    
    # 系统提示模板
    system_prompt = SimpleTemplate(
        "这是一个多函数调用测试。请在一次调用中完成以下任务：\n"
        "1) 使用calculate_circle_area计算半径为{radius}米的圆形桌子面积\n"
        "2) 使用currency_convert将{amount}{currency_code}转换为{target_currency_code}"
    )
    
    # 结果显示模板
    result = SimpleTemplate(
        "计算结果：\n"
        "1. 圆形餐桌面积：{area:.2f} 平方米\n"
        "2. 价格转换：{original_amount} {currency_name} = {converted_amount:.2f} {target_currency_name}\n"
        "   (使用汇率：1 {currency_name} = {rate:.3f} {target_currency_name})"
    )

@dataclass
class CirclePriceTest:
    """圆形桌子价格测试场景"""
    radius: float
    amount: float
    from_currency: str
    to_currency: str
    from_currency_name: str
    to_currency_name: str
    content: CirclePriceContent = CirclePriceContent()

    def get_user_input(self) -> str:
        """生成用户输入文本"""
        return self.content.user_input.render(
            radius=self.radius,
            amount=self.amount,
            currency_name=self.from_currency_name,
            target_currency_name=self.to_currency_name
        )

    def get_system_prompt(self) -> str:
        """生成系统提示文本"""
        return self.content.system_prompt.render(
            radius=self.radius,
            amount=self.amount,
            currency_code=self.from_currency,
            target_currency_code=self.to_currency
        )

    def format_result(self, area_result: float, price_result: Dict[str, Any]) -> str:
        """格式化最终结果"""
        return self.content.result.render(
            area=area_result,
            original_amount=price_result["original_amount"],
            currency_name=self.from_currency_name,
            converted_amount=price_result["converted_amount"],
            target_currency_name=self.to_currency_name,
            rate=price_result["rate"]
        )

def test_singlestep_circle_price():
    """测试圆形桌子面积计算和价格转换"""
    print_test_header("测试圆形桌子面积计算和价格转换")
    
    # 初始化测试场景
    test_case = CirclePriceTest(
        radius=0.8,
        amount=230,
        from_currency="EUR",
        to_currency="CNY",
        from_currency_name="欧元",
        to_currency_name="人民币"
    )
    
    # 初始化函数调用器
    function_map = {
        "calculate_circle_area": func_simple.calculate_circle_area,
        "currency_convert": func_advanced.currency_convert
    }
    
    caller = GPTFunctionCaller(
        functions=[
            func_simple.FUNCTION_DESCRIPTIONS[1],  # calculate_circle_area
            func_advanced.ADVANCED_FUNCTION_DESCRIPTIONS[1]  # currency_convert
        ],
        function_map=function_map
    )
    
    # 执行测试
    user_input = test_case.get_user_input()
    print_user_input(user_input)
    
    # 执行调用
    response = caller.call_with_functions(
        user_input,
        system_message=test_case.get_system_prompt()
    )
    
    # 输出结果
    print_request_data(caller.last_request)
    print_api_response(response.model_dump())
    print_execution_time(caller.execution_time)
    
    # 处理结果
    logger = TestLogger()
    
    if response.choices and response.choices[0].message.tool_calls:
        area_result = None
        price_result = None
        
        for tool_call in response.choices[0].message.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)
            
            if func_name == "calculate_circle_area":
                area_result = function_map[func_name](**func_args)
            elif func_name == "currency_convert":
                price_result = function_map[func_name](**func_args)
        
        if area_result is not None and price_result is not None:
            result_message = test_case.format_result(area_result, price_result)
            logger.print_panel("最终结果", result_message, "green")
            logger.print_success("所有计算已完成")
        else:
            logger.print_error("无法获取完整的计算结果")
    else:
        logger.print_error("函数调用失败")

if __name__ == "__main__":
    test_singlestep_circle_price() 
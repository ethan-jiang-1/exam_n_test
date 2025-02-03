from datetime import datetime, timedelta
from typing import List, Dict
from dataclasses import dataclass, asdict
from exam_funcall_simple.function_caller.infra import logger, log_function_call

# 高级函数描述
ADVANCED_FUNCTION_DESCRIPTIONS = [
    {
        "name": "get_weather",
        "description": "获取指定城市的天气信息",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名称"
                },
                "country": {
                    "type": "string",
                    "description": "国家代码（默认CN）",
                    "default": "CN"
                }
            },
            "required": ["city"]
        }
    },
    {
        "name": "currency_convert",
        "description": "货币转换功能",
        "parameters": {
            "type": "object",
            "properties": {
                "amount": {
                    "type": "number",
                    "description": "要转换的金额"
                },
                "from_currency": {
                    "type": "string",
                    "description": "源货币代码（如USD、CNY等）"
                },
                "to_currency": {
                    "type": "string",
                    "description": "目标货币代码（如USD、CNY等）"
                }
            },
            "required": ["amount", "from_currency", "to_currency"]
        }
    },
    {
        "name": "schedule_reminder",
        "description": "创建日程提醒，支持 ISO 格式时间和相对时间（如 '+2 hours'）",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "提醒事项标题"
                },
                "datetime_str": {
                    "type": "string",
                    "description": "提醒时间，支持两种格式：\n1. ISO格式: YYYY-MM-DDTHH:MM:SS\n2. 相对时间: +N hours/minutes/days"
                },
                "priority": {
                    "type": "string",
                    "description": "优先级",
                    "enum": ["low", "normal", "high"],
                    "default": "normal"
                },
                "participants": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "参与者邮箱列表"
                }
            },
            "required": ["title", "datetime_str"]
        }
    },
    {
        "name": "search_restaurants",
        "description": "搜索餐厅",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "位置"
                },
                "cuisine_type": {
                    "type": "string",
                    "description": "菜系类型"
                },
                "price_range": {
                    "type": "string",
                    "description": "价格范围 ($: 便宜, $$: 适中, $$$: 昂贵)",
                    "enum": ["$", "$$", "$$$"]
                },
                "min_rating": {
                    "type": "number",
                    "description": "最低评分 (0-5)",
                    "minimum": 0,
                    "maximum": 5,
                    "default": 4.0
                }
            },
            "required": ["location"]
        }
    }
]

@dataclass
class WeatherInfo:
    temperature: float
    humidity: float
    description: str
    location: str
    timestamp: str
    
    def to_dict(self) -> Dict:
        """转换为字典以便JSON序列化"""
        return asdict(self)

def log_function(func):
    """函数调用日志装饰器"""
    def wrapper(args_dict):
        logger.function_call(func.__name__, args_dict)
        result = func(**args_dict)
        logger.function_result(result)
        return result
    return wrapper

@log_function_call("get_weather")
def get_weather(city: str, country: str = "CN") -> WeatherInfo:
    """获取指定城市的天气信息"""
    # 这里模拟天气API调用
    weather_data = {
        "temp": 23.5,
        "humidity": 65,
        "desc": "晴朗",
        "city": city,
        "country": country,
    }
    return WeatherInfo(
        temperature=weather_data["temp"],
        humidity=weather_data["humidity"],
        description=weather_data["desc"],
        location=f"{city}, {country}",
        timestamp=datetime.now().isoformat()
    )

@log_function_call("currency_convert")
def currency_convert(amount: float, from_currency: str, to_currency: str) -> Dict:
    """货币转换功能"""
    # 模拟汇率API调用
    # 基准汇率（以CNY为基准）
    base_rates = {
        "USD": 0.155,  # 1 CNY = 0.155 USD
        "EUR": 0.127,  # 1 CNY = 0.127 EUR
        "JPY": 16.95,  # 1 CNY = 16.95 JPY
        "CNY": 1.0     # 1 CNY = 1.0 CNY
    }
    
    if from_currency not in base_rates or to_currency not in base_rates:
        raise ValueError(f"Unsupported currency: {from_currency} or {to_currency}")
    
    # 先转换为CNY，再转换为目标货币
    amount_in_cny = amount / base_rates[from_currency]
    converted = amount_in_cny * base_rates[to_currency]
    
    return {
        "original_amount": amount,
        "converted_amount": round(converted, 2),
        "from_currency": from_currency,
        "to_currency": to_currency,
        "rate": round(base_rates[to_currency] / base_rates[from_currency], 4),
        "timestamp": datetime.now().isoformat()
    }

@log_function_call("schedule_reminder")
def schedule_reminder(title: str, datetime_str: str, priority: str = "normal", participants: List[str] = None) -> Dict:
    """创建日程提醒"""
    # 解析时间字符串
    if datetime_str.startswith('+'):
        # 处理相对时间
        parts = datetime_str[1:].split()
        if len(parts) != 2:
            raise ValueError("Invalid relative time format. Expected format: '+N hours/minutes/days'")
        
        amount = int(parts[0])
        unit = parts[1].lower()
        
        if unit not in ['hours', 'minutes', 'days']:
            raise ValueError("Invalid time unit. Must be 'hours', 'minutes', or 'days'")
        
        delta = {
            'hours': timedelta(hours=amount),
            'minutes': timedelta(minutes=amount),
            'days': timedelta(days=amount)
        }[unit]
        
        reminder_time = datetime.now() + delta
    else:
        # 处理ISO格式时间
        reminder_time = datetime.fromisoformat(datetime_str)
    
    # 创建提醒
    reminder = {
        "title": title,
        "time": reminder_time.isoformat(),
        "priority": priority,
        "participants": participants or []
    }
    
    return reminder

@log_function_call("search_restaurants")
def search_restaurants(location: str, cuisine_type: str = None, price_range: str = None, min_rating: float = 4.0) -> List[Dict]:
    """搜索餐厅"""
    # 模拟餐厅数据库
    restaurants = [
        {
            "name": "北京烤鸭店",
            "cuisine": "中餐",
            "location": "北京",
            "price_range": "$$",
            "rating": 4.5
        },
        {
            "name": "意大利面屋",
            "cuisine": "意大利菜",
            "location": "北京",
            "price_range": "$$$",
            "rating": 4.2
        },
        {
            "name": "寿司之家",
            "cuisine": "日本料理",
            "location": "北京",
            "price_range": "$$$",
            "rating": 4.7
        }
    ]
    
    # 过滤结果
    results = []
    for restaurant in restaurants:
        if restaurant["location"] != location:
            continue
            
        if cuisine_type and restaurant["cuisine"] != cuisine_type:
            continue
            
        if price_range and restaurant["price_range"] != price_range:
            continue
            
        if restaurant["rating"] < min_rating:
            continue
            
        results.append(restaurant)
    
    return results

if __name__ == "__main__":
    # 测试天气功能
    weather = get_weather("北京")
    print("天气信息:", weather)
    
    # 测试货币转换
    conversion = currency_convert(100, "USD", "CNY")
    print("货币转换:", conversion)
    
    # 测试日程提醒（使用相对时间）
    reminder = schedule_reminder(
        "团队会议",
        "+2 hours",
        "high",
        ["team@example.com"]
    )
    print("日程提醒:", reminder)
    
    # 测试餐厅搜索
    restaurants = search_restaurants("北京", "中餐", "$$")
    print("餐厅搜索:", restaurants) 
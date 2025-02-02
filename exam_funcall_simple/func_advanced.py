from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class WeatherInfo:
    temperature: float
    humidity: float
    description: str
    location: str
    timestamp: str

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

def schedule_reminder(
    title: str,
    datetime_str: str,
    priority: str = "normal",
    participants: Optional[List[str]] = None
) -> Dict:
    """创建日程提醒"""
    try:
        reminder_time = datetime.fromisoformat(datetime_str)
        reminder = {
            "title": title,
            "time": reminder_time.isoformat(),
            "priority": priority,
            "participants": participants or [],
            "created_at": datetime.now().isoformat(),
            "status": "scheduled"
        }
        return reminder
    except ValueError as e:
        raise ValueError(f"Invalid datetime format. Please use ISO format (YYYY-MM-DDTHH:MM:SS). Error: {str(e)}")

def search_restaurants(
    location: str,
    cuisine_type: Optional[str] = None,
    price_range: Optional[str] = None,
    min_rating: float = 4.0
) -> List[Dict]:
    """搜索餐厅"""
    # 模拟餐厅数据库
    sample_restaurants = [
        {
            "name": "北京烤鸭店",
            "cuisine": "中餐",
            "price_range": "$$",
            "rating": 4.5,
            "location": "北京",
            "address": "王府井大街123号"
        },
        {
            "name": "Pasta House",
            "cuisine": "意餐",
            "price_range": "$$$",
            "rating": 4.3,
            "location": "北京",
            "address": "朝阳区国贸大厦"
        }
    ]
    
    # 过滤逻辑
    results = [r for r in sample_restaurants if r["location"] == location]
    if cuisine_type:
        results = [r for r in results if r["cuisine"] == cuisine_type]
    if price_range:
        results = [r for r in results if r["price_range"] == price_range]
    results = [r for r in results if r["rating"] >= min_rating]
    
    return results

# Function descriptions for GPT
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
                    "description": "原始货币代码 (USD, CNY, EUR, JPY)",
                    "enum": ["USD", "CNY", "EUR", "JPY"]
                },
                "to_currency": {
                    "type": "string",
                    "description": "目标货币代码 (USD, CNY, EUR, JPY)",
                    "enum": ["USD", "CNY", "EUR", "JPY"]
                }
            },
            "required": ["amount", "from_currency", "to_currency"]
        }
    },
    {
        "name": "schedule_reminder",
        "description": "创建日程提醒",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "提醒事项标题"
                },
                "datetime_str": {
                    "type": "string",
                    "description": "提醒时间 (ISO格式: YYYY-MM-DDTHH:MM:SS)"
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

if __name__ == "__main__":
    # 测试天气功能
    weather = get_weather("北京")
    print("天气信息:", weather)
    
    # 测试货币转换
    conversion = currency_convert(100, "USD", "CNY")
    print("货币转换:", conversion)
    
    # 测试日程提醒
    reminder = schedule_reminder(
        "团队会议",
        "2024-02-03T14:30:00",
        "high",
        ["team@example.com"]
    )
    print("日程提醒:", reminder)
    
    # 测试餐厅搜索
    restaurants = search_restaurants("北京", "中餐", "$$")
    print("餐厅搜索:", restaurants) 
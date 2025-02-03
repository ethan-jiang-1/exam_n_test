import pandas as pd
from typing import Dict

def _create_dataframes() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    创建奥运会金牌数和GDP数据的DataFrame
    
    Returns:
        tuple: (金牌DataFrame, GDP DataFrame)
    """
    medals_data = {
        '年份': [2012, 2012, 2012, 2016, 2016, 2016, 2020, 2020, 2020],
        '国家': ['USA', 'CHN', 'GBR', 'USA', 'CHN', 'GBR', 'USA', 'CHN', 'GBR'],
        '金牌': [46, 38, 29, 46, 26, 27, 39, 38, 22]
    }

    gdp_data = {
        '年份': [2012, 2012, 2012, 2016, 2016, 2016, 2020, 2020, 2020],
        '国家': ['USA', 'CHN', 'GBR', 'USA', 'CHN', 'GBR', 'USA', 'CHN', 'GBR'],
        'GDP（亿美元）': [16155, 8532, 2705, 18707, 11218, 2694, 21433, 14723, 2827]
    }

    return pd.DataFrame(medals_data), pd.DataFrame(gdp_data)

def _calculate_gdp_growth(df: pd.DataFrame) -> Dict[str, float]:
    """
    计算每个国家的GDP增长率
    
    Args:
        df: GDP数据的DataFrame
    
    Returns:
        Dict[str, float]: 国家与其GDP增长率的映射
    """
    gdp_growth = {}
    
    for country in df['国家'].unique():
        country_data = df[df['国家'] == country]
        min_gdp = country_data['GDP（亿美元）'].min()
        max_gdp = country_data['GDP（亿美元）'].max()
        
        if min_gdp > 0:  # 避免除以零
            gdp_growth[country] = ((max_gdp - min_gdp) / min_gdp) * 100
            
    return gdp_growth

def _get_medals_for_country(df: pd.DataFrame, country: str, year: int) -> int:
    """
    获取指定国家在指定年份的金牌数
    
    Args:
        df: 金牌数据的DataFrame
        country: 国家名称
        year: 年份
    
    Returns:
        int: 金牌数量
    """
    medals = df[(df['国家'] == country) & (df['年份'] == year)]['金牌'].sum()
    return medals

def analyze_olympic_medals_gdp_correlation() -> str:
    """
    分析GDP增长率最高的国家在奥运会上的金牌表现
    
    Returns:
        str: 分析结果描述
    """
    try:
        # 创建数据框
        medals_df, gdp_df = _create_dataframes()
        
        # 计算GDP增长率
        gdp_growth = _calculate_gdp_growth(gdp_df)
        
        # 找到GDP增长率最高的国家
        highest_growth_country = max(gdp_growth.items(), key=lambda x: x[1])[0]
        
        # 获取该国2020年的金牌数
        medals_2020 = _get_medals_for_country(medals_df, highest_growth_country, 2020)
        
        # 返回结果
        return f"在GDP增长率最高的国家中，{highest_growth_country}在2020年奥运会上获得的金牌总数是{medals_2020}枚。"
        
    except Exception as e:
        return f"分析过程出错: {str(e)}"

if __name__ == "__main__":
    result = analyze_olympic_medals_gdp_correlation()
    print(result)
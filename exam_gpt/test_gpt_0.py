import pandas as pd

# 创建表格1和表格2的数据帧
data1 = {
    '年份': [2012, 2012, 2012, 2016, 2016, 2016, 2020, 2020, 2020],
    '国家': ['USA', 'CHN', 'GBR', 'USA', 'CHN', 'GBR', 'USA', 'CHN', 'GBR'],
    '金牌': [46, 38, 29, 46, 26, 27, 39, 38, 22]
}

data2 = {
    '年份': [2012, 2012, 2012, 2016, 2016, 2016, 2020, 2020, 2020],
    '国家': ['USA', 'CHN', 'GBR', 'USA', 'CHN', 'GBR', 'USA', 'CHN', 'GBR'],
    'GDP（亿美元）': [16155, 8532, 2705, 18707, 11218, 2694, 21433, 14723, 2827]
}

df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

# 计算每个国家的GDP增长率
gdp_growth = {}
for country in df2['国家'].unique():
    gdp_data = df2[df2['国家'] == country]
    gdp_growth[country] = ((gdp_data['GDP（亿美元）'].max() - gdp_data['GDP（亿美元）'].min()) / gdp_data['GDP（亿美元）'].min()) * 100

# 找到GDP增长率最高的国家
highest_gdp_growth_country = max(gdp_growth, key=gdp_growth.get)

# 在GDP增长率最高的国家中找到2020年奥运会上获得的金牌总数
gold_medals_2020 = df1[(df1['国家'] == highest_gdp_growth_country) & (df1['年份'] == 2020)]['金牌'].sum()

print(f"在GDP增长率最高的国家中，{highest_gdp_growth_country}在2020年奥运会上获得的金牌总数是{gold_medals_2020}枚。")
# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/12/3
Description: <Brief description of the file>
"""
from public.other.time_way import TimeWay


def get_capacity_price(pricing_data, month):
    """
    获取指定月份的有效 capacityPrice
    :param pricing_data: 容量电价数据
    :param month: 月份 (格式为 YYYY-MM)
    :return: capacityPrice
    """
    for pricing in pricing_data:
        if pricing['effectiveTime'] <= month <= pricing['expirationTime']:
            return pricing['capacityPrice']
    return None

def calculate_and_compare(capacity, month, echart_data, pricing_data):
    """
    计算并比较容量 * capacityPrice 是否等于 series 中 name 为 容量*基准比例 对应月份的值
    :param capacity: 容量值
    :param month: 月份 (格式为 YYYY-MM)
    :param echart_data: 基本电费接口表返回的数据
    :param pricing_data: 容量电价数据
    :return: 比较结果
    """
    # 获取指定月份的有效 capacityPrice
    capacity_price = get_capacity_price(pricing_data, month)
    if capacity_price is None:
        return f"未找到 {month} 的有效 capacityPrice"

    # 计算 容量 * capacityPrice
    calculated_value = capacity * capacity_price


    # 获取 series 中 name 为 容量*基准比例 对应月份的值
    index = echart_data['category'].index(month)
    benchmark_value = echart_data['series'][5]['data'][index]

    print(calculated_value,benchmark_value)
    # 比较计算结果与基准值
    if calculated_value == benchmark_value:
        return True
    else:
        return False

# 示例数据
echart_data = {
    "category": [
        "2023-12", "2024-01", "2024-02", "2024-03", "2024-04", "2024-05", "2024-06", "2024-07", "2024-08", "2024-09", "2024-10", "2024-11"
    ],
    "series": [
        {"name": "最大需量", "unit": "MWh", "data": [None] * 10 + [99, 95]},
        {"name": "正向有功电量累计值", "unit": "Wh", "data": [None] * 10 + [605410, 526860]},
        {"name": "需量基本电费(元)", "unit": None, "data": [0] * 10 + [3500000, 3500000]},
        {"name": "容量", "unit": "Kwh", "data": [1000] * 12},
        {"name": "容量*基准比例", "unit": None, "data": [50000] * 12},
        {"name": "容量基本电费(元)", "unit": None, "data": [70000] * 12},
        {"name": "基本电费差(元)", "unit": None, "data": [70000] * 10 + [-3430000, -3430000]},
        {"name": "容需量成本转折点", "unit": None, "data": [875] * 12}
    ]
}

pricing_data = [
    {
        "id": "2",
        "demandPrice": 80,
        "capacityPrice": 70,
        "discountStandard": 112,
        "discountRatio": 60,
        "baseRatio": 50,
        "effectiveTime": "2023-11-01",
        "expirationTime": "2024-11-30"
    },
    {
        "id": "1",
        "demandPrice": 100,
        "capacityPrice": 90,
        "discountStandard": 1111,
        "discountRatio": 70,
        "baseRatio": 40,
        "effectiveTime": "2024-12-01",
        "expirationTime": "2024-12-31"
    }
]

# 测试
capacity = 1000

tslist = TimeWay().generate_date_or_timestamp_list(
    start_time_str="2024-02-01 00:00:00", end_time_str="2024-11-01 23:10:00",
    time_unit='month', output_format="data", if_nowtime=False)  # 获取时间列表 时间戳格式

for i in tslist:
    i=str(i)[0:7]
    print(i)

    result = calculate_and_compare(capacity, i, echart_data, pricing_data)
    print(f"计算结果: {result}")

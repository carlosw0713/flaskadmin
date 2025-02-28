# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2025/2/27
Description: <Brief description of the file>
"""

def parse_cron_expression(cron_expr: str):
    """
    解析cron表达式并验证格式
    :param cron_expr: cron表达式字符串
    :return: 解析结果或错误信息
    """
    # 定义各字段的正则表达式模式（支持6字段格式）
    patterns = [
        r'^\*|[0-9]+$',  # 秒/分/时 - 支持数字或*
        r'^\*|[0-5][0-9]$|([0-5]?[0-9]-[0-5]?[0-9])?(\|[\d-]+)?$',
        r'^\*|[0-2][0-9]|3[01]$',
        r'^\*|[1-3][0-1]|([0-9]|[0-9]-[0-9]|\|[\d-]+)?$',
        r'^\*|[1-12](\|[\d-]+)?$',
        r'^\*|0([1-7])?|7$'  # 星期几特殊处理（0=7）
    ]

    parts = cron_expr.split()

    # 结构验证
    if len(parts) not in (5, 6):
        return {"error": "Invalid cron expression format",
                "details": f"Expected 5 or 6 fields, got {len(parts)}"}

    # 字段非空验证
    for part in parts:
        if not part.strip():
            return {"error": "Cron field cannot be empty"}

    # 兼容旧版5字段格式（自动补全秒字段）
    if len(parts) == 5:
        parts.append('*')

    # 字段匹配验证
    try:
        second, minute, hour, day, month, dow = parts
    except ValueError:
        return {"error": "Invalid cron expression format",
                "details": f"Failed to unpack fields: {parts}"}

    # 正则匹配验证
    for i, (field, pattern) in enumerate(zip([second, minute, hour, day, month, dow], patterns)):
        if re.fullmatch(pattern, field) is None:
            return {"error": f"Invalid value in field {i + 1}",
                    "details": f"Field: {field}, Expected: {pattern}"}

    # 特殊值校验
    if month == '*':
        pass  # 合法
    elif not (1 <= int(month) <= 12):
        return {"error": "Invalid month value",
                "details": f"Month must be 1-12 or '*'"}

    if dow in ['0', '7']:
        pass  # 合法
    elif dow != '*':
        if not (1 <= int(dow) <= 6):
            return {"error": "Invalid day of week value",
                    "details": f"Day must be 1-6 or 0/7 (*)"}

    # return {
    #     "success": True,
    #     "second": second,
    #     "minute": minute,
    #     "hour": hour,
    #     "day": day,
    #     "month": month,
    #     "day_of_week": dow
    # }

    return  second, minute, hour, day, month, dow



#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/5/29 18:15
# @Author  : carlos
# @Email   : carlos.w.0713@outlook.com
# @file_tool    : string_changge.py
# @IDE     : PyCharm
# @REMARKS : 备注


def dict_to_str(data):
    result = []
    for key, value in data.items():
        if isinstance(value, list):
            # 将列表转换为逗号分隔的字符串，并用引号包围每个元素
            value_str = ','.join(f'{item}' for item in value)
        else:
            # 如果值不是列表，则直接添加（这里假设其他类型的值不需要特殊处理）
            value_str = str(value)
        result.append(f'{key}:"{value_str}"')

    # 将所有键值对连接成一个大的字符串，每个键值对之间用逗号和空格分隔
    return '\n'.join(result)


# 示例字典
data_dict = {
    "pm": ["1", "2"],
    "am": ["3"],
    "evening": "4"
}

# 转换并打印结果
converted_str = dict_to_str(data_dict)
print(converted_str)

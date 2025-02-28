# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/11/27
Description: <Brief description of the file>
"""

import functools
def log_function_details(description="No description"):
    """
    一个通用装饰器，用于输出函数的名称、入参、描述和返回值。
    :param description: 可选参数，描述信息，用于输出附加描述
    """
    def decorator(func):
        @functools.wraps(func)  # 保留原函数的元数据（如函数名、文档字符串）
        def wrapper(*args, **kwargs):
            # 输出函数名、入参和描述
            # print(f"方法名: {func.__name__} 入参: args={args}, kwargs={kwargs} ,返回值: {result}")
            # print(f"描述: {description}")
            # print(f"入参: args={args}, kwargs={kwargs}")

            # 执行原函数并获取返回值
            result = func(*args, **kwargs)

            # 输出返回值
            # print(f"返回值: {result}")
            print(f"方法名: {func.__name__} "
                  # f"入参: args={args},"
                  f" kwargs={kwargs} ,返回值: {result}")
            return result

        return wrapper

    return decorator

# 示例使用

@log_function_details("This is a TEST function")
def add(a, b):
    return a + b

@log_function_details("This function multiplies two numbers")
def multiply(a, b):
    return a * b

if __name__ == '__main__':

    # 测试函数
    add(3, 5)
    multiply(4, 6)

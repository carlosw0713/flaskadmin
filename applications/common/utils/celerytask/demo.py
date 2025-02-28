# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2025/2/25
Description: <Brief description of the file>
"""

import time
from celery import Celery
# from prefixed_redis import PrefixedStrictRedis

# 实例化Celery对象
celery = Celery(
    'tasks',  # 当前模块名
    broker='redis://39.105.205.148:6379/0',  # 使用redis为中间人
    backend='redis://39.105.205.148:6379/0'  # 结果存储
)

@celery.task()  # 使用异步任务装饰器task
def add(a, b):
    time.sleep(5)  # 休眠5秒
    return a + b

if __name__ == '__main__':
    print('开始执行')
    result = add.delay(2, 3)  # 调用add方法并使用delay延时函数
    print('执行结束')
    print(result)
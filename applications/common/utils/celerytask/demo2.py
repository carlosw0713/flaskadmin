# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2025/2/26
Description: <Brief description of the file>
"""
import time

from celery import shared_task,Celery

def init_celery():
    global celery
    celery = Celery(
        'demo2',
        backend='redis://39.105.205.148:6379/0',
        broker='redis://39.105.205.148:6379/0'
    )

    return celery


@shared_task
def task1(timenums):
    '''
    模拟执行异步任务
    '''

    time.sleep(timenums)
    print("任务1结束")
    return timenums


def runtask():

    taskobj=task1.delay(timenums=5)

    return "提前结束"


 # ✅ 确保先初始化Celery
celery = init_celery()
if __name__ == '__main__':

    print(runtask())

    print("6666")
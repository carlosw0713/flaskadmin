# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2025/2/28
Description: <Brief description of the file>
"""
from datetime import datetime



def demoscheduler(*args,**kwargs):


    print(f'调度任务测试脚本\n'
          f'当前时间{datetime.now()}\n '
          f'入参信息**kwargs:{kwargs}'
          f'入参信息*args:{args}')

    return f'调度任务测试脚本\n',f'当前时间{datetime.now()}\n ', f'入参信息**kwargs:{kwargs}\n',f'入参信息*args:{args}'

if __name__ == '__main__':
    demoscheduler()

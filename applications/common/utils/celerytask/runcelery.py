# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2025/2/25
Description: <Brief description of the file>
"""

from celery import Celery
from flask import Flask
celery = None

def init_celery():
    global celery
    celery = Celery(
        '异步处理',
        backend='redis://39.105.205.148:6379/0',
        broker='redis://39.105.205.148:6379/0'
    )

    return celery

if __name__ == '__main__':

    pass


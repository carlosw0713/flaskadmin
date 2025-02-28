"""
-*- coding: utf-8 -*-

@Author : carlos
@Time : 2023/captchacode/3 9:57
@file_tool : log_control.py.py
@talk : 干什么的？

日志封装，可设置不同等级的日志颜色
"""
import logging
import os.path
from logging import handlers
from typing import Text
import colorlog
import time


def root_dirname_number(path, number: int):
    '''
    获取输入路径的第几级父路径
    :param path:
    :param number:
    :return:
    '''

    if number == 0:
        return path
    for i in range(number):
        path = os.path.dirname(path)

    return path



class LogHandler:
    """ 日志打印封装"""
    # 日志级别关系映射
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }

    def __init__(
            self,
            filename: Text,
            level: Text = "info",
            when: Text = "D",
            # fmt: Text = "%(levelname)-8s%(asctime)s%(name)s:%(filename)s:%(lineno)d %(message)s"
            fmt: Text = "%(levelname)-8s%(asctime)s:%(filename)s:%(lineno)d %(message)s"
    ):
        self.logger = logging.getLogger(filename)

        formatter = self.log_color()

        # 设置日志格式
        format_str = logging.Formatter(fmt)
        # 设置日志级别
        self.logger.setLevel(self.level_relations.get(level))
        # 往屏幕上输出
        screen_output = logging.StreamHandler()
        # 设置屏幕上显示的格式
        screen_output.setFormatter(formatter)
        # 往文件里写入#指定间隔时间自动生成文件的处理器
        time_rotating = handlers.TimedRotatingFileHandler(
            filename=filename,
            when=when,
            backupCount=3,
            encoding='utf-8'
        )
        # 设置文件里写入的格式
        time_rotating.setFormatter(format_str)
        # 把对象加到logger里
        self.logger.addHandler(screen_output)
        self.logger.addHandler(time_rotating)
        # self.log_path = os.path.join('\\logs\\log.log')

    #
    @classmethod
    def log_color(cls):
        """ 设置日志颜色 """
        log_colors_config = {
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red',
        }

        # 设置打印格式 [2023-captchacode-03 10:53:56,965] [log_control.py:96] [ERROR]: 测试error
        formatter = colorlog.ColoredFormatter(
            '%(log_color)s[%(asctime)s] [%(filename)s:%(lineno)d] [%(levelname)s]: %(message)s',
            # '%(log_color)s[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s',
            log_colors=log_colors_config
        )
        return formatter


CURRENT_DIR = os.path.abspath(__file__)
BASE_DIR=root_dirname_number(path=CURRENT_DIR,number=3)
LOGS = os.path.join(BASE_DIR,"HLZY","logs" )

now_time_day = time.strftime("%Y-%m-%d", time.localtime())
INFO = LogHandler(os.path.join(LOGS,f"info-{now_time_day}.log"), level='info')
ERROR = LogHandler(os.path.join(LOGS,f"error-{now_time_day}.log"), level='error')
WARNING = LogHandler(os.path.join(LOGS,f"warning-{now_time_day}.log"))


if __name__ == '__main__':


    ERROR.logger.error("日志存ERROR表中,颜色为error")
    # INFO.logger.info("日志存在INFO表中,颜色为绿色")
    # WARNING.logger.warning("日志存在WARING中,颜色为黄色")
    WARNING.logger.warning(111)
    INFO.logger.error("日志存在INFO表中,颜色为红色")
    loc_str=1
    INFO.logger.info('通过xpath:{}成功找到元素'.format(loc_str))




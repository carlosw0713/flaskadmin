#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/16 16:36
# @Author  : carlos
# @Email   : carlos.w.0713@outlook.com
# @File    : fakerrandom.py
# @IDE     : PyCharm
# @REMARKS : 备注

"""
-*- coding: utf-8 -*-

@Author : carlos
@Time : 2023/11/21 16:27
@File : Faker_Random.py
@talk : 数据构造： 时间，随机值，其他数据？
"""


import re
import datetime
import random
from datetime import date, timedelta, datetime

from faker import Faker

class Fakerrandom:
    """ 正则替换 """
    def __init__(self):
        self.faker = Faker(locale='zh_CN')

    @classmethod
    def random_int(cls,min=0,max=100) -> int:
        """
        :return: 随机数
        """
        _data = random.randint(min, max)
        return _data

    def get_phone(self) -> int:
        """
        :return: 随机生成手机号码
        """
        phone = self.faker.phone_number()
        return phone

    def get_id_number(self) -> int:
        """

        :return: 随机生成身份证号码
        """

        id_number = self.faker.ssn()
        return id_number

    def get_female_name(self) -> str:
        """

        :return: 女生姓名
        """
        female_name = self.faker.name_female()
        return female_name

    def get_male_name(self) -> str:
        """

        :return: 男生姓名
        """
        male_name = self.faker.name_male()
        return male_name

    def get_email(self) -> str:
        """

        :return: 生成邮箱
        """
        email = self.faker.email()
        return email

    def generate_random_string(self,length,source='1234567890qwertyuio'):
        # 从给定的源字符串中随机选择字符
        random_string = ''.join(random.choice(source) for _ in range(length))

        return random_string


if __name__ == '__main__':
    task = Fakerrandom()
    print(task.generate_random_string(length=5))






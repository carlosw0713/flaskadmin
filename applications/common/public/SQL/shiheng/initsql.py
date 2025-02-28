#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/18 17:56
# @Author  : carlos
# @Email   : carlos.w.0713@outlook.com
# @File    : initsql.py
# @IDE     : PyCharm
# @REMARKS : 备注
import os

from public.file_tool.yaml_way import YamlWay
from settings.path import BASE_DIR


redisinfoyamlpath=f"{os.path.join(BASE_DIR,'public','SQL','shiheng','redisinfo.yaml')}"
redisinfo1=YamlWay().get_yaml_data(yaml_file=redisinfoyamlpath)
redisinfo=redisinfo1.get('test')
print(f'读取redis信息:{redisinfo}')
# print(redisinfo1)

mysqlinfoyamlpath=f"{os.path.join(BASE_DIR,'public','SQL','shiheng','mysqlinfo.yaml')}"
mysqlinfo1=YamlWay().get_yaml_data(yaml_file=mysqlinfoyamlpath)
mysqlinfo=mysqlinfo1.get('test')
print(f'读取mysql信息:{mysqlinfo}')

taosinfoyamlpath=f"{os.path.join(BASE_DIR,'public','SQL','shiheng','taosinfo.yaml')}"
taosinfo1=YamlWay().get_yaml_data(yaml_file=taosinfoyamlpath)
taosinfo=taosinfo1.get('test')
print(f'读取taos信息:{taosinfo}')
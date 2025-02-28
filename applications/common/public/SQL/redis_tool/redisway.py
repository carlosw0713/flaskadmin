#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/18 17:03
# @Author  : carlos
# @Email   : carlos.w.0713@outlook.com
# @File    : redisway.py
# @IDE     : PyCharm
# @REMARKS : 备注

import redis

from public.SQL.shiheng.initsql import redisinfo
host=redisinfo.get('host')
port=redisinfo.get('port')
password=redisinfo.get('password')
db=redisinfo.get('db')

class RedisOperator:
    def __init__(self):
        """
        初始化Redis连接。
        :param host: Redis服务器地址，默认为'localhost'
        :param port: Redis服务器端口，默认为6379
        :param db: 数据库索引，默认为0
        """
        # self.redis_conn = redis.Redis(host=host, port=port, db=db, password=password)
        self.redis_conn = redis.Redis(host=host, port=port, db=db)

        try:
            self.redis_conn.ping()  # 使用 ping 方法检查连接
            print("Redis 连接成功！")
        except redis.ConnectionError:
            print("无法连接到 Redis！")

    def execute_command(self,key, offset, value):
        """
        执行Redis命令。

        :param command: 要执行的Redis命令名称
        :param args: 命令的参数
        :return: 命令执行的结果
        """

        result = self.redis_conn.setbit(key, offset, value)
        # print(result) #执行便宜返回1，不执行偏移返回0
        return result


    def redishset(self,key, offset, value):
        '''
        设置位图命令
        :return:
        '''
        result = self.redis_conn.hset(key, offset, value)
        print(result)
        return result

# 使用示例
if __name__ == "__main__":

   task=RedisOperator()
   # task.execute_command('TEST',1,1)





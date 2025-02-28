#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/22 16:54
# @Author  : carlos
# @Email   : carlos.w.0713@outlook.com
# @File    : mysql_way.py
# @IDE     : PyCharm
# @REMARKS : 备注

from public.SQL.shiheng.initsql import mysqlinfo
host=mysqlinfo.get('host')
port=mysqlinfo.get('port')
user=mysqlinfo.get('user')
password=mysqlinfo.get('password')
db=mysqlinfo.get('db')



import pymysql

class MysqlWay:
    def __init__(self):
        self.host = host
        self.user = user
        self.password = password
        self.database = db
        # self.connection = None

        # print(host, port, user, password,db)

        self.connection = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            port=port,
            db=db,
            charset='utf8',

        )
    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()

    def execute_query(self, sql, return_as_dict=True):
        """执行SQL查询并返回结果

        Args:
            sql (str): SQL 查询语句。
            return_as_dict (bool, optional): 是否以字典列表形式返回结果，默认为 True。

        Returns:
            list: 查询结果，如果 return_as_dict 为 True，则返回字典列表；否则返回原始列表。
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                columns = [col[0] for col in cursor.description]  # 获取查询结果的列名
                results = cursor.fetchall()

                if return_as_dict:
                    formatted_results = [dict(zip(columns, row)) for row in results]
                else:
                    formatted_results = [list(row) for row in results]

            INFO.logger.info(f"执行查询语句：{sql} \n查询结果: {formatted_results}")
            return formatted_results
        except Exception as e:
            raise Exception(f"Error executing query: {e}")

    def execute_edit(self, sql):
        """执行SQL编辑操作（如INSERT, UPDATE, DELETE）"""
        INFO.logger.info(f"执行编译sql: {sql}")
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
            self.connection.commit()

        except Exception as e:
            print(f"Error executing edit operation: {e}")
            # self.connection.rollback()



if __name__ == '__main__':
    task=MysqlWay()
    # task.execute_query(sql="SELECT * FROM we_com_welcome_speech_material where brand_id =6533 ;")


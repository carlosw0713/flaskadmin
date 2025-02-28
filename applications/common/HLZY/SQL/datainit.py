# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/12/11
Description: <Brief description of the file>
"""
from public.SQL.mysql_tool.mysql_way import MysqlWay

class DataInit(MysqlWay):

    def seltablename(self):

        indicatorname='vkdcv'
        SQL=f"""SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'ems'
                  AND table_name LIKE '%{indicatorname}%';
                        """

        self.execute_query(sql=SQL,return_as_dict=False)


    def indicatorLibraryinit(self):
        ''''
        指标初始化
        '''

        sql =1


if __name__ == '__main__':
    task=DataInit()
    task.seltablename()
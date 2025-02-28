# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/12/20
Description: <Brief description of the file>
"""
from public.SQL.taos_tool.taos_way import TaosWay


class TaoSDevice(TaosWay):
    def deletetaosdata(self):
        '''
        删除taos数据
        :return:
        '''

        sql_list = """ DELETE FROM  `ems`.`col_6rtOTJ` WHERE `_timestamp` >= '2024-11-01' AND `_timestamp` <= '2025-01-11';
         DELETE FROM  `ems`.`cal_QMygKS` WHERE `_timestamp` >= '2024-11-01' AND `_timestamp` <= '2025-01-11';
        """

        sql_list=sql_list.split(';')
        for sql in sql_list:
            # print(sql)

            self.execute_edit(query=sql)

if __name__ == '__main__':
    taos = TaoSDevice()
    taos.deletetaosdata()

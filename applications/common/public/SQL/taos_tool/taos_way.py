# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/12/11
Description: <Brief description of the file>
"""
import taosrest

from public.logging_tool.log_control import *

from public.SQL.shiheng.initsql import taosinfo
host=taosinfo.get('host')
port=taosinfo.get('port')
user=taosinfo.get('user')
password=taosinfo.get('password')
db=taosinfo.get('db')


from taosrest import connect, TaosRestConnection, TaosRestCursor


# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/12/11
Description: <Brief description of the file>
"""
import taos
import taosrest
from public.SQL.shiheng.initsql import taosinfo
host=taosinfo.get('host')
port=taosinfo.get('port')
user=taosinfo.get('user')
password=taosinfo.get('password')

class TaosWay:

    def __init__(self):

        url=f"http://{host}:{port}"


        self.conn = taosrest.connect(url=url,
                                user=user,
                                password=password,
                                timeout=30)

        print(f"Connected to {url} successfully.")


    def execute_query(self, query):
        """执行查询操作"""
        if not self.conn:
            raise Exception("Not connected to the database. Call connect() first.")

        cursor = self.conn.cursor()
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            print(results)
            return results
        except Exception as e:
            print(f"Query execution failed: {e}")
            return None
        finally:
            cursor.close()

    def execute_edit(self, query):
        """执行编辑操作（插入、更新、删除）"""
        if not self.conn:
            raise Exception("Not connected to the database. Call connect() first.")

        cursor = self.conn.cursor()
        try:
            cursor.execute(query)
            INFO.logger.info(f"执行编译语句：{query}")
            self.conn.commit()
            # return True
        except Exception as e:
            print(f"Edit execution failed: {e}")
            # self.conn.rollback()
            # return False
        # finally:
        #     cursor.close()

if __name__ == '__main__':
    task = TaosWay()
    task.execute_query(query="SELECT `_timestamp`,`value` FROM  `ems`.`col_3b9Ru9` limit 200;DROP TABLE ems.`col_0eRipW`")
    # task.execute_edit(query="DROP TABLE `ems`.`cal_lesNl3`")
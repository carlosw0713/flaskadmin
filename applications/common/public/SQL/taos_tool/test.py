# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/12/11
Description: <Brief description of the file>
"""
import taos
import taosrest


# def create_connection():
#     # all parameters are optional.
#
#     host = "http://10.1.1.140"
#     port = 6060
#
#     conn = taos.connect(
#         user="root",
#         password="taosdata",
#         host=host,
#         port=port,
#     )
#     # try:
#     #     conn = taos.connect(
#     #         user="root",
#     #         password="taosdata",
#     #         host=host,
#     #         port=port,
#     #     )
#     #     print(f"Connected to {host}:{port} successfully.");
#     # except Exception as err:
#     #     print(f"Failed to connect to {host}:{port} , ErrMessage:{err}")
#     #     raise err
#     # finally:
#     if conn:
#         conn.close()
#
#
# import taosrest
class TaosRestClient:

    def __init__(self):
        conn = None
        host = "http://10.1.1.140"
        port = 6060
        url=f"{host}:{port}"


        self.conn = taosrest.connect(url=url,
                                user="root",
                                password="taosdata",
                                timeout=30)

        print(f"Connected to {url} successfully.")
        # a=conn.query("SELECT `_timestamp`,`value` FROM  `ems`.`cal_lesNl3` limit 200;DROP TABLE ems.`col_0eRipW`")


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
if __name__ == "__main__":
    task=TaosRestClient()
    task.execute_query(query='SELECT `_timestamp`,`value` FROM  `ems`.`cal_lesNl3` limit 200;DROP TABLE ems.`col_0eRipW`')

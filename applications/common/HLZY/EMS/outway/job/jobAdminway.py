# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/11/20
Description: <Brief description of the file>
"""

from public.file_tool.string_changge import data_dict
from applications.common.HLZY.IOT import *

class jobAdminway:
    def __init__(self):
        self.cookies = EMS_INFO.get('cookies')
        self.headers = EMS_INFO.get('headers')
        self.uri = EMS_INFO.get('uri')


    def jobAdmintrigger(self,json_data):
        '''
        调度任务执行
        :return:
        '''


        # json_data = {
        #     'id': '12',
        #     'executorParam': '2024-11-09',
        # }

        response = requestSession.post(f'{self.uri}/api/ems-biz-websvc/jobAdmin/trigger',
                                 cookies=self.cookies, headers=self.headers, json=json_data)

        resp = response.json()
        curl = generate_curl_command(response)
        if resp.get('code') == 0:
            INFO.logger.info(f"调度任务执行成功 {json_data.get('executorParam')}")
            # result = resp.get('data')
            return resp
        else:
            ERROR.logger.error(f"调度任务执行失败，返回信息：{resp}")

    def run_batchjobAdmintrigger(self):
        '''
        批量执行任务
        :return:
        '''

        tslist = TimeWay().generate_date_or_timestamp_list(
            start_time_str="2024-11-01 00:00:00", end_time_str="2025-01-10 23:10:00",
            time_unit='day', output_format="data", if_nowtime=False)  # 获取时间列表 时间戳格式

        for i in tslist:
            i=str(i).split(" ")[0]
            time.sleep(0.5)
            # print(i)


            #id 任务执行的id
            # self.jobAdmintrigger(json_data={'id': '12', 'executorParam': i})
            self.jobAdmintrigger(json_data={'id': '15', 'executorParam': i}) #9、10、11 日月年
            # self.jobAdmintrigger(json_data={'id': '10', 'executorParam': i}) #9、10、11 日月年
            # self.jobAdmintrigger(json_data={'id': '17', 'executorParam': i})

if __name__ == '__main__':
    task=jobAdminway()
    task.run_batchjobAdmintrigger()

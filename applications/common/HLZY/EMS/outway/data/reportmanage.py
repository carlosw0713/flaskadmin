# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/12/31
Description: <报表管理>
"""
from applications.common.HLZY.IOT import *
class ReportManage:

    def __init__(self):
        self.cookies = EMS_INFO.get('cookies')
        self.headers = EMS_INFO.get('headers')
        self.uri = EMS_INFO.get('uri')

    def reportdisplay(self):
        '''
        报表查看
        :return:
        '''

        json_data = {    'formId': '2',    'sheetIndex': '1',
                         'globalParamReqVOList': [
                             {'globalParamId': '1',
                              'globalParamVal': '2024-12-30',
                              'globalParamStr': '',}]}

        response = requestSession.post(f'{self.uri}/api/ems-report-websvc/report/display', cookies=self.cookies, headers=self.headers, json=json_data)

        resp=response.json()
        curl=generate_curl_command(response)
        if resp.get('code')==0:
            INFO.logger.info(f"报表查看成功，返回信息")
            return resp
        else:
            ERROR.logger.error(f"报表查看失败，返回信息：{resp}")
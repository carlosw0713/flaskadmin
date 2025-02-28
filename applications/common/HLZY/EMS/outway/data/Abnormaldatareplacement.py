# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/12/18
Description: <Brief description of the file>
"""
from applications.common.HLZY.IOT import *
class AbnormalDataReplacement:


    def __init__(self):
        self.cookies = EMS_INFO.get('cookies')
        self.headers = EMS_INFO.get('headers')
        self.uri = EMS_INFO.get('uri')

    def importantData(self):

        json_data = {"intervalValue": "", "intervalType": "default", "startTime": "2024-12-22 00:00:00",
                     "endTime": "2024-12-23 23:59:59", "energyId": "5", "businessAttributes": "重点数据",
                     "menuId": "1838770093501190146", "dimensionId": "5", "groupId": "12", "deviceCode": ""}

        response = requestSession.post(f'{self.uri}/api/ems-analysis-websvc/statistics/importantData',
                                       headers={self.headers}, data=json_data)

        resp = response.json()
        curl = generate_curl_command(response)
        if resp.get('code') == 0:
            INFO.logger.info(f"成功，返回信息：{resp}")
            return resp
        else:
            ERROR.logger.error(f"失败，返回信息：{resp}")
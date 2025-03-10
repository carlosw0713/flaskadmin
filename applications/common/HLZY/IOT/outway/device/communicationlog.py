# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2025/2/8
Description: <通信日志>
"""


from applications.common.HLZY import *

class Communicationlog():

    def __init__(self,auth_info):
        IOT_INFO=auth_info
        self.cookies = IOT_INFO.get('cookies')
        self.headers = IOT_INFO.get('headers')
        self.uri = IOT_INFO.get('uri')
    def iotdevicelogPage(self,params):
        '''
        通信日志信息
        :return:
        '''

        # params = {'size': '1000', 'current': '1', 'deviceCode': 'device20_YC',
        #           'startTime': '1738944000000','endTime': '1739030399000', }


        response = requestSession.get(f'{self.uri}/api/iot/device/logPage', params=params, cookies=self.cookies,
                                      headers=self.headers)

        resp = response.json()
        
        if resp.get('code') == 0:
            INFO.logger.info(f"通信日志信息查询成功，返回信息")
            return resp
        else:
            ERROR.logger.error(f"通信日志信息查询失败，返回信息：{resp}")

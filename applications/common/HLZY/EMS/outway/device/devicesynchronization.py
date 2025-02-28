# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/12/27
Description: <Brief description of the file>
"""

from applications.common.HLZY.IOT import *

class DeviceSynchronization:

    def __init__(self):

        self.cookies = EMS_INFO.get('cookies')
        self.headers = EMS_INFO.get('headers')
        self.uri = EMS_INFO.get('uri')

    def pointCodegetThingsModelsDetailPage(self,params):
        '''
        等待设备同步设备信息列表查询
        :param params:
        :return:
        '''

        # params = {'size': '100', 'current': '1', 'gatewayCode': 'HLGW1012426003188',
        #           'deviceCode': 'HLGW1012426003188_RS48511', 'subDeviceName': '包三线', }


        response = requestSession.get(f'{self.uri}/api/ems-biz-websvc/pointCode/getThingsModelsDetailPage', params=params,
                                      cookies=self.cookies, headers=self.headers)

        resp = response.json()
        curl = generate_curl_command(response)
        if resp.get('code') == 0:
            INFO.logger.info(f"等待设备同步设备信息查询成功，返回信息")
            return resp
        else:
            ERROR.logger.error(f"等待设备同步设备信息查询 失败，返回信息：{resp}")


    def pointCode(self,json_data,requsetmethod='POST'):
        '''
        同步设备点位信息
        :return:
        '''


        if requsetmethod=='POST':

            response = requestSession.post(f'{self.uri}/api/ems-biz-websvc/pointCode', cookies=self.cookies,
                                   headers=self.headers, json=json_data)
        elif requsetmethod=='PUT':
            response = requestSession.put(f'{self.uri}/api/ems-biz-websvc/pointCode', cookies=self.cookies,
                                   headers=self.headers, json=json_data)


        resp = response.json()
        curl = generate_curl_command(response)
        if resp.get('code') == 0:
            INFO.logger.info(f"同步设备点位信息成功，返回信息 入参:{json_data}")
            return resp
        else:
            ERROR.logger.error(f"同步设备点位信息 失败，返回信息：{resp}\n可以注意下请求方式")


if __name__ == '__main__':
    task=DeviceSynchronization()
    params={'size': '100', 'current': '1', 'gatewayCode': 'HLGW1012424003096',
              'deviceCode': 'HLGW1012426003096_RS48511', 'subDeviceName': '5#分变Ⅰ段', }
    task.pointCodegetThingsModelsDetailPage(params=params)
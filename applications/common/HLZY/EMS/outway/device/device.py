# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/11/21
Description: <Brief description of the file>
"""
from applications.common.HLZY.IOT import *

class DeviceData:

    def __init__(self):

        self.cookies = EMS_INFO.get('cookies')
        self.headers = EMS_INFO.get('headers')
        self.uri = EMS_INFO.get('uri')

    def devicepage(self,deviceCode=None,deviceName=None):
        '''
        设备列表信息
        :return:
        '''

        params = {'size': '1000', 'current': '1', "deviceCode": deviceCode, 'deviceName': deviceName, }
        response = requestSession.get(f'{self.uri}/api/ems-biz-websvc/device/page', params=params, cookies=self.cookies,
                                      headers=self.headers)

        resp = response.json()
        curl = generate_curl_command(response)
        if resp.get('code') == 0:
            INFO.logger.info(f"设备列表信息查询成功，返回信息：{resp}")
            return resp
        else:
            ERROR.logger.error(f"设备列表信息查询失败，返回信息：{resp}")

    def pointCodepage(self,deviceCode=None):
        '''
        pointCodepage： None 查的是点位类型列表，不为None查的是正确的
        设备数据绑定采集点 列表查询
        :return:
        '''

        params = {
            'size': '1000',
            'current': '1',
            'deviceCode': deviceCode,
        }

        response = requestSession.get(f'{self.uri}/api/ems-biz-websvc/pointCode/page', params=params,
                                cookies=self.cookies, headers=self.headers)

        resp = response.json()

        # 增加判断
        selcount=int(resp.get('data').get('total')//1000)
        if selcount>=1:
            for i in range(2,selcount+2):
                params = {
                    'size': '1000',
                    'current': f'{i}',
                    'deviceCode': deviceCode,
                }

                response = requestSession.get(f'{self.uri}/api/ems-biz-websvc/pointCode/page', params=params,
                                              cookies=self.cookies, headers=self.headers)
                resp['data']['records'].extend(response.json().get('data').get('records'))
        else:
            print("数据少于1000")


        curl = generate_curl_command(response)
        if resp.get('code') == 0:
            INFO.logger.info(f"设备数据绑定采集点 列表查询")
            # result = resp.get('data').get('records')
            return resp
        else:
            ERROR.logger.error(f"设备数据绑定采集点查询失败，返回信息：{resp}")

    def calPointCodedetails(self,calPointCodeId):
        '''
        计算点详情信息
        :param calPointCodeId:计算点的Id
        :return:
        '''

        response = requestSession.get(f'{self.uri}/api/ems-biz-websvc/calPointCode/details/{calPointCodeId}', cookies=self.cookies,
                                      headers=self.headers)

        resp = response.json()
        curl = generate_curl_command(response)
        if resp.get('code') == 0:
            INFO.logger.info(f"计算点详情信息 成功，返回信息：{resp}")
            return resp
        else:
            ERROR.logger.error(f"计算点详情信息 失败，返回信息：{resp}")

    def calpointCodepage(self, deviceCode=None):
        '''
        pointCodepage： None 查的是点位类型列表，不为None查的是正确的
        设备数据绑定计算点 列表查询
        :return:
        '''

        params = {
            'size': '1000',
            'current': '1',
            'deviceCode': deviceCode,
        }

        response = requestSession.get(f'{self.uri}/api/ems-biz-websvc/calPointCode/page', params=params,
                                cookies=self.cookies, headers=self.headers)

        resp = response.json()
        curl = generate_curl_command(response)
        if resp.get('code') == 0:
            INFO.logger.info(f"设备数据绑定计算点 列表查询")
            # result = resp.get('data').get('records')
            return resp
        else:
            ERROR.logger.error(f"设备数据绑定计算点，返回信息：{resp}")

    def pointCodehistoryData(self,params):
        '''
        点位历史数据查询
        :return:
        '''

        # params = {'pointCode': 'cal_ywAMRT', 'startTime': '1734451200420', 'endTime': '1734485758420',
        #           'intervalType': 'default', }
        response = requestSession.get(f'{self.uri}/api/ems-biz-websvc/pointCode/historyData', params=params,
                                      cookies=self.cookies, headers=self.headers)

        resp = response.json()
        curl = generate_curl_command(response)
        if resp.get('code') == 0:
            INFO.logger.info(f"点位历史数据查询成功，")
            return resp
        else:
            ERROR.logger.error(f"点位历史数据查询失败，返回信息：{resp}")

    def calPointCode(self, json_data):
        '''
        新增计算点数据
        :return:
        '''

        response = requestSession.post(f'{self.uri}/api/ems-biz-websvc/calPointCode', cookies=self.cookies,
                                 headers=self.headers, json=json_data)


        resp = response.json()
        curl = generate_curl_command(response)
        if resp.get('code') == 0:
            INFO.logger.info(f"新增计算点数据成功,{json_data.get('pointName')}")
            result = resp.get('data')
            return result
        else:
            ERROR.logger.error(f"新增计算点数据失败，返回信息：{resp},\n{json_data}")





if __name__ == '__main__':
    task=DeviceDataWay()

    task.run_batchaddcalPointCode()





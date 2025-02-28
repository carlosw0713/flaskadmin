# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/12/3
Description: <Brief description of the file>
"""
from applications.common.HLZY.IOT import *
class ElectricCharge:

    def __init__(self):
        self.cookies = EMS_INFO.get('cookies')
        self.headers = EMS_INFO.get('headers')
        self.uri = EMS_INFO.get('uri')
    def electricityPricelist(self,params=None):
        '''
        容需量电价
        :return:
        '''
        if params is None:
            params = {    'size': '100',    'current': '1',    'queryDate': '',}

        response = requestSession.get(f'{self.uri}/api/ems-biz-websvc/electricityPrice/list',
                                      params=params, cookies=self.cookies, headers=self.headers)

        resp=response.json()
        curl=generate_curl_command(response)
        if resp.get('code')==0:
            INFO.logger.info(f"容需量电价查询成功，返回信息：{resp}")
            return resp
        else:
            ERROR.logger.error(f"容需量电价查询失败，返回信息：{resp}")


    def getBasicCharge(self,json_data=None):
        '''
        基本电费分析列表查询
        :return:
        '''

        if json_data is None:
            json_data = {    'startTime': '2024-12',
                             'endTime': '2025-1',
                             'energyId': '11',
                             'energyDimensionId': '4',
                             'menuId': '1863426873777778690',
                             'dimensionId': '5',
                             'groupId': '13',}

        response = requestSession.post(f'{self.uri}/api/ems-analysis-websvc/cumulativeAnalysis/getBasicCharge', cookies=self.cookies, headers=self.headers, json=json_data)


        resp=response.json()
        curl=generate_curl_command(response)
        if resp.get('code')==0:
            INFO.logger.info(f"成功，返回信息：{resp}")
            return resp
        else:
            ERROR.logger.error(f"失败，返回信息：{resp}")
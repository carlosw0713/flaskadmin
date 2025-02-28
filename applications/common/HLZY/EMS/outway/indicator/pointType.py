# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/12/9
Description: <Brief description of the file>
"""
from applications.common.HLZY.IOT import *
class PointType:

    def __init__(self):
        self.cookies = EMS_INFO.get('cookies')
        self.headers = EMS_INFO.get('headers')
        self.uri = EMS_INFO.get('uri')


    def pointTypepage(self):
        '''
        点位类型列表
        :return:
        '''

        params = {    'size': '100',    'current': '1',}
        response = requestSession.get(f'{self.uri}/api/ems-biz-websvc/pointType/page', params=params, cookies=self.cookies, headers=self.headers)

        resp=response.json()
        curl=generate_curl_command(response)
        if resp.get('code')==0:
            INFO.logger.info(f"点位类型列表查询成功，返回信息：{resp}")
            return resp
        else:
            ERROR.logger.error(f"点位类型列表查询失败，返回信息：{resp}")

    def pointTypeadd(self,json_data):
        '''
        点位类型新增
        :return:
        '''

        # json_data = {    'id': '',    'pointTypeName': '测试创建',    'pointTypeUnitIdList': [        '1023',        '1024',        '1025',        '1026',        '1027',        '1556',    ],}

        response = requestSession.post(f'{self.uri}/api/ems-biz-websvc/pointType/add', cookies=self.cookies, headers=self.headers, json=json_data)

        resp=response.json()
        curl=generate_curl_command(response)
        if resp.get('code')==0:
            INFO.logger.info(f"点位类型新增成功，返回信息：{resp}")
            return resp
        else:
            ERROR.logger.error(f"点位类型新增失败，返回信息：{resp}")
# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/11/28
Description: <Brief description of the file>
"""
from applications.common.HLZY.IOT import *
class ManualEmploymentData:

    def __init__(self):
        self.cookies = EMS_INFO.get('cookies')
        self.headers = EMS_INFO.get('headers')
        self.uri = EMS_INFO.get('uri')


    def manualDataCellquerydata(self,json_data):
        '''
        手工录用数据查询
        :param json_data:
        :return:
        '''

        # json_data = {
        #     'type': 'DAY',
        #     'start': '2024-11-01',
        #     'end': '2024-11-28',
        #     'groupId': '6',
        #     'columns': [],
        # }

        response = requests.post(f'{self.uri}/api/ems-biz-websvc/manualDataCell/query/data',
                         cookies=self.cookies, headers=self.headers, json=json_data)

        resp = response.json()
        curl = generate_curl_command(response)
        if resp.get('code') == 0:
            INFO.logger.info(f"手工录用数据查询查询成功")
            return resp
        else:
            ERROR.logger.error(f"手工录用数据查询查询失败，返回信息：{resp}")


    def manualDataGrouptree(self):
        '''
        手工填报数据组织树
        :return:
        '''

        response = requests.get(f'{self.uri}/api/ems-biz-websvc/manualDataGroup/tree',
                                cookies=self.cookies, headers=self.headers)
        resp = response.json()
        curl = generate_curl_command(response)
        if resp.get('code') == 0:
            INFO.logger.info(f"手工填报数据组织树查询成功")
            return resp
        else:
            ERROR.logger.error(f"手工填报数据组织树查询失败，返回信息：{resp}")



    def unitConsumeAssessBasisadd(self,json_data):
        '''
        单耗考核指标管理 ，添加考核指标
        :return:
        '''

        # json_data = {    'organizeId': 14,    'productName': '产量点A',    'type': 'day',    'energyTypeId': 24,    'basisDate': '2024-11-01',    'basisValue': 1,    'unitId': 79,}
        response = requestSession.post(f'{self.uri}/api/ems-biz-websvc/unitConsumeAssessBasis/add', cookies=self.cookies, headers=self.headers, json=json_data)

        resp=response.json()
        curl=generate_curl_command(response)
        if resp.get('code')==0:
            INFO.logger.info(f"添加考核指标成功，请求信息：{json_data}")
            return resp
        else:
            ERROR.logger.error(f"添加考核指标失败，返回信息：{resp}")


    def unitConsumeAssessBasispage(self,params):

        # params = {    'size': '10000',
        #               'current': '1',
        #               # 'organizeId': '14',
        #               'productName': '',
        #               'energyTypeId': '',
        #               'type': 'day',
        #               'startTime': '2024-10-30',
        #               'endTime': '2024-11-29',}

        response = requestSession.get(f'{self.uri}/api/ems-biz-websvc/unitConsumeAssessBasis/page', params=params, cookies=self.cookies, headers=self.headers)

        resp=response.json()
        curl=generate_curl_command(response)
        if resp.get('code')==0:
            INFO.logger.info(f"成功，返回信息：{resp}")
            return resp
        else:
            ERROR.logger.error(f"失败，返回信息：{resp}")


    def unitConsumeAssessBasisdelete(self,id):
        """
        单耗考核指标管理 ，删除考核指标
        :return:
        """

        params = {    'id': id,}
        response = requestSession.delete(f'{self.uri}/api/ems-biz-websvc/unitConsumeAssessBasis/delete', params=params, cookies=self.cookies, headers=self.headers)

        resp=response.json()
        curl=generate_curl_command(response)
        result=resp.get('data')
        if resp.get('code')==0:
            INFO.logger.info(f"删除考核指标成功，请求信息：{params}")
            return result
        else:
            ERROR.logger.error(f"删除考核指标失败，返回信息：{resp}")

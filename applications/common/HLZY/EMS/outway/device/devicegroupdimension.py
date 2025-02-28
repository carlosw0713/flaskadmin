# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/11/28
Description: <Brief description of the file>
"""
from applications.common.HLZY.IOT import *
class DeviceGroupDimension:

    def __init__(self):

        self.cookies = EMS_INFO.get('cookies')
        self.headers = EMS_INFO.get('headers')
        self.uri = EMS_INFO.get('uri')

    def grouptree(self,dimensionId=1):
        '''
        设备分组维度
        :param dimensionId: 维度类型
        :return:
        '''

        params = {
            'size': '100',
            'current': '1',
            'dimensionId': dimensionId, # 1:组织维度 2:能源维度
        }

        response = requests.get(f'{self.uri}/api/ems-biz-websvc/group/tree',
                                params=params, cookies=self.cookies, headers=self.headers)

        resp = response.json()
        curl = generate_curl_command(response)
        if resp.get('code') == 0:
            INFO.logger.info(f"设备分组维度 列表查询成功")
            return resp
        else:
            ERROR.logger.error(f"设备分组维度 列表查询查询失败，返回信息：{resp}")

    def groupDeviceTree(self,dimensionId=1):
        '''
        设备组织树,
        :param dimensionId: 维度类型
        :return:
        '''

        params = {
            'dimensionId': dimensionId,
        }

        response = requests.get(f'{self.uri}/api/ems-biz-websvc/group/groupDeviceTree',
                                params=params, cookies=self.cookies, headers=self.headers)

        resp = response.json()
        curl = generate_curl_command(response)
        if resp.get('code') == 0:
            INFO.logger.info(f"设备组织树 列表查询成功")
            return resp
        else:
            ERROR.logger.error(f"设备组织树查询失败，返回信息：{resp}")
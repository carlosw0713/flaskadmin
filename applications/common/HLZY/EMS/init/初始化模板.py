# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/11/27
Description: <Brief description of the file>
"""
from applications.common.HLZY.IOT import *
class IndicatorComputeWay:

    def __init__(self):

        self.cookies = EMS_COOKIES
        self.headers = EMS_HEREADERS
        self.uri = EMS_URI

from applications.common.HLZY.IOT import *
class IndicatorComputeWay:

    def __init__(self):
        self.cookies = EMS_INFO.get('cookies')
        self.headers = EMS_INFO.get('headers')
        self.uri = EMS_INFO.get('uri')

from applications.common.HLZY.IOT import *
class IndicatorComputeWay:

    def __init__(self):
        self.cookies = IOT_INFO.get('cookies')
        self.headers = IOT_INFO.get('headers')
        self.uri = IOT_INFO.get('uri')

    def add(self):

        response={1:2}
        resp = response.json()
        curl = generate_curl_command(response)
        if resp.get('code') == 0:
            INFO.logger.info(f"设备数据绑定采集点 列表查询")
            return resp
        else:
            ERROR.logger.error(f"设备数据绑定采集点查询失败，返回信息：{resp}")
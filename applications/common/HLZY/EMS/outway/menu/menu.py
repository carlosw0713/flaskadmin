# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/12/9
Description: <Brief description of the file>
"""

from applications.common.HLZY.IOT import *
class Menu:

    def __init__(self):
        self.cookies = EMS_INFO.get('cookies')
        self.headers = EMS_INFO.get('headers')
        self.uri = EMS_INFO.get('uri')

    def scenelist(self):
        '''
        菜单关系列表
        :return:
        '''

        params = {'name': '', }
        response = requestSession.get(f'{self.uri}/api/ems-analysis-websvc/app-scene/list', params=params,
                                      cookies=self.cookies, headers=self.headers)

        resp = response.json()
        curl = generate_curl_command(response)
        if resp.get('code') == 0:
            INFO.logger.info(f"菜单关系列表成功，返回信息：{resp}")
            return resp
        else:
            ERROR.logger.error(f"菜单关系列表失败，返回信息：{resp}")


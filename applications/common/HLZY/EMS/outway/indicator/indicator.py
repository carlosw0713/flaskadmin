# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/11/27
Description: <Brief description of the file>
"""
from public.file_tool.string_changge import data_dict
from applications.common.HLZY.IOT import *

class Indicator:
    def __init__(self):
        self.cookies = EMS_INFO.get('cookies')
        self.headers = EMS_INFO.get('headers')
        self.uri = EMS_INFO.get('uri')

    def indicatorapppage(self, appSceneId=None):
        '''
        指标应用页面
        :return:
        '''
        params = {
            'size': '100',
            'current': '1',
            'appSceneId': appSceneId,
            'businessName':''
        }

        response = requestSession.get(f'{self.uri}/api/ems-analysis-websvc/indicator-app/page',
                                params=params, cookies=self.cookies, headers=self.headers)

        resp = response.json()
        curl = generate_curl_command(response)
        if resp.get('code') == 0:
            INFO.logger.info(f"指标应用页面查询成功")
            result = resp.get('data').get('records')
            return result
        else:
            ERROR.logger.error(f"指标应用页面查询失败，返回信息：{resp}")

    def sceneaddOrUpdate(self,json_data):
        '''
        指标应用页面添加
        :return:
        '''

        # json_data = {'id': '', 'sceneType': 'EMS菜单', 'menuId': '1839599538671718401', 'energyDimensionIds': '[]', }
        response = requestSession.post(f'{self.uri}/api/ems-analysis-websvc/app-scene/addOrUpdate', cookies=self.cookies,
                                       headers=self.headers, json=json_data)

        resp = response.json()
        curl = generate_curl_command(response)
        if resp.get('code') == 0:
            INFO.logger.info(f"指标应用页面添加成功，返回信息：{resp}")
            return resp
        else:
            ERROR.logger.error(f"指标应用页面添加失败，返回信息：{resp}")

    def icatorLibraryupdate(self,json_data):
        '''
        指标定义更新
        :param json_data:
        :return:
        '''
        # json_data = {'id': '122', 'name': '测试创建', 'code': 'M_QMYcC', 'type': 1, 'groupId': '43', 'unitId': '1023',
        #              'unit': 'kw/h', 'unitName': '千瓦时', 'decimalNumber': 3,
        #              'formula': 'SUM(PT_01333)-MAX(PT_01333)-MIN(PT_01333)-LAST(PT_01333)-FIRST(PT_01333)',
        #              'deviceGroupDimensionIds': '0,14,15', 'deviceGroupDimensionFunction': 'SUM', 'logicType': 1,
        #              'calculateWay': 1, 'taskId': '16', 'publishStatus': 0, 'contrastSwitch': 0, 'trialStatus': 0,
        #              'useCount': 0, 'description': None,
        #              'indicatorTimeWindowDTO': {'indicatorId': '122', 'windowType': 1, 'timeCycleDefineId': '3',
        #                                         'timeGroupDimensionFunction': 'SUM', }
        response = requestSession.put(f'{self.uri}/api/ems-biz-websvc/indicatorLibrary/update',
                                           cookies=self.cookies, headers=self.headers, json=json_data)

        resp = response.json()
        curl = generate_curl_command(response)
        if resp.get('code') == 0:
            INFO.logger.info(f"指标定义更新成功，入参：{json_data}")
            return resp
        else:
            ERROR.logger.error(f"指标定义更新失败，返回信息：{resp}")

    def indicatorLibrarypage(self,groupId=None,indicatortype=None,publishStatus=None):
        '''
        指标定义列表
        :return:
        '''
        params = {
            'size': '1000',
            'current': '1',
            'groupId': groupId,
            'type':indicatortype,
            'publishStatus':publishStatus
        }

        response = requestSession.get(f'{self.uri}/api/ems-biz-websvc/indicatorLibrary/page',
                                params=params, cookies=self.cookies, headers=self.headers)

        resp = response.json()
        curl = generate_curl_command(response)
        if resp.get('code') == 0:
            INFO.logger.info(f"指标定义页面查询成功")
            return resp
        else:
            ERROR.logger.error(f"指标定义页面查询失败，返回信息：{resp}")

    def icatorLibrarystatuschange(self,icatorLibraryId,statustype):
        '''
        指标定义的状态更改
        :param icatorLibraryId:
        :param statustype: publish
        :return:
        '''


        params = {'id': f'{icatorLibraryId}', }
        response = requestSession.put(f'{self.uri}/api/ems-biz-websvc/indicatorLibrary/{statustype}', params=params,
                                      cookies=self.cookies, headers=self.headers)

        resp = response.json()
        curl = generate_curl_command(response)
        if resp.get('code') == 0:
            INFO.logger.info(f"成功，返回信息：{resp}")
            return resp
        else:
            ERROR.logger.error(f"失败，返回信息：{resp}")

    def pointTypeUnitpage(self):
        '''
        点位类型单位管理列表
        :return:
        '''
        params = {
            'size': '100',
            'current': '1',
        }

        response = requestSession.get(f'{self.uri}/api/ems-biz-websvc/pointTypeUnit/page',
                                params=params, cookies=self.cookies, headers=self.headers)

        resp = response.json()
        curl = generate_curl_command(response)
        if resp.get('code') == 0:
            INFO.logger.info(f"点位类型单位管理列表查询成功")

            return resp
        else:
            ERROR.logger.error(f"点位类型单位管理列表查询失败，返回信息：{resp}")
    def indicatorappadd(self,json_data):
        '''
        指标应用添加
        :param json_data:
        :return:
        '''

        # json_data = {
        #     'id': '',
        #     'appSceneId': '8',
        #     'menuId': '1856260902562623489',
        #     'businessName': '正向有功',
        #     'businessAttributes': '正向有功',
        #     'businessAttributesCode': '正向有功',
        #     'indicatorId': '',
        #     'indicatorCode': 'M_j6iR7',
        #     'indicatorGroupId': '22',
        #     'remark': '',
        # }

        response = requestSession.post(f'{self.uri}/api/ems-analysis-websvc/indicator-app/add',
                                 cookies=self.cookies, headers=self.headers, json=json_data)

        resp = response.json()
        curl = generate_curl_command(response)
        if resp.get('code') == 0:
            INFO.logger.info(f"指标应用添加成功,请求信息{json_data}")
            result = resp.get('data')
            return result
        else:
            ERROR.logger.error(f"指标应用添加失败，返回信息：{resp}")

    def pointTypepage(self):
        '''
        点位类型列表
        :return:
        '''
        params = {
            'size': '100',
            'current': '1',
        }

        response = requestSession.get(f'{self.uri}/api/ems-biz-websvc/pointType/page', params=params,
                                cookies=self.cookies, headers=self.headers)

        resp = response.json()
        curl = generate_curl_command(response)
        if resp.get('code') == 0:
            INFO.logger.info(f"点位类型列表查询成功")
            # result = resp.get('data').get('records')
            return resp
        else:
            ERROR.logger.error(f"点位类型列表查询查询失败，返回信息：{resp}")

    def pointCodepage(self,deviceCode=None):
        '''
        pointCodepage： None 查的是点位类型列表，不为None查的是正确的
        设备数据绑采集点 列表查询
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
        curl = generate_curl_command(response)
        if resp.get('code') == 0:
            INFO.logger.info(f" 设备数据绑采集点 列表查询")

            return resp
        else:
            ERROR.logger.error(f" 设备数据绑采集点 列表查询失败，返回信息：{resp}")

    def calPointCodepage(self,deviceCode=None):
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

            return resp
        else:
            ERROR.logger.error(f"设备数据绑定计算点 列表查询失败，返回信息：{resp}")




    def icatorLibraryquerydata(self,json_data):
        ''''
        指标信息查询,内容查询
        '''

        # json_data = {    'indicatorId': '107',
        #                  'startTime': 1704038400621,
        #                  'endTime': 1735660799621,
        #                  'paramDTOS': [{ 'dimension': 'dd_0','groupId': 'dev_ele_bb',},{ 'dimension': 'dd_1','groupId': '36',}]
        #                  }

        response = requestSession.post(f'{self.uri}/api/ems-biz-websvc/indicatorLibrary/query/data', cookies=self.cookies, headers=self.headers, json=json_data)

        resp=response.json()
        curl=generate_curl_command(response)
        if resp.get('code')==0:
            INFO.logger.info(f"指标信息查询,内容查询成功，")
            return resp
        else:
            ERROR.logger.error(f"指标信息查询,内容查询失败，返回信息：{resp}")

    def indicatorLibraryadd(self,json_data):
        '''
        添加指标定义数据
        :return:
        '''

        # json_data = {'groupId': '42', 'name': '测试', 'type': 1, }
        response = requestSession.post(f'{self.uri}/api/ems-biz-websvc/indicatorLibrary/add', cookies=self.cookies,
                                       headers=self.headers, json=json_data)

        resp = response.json()
        curl = generate_curl_command(response)
        if resp.get('code') == 0:
            INFO.logger.info(f"添加指标定义数据成功，入参{json_data}")
            return resp
        else:
            ERROR.logger.error(f"添加指标定义数据失败，返回信息：{resp}")



if __name__ == '__main__':
    indicator = Indicator()
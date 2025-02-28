# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/11/19
Description: <Brief description of the file>
"""
from applications.common.HLZY.EMS.outway.user.userinfo import UserInfo
from public.file_tool.string_changge import data_dict
from applications.common.HLZY.EMS.outway.indicator.indicator import Indicator
from applications.common.HLZY.EMS.outway.menu.menu import Menu
from applications.common.HLZY.IOT import *


class IndicatorWay(Indicator,Menu,UserInfo):


    def dev_get_point_code(self,deviceCode=None):
        import requests

        cookies = {
            'access_token': '85140f68-4e6f-47e1-b3b7-f68360437dda',
            'tenant_id': '1864554814985269250',
        }

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Authorization': 'Bearer 85140f68-4e6f-47e1-b3b7-f68360437dda',
            'Connection': 'keep-alive',
            # Requests sorts cookies= alphabetically
            # 'Cookie': 'access_token=85140f68-4e6f-47e1-b3b7-f68360437dda; tenant_id=1864554814985269250',
            'Referer': 'https://saas-ems-test.heilansc.cn/indicator/indicatorApply',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'TENANT-ID': '1864554814985269250',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
            'X-Biz-App-Name': 'EMS',
            'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        params = {
            'size': '100',
            'current': '1',
            'appSceneId': '',
        }

        response = requests.get('https://saas-ems-test.heilansc.cn/api/ems-analysis-websvc/indicator-app/page',
                                params=params, cookies=cookies, headers=headers)


        # 注意 params中的size要是查所有
        return response.json().get('data').get('records')

    def  indicatorsceneadd(self,mockmenuNames):
        '''
        指标应用场景的添加
        :mockmenuNames: 需要创建的指标场景名称
        :return:
        '''


        indicatormenulist = self.scenelist().get('data')
        usermenuinfo = self.usermenuinfo()
        menuNames = [i.get('menuName') for i in indicatormenulist]
        # 判断场景是否存在,不存在则创建场景
        for mockmenuName in mockmenuNames:
            if mockmenuName not in menuNames:
                usermenuId = usermenuinfo.get(f'{mockmenuName}').get('menuId')
                json_data = {
                    "energyDimensionIds": "[]",
                    "id": "",
                    "menuId": f"{usermenuId}",
                    "sceneType": "EMS菜单"  # 暂时写死
                }

                self.sceneaddOrUpdate(json_data=json_data)


    def add_indicatorappby_devset2(self):
        '''
        1.调用复制接口，获取信息，包含菜单名，场景名称等等
        2.判断我们页面是否创建，没有创建则调用创建场景接口先创建，
        2.1 没有创建则调用创建场景接口先创建场景，
        2.2 已经创建则判断场景下是否创建相关业务名称，
        :return:
        '''

        mockdatainfolist=self.dev_get_point_code()

        indicatorapppage=self.indicatorapppage()

        meuninfolist = self.scenelist().get('data')

        mockmenuNames = list(set([i.get("menuName") for i in mockdatainfolist]))

        # 创建场景
        self.indicatorsceneadd(mockmenuNames=mockmenuNames)

        # 循环判断是否要创建指标应用
        for mockdatainfo in mockdatainfolist:
            mockmenuName=mockdatainfo.get('menuName')
            mockbusinessAttributes=mockdatainfo.get('businessAttributes')
            mockbusinessAttributesCode=mockdatainfo.get('businessAttributesCode')

            WhetherCreate=True

            for indicatorappinfo in indicatorapppage:
                businessAttributes = indicatorappinfo.get('businessAttributes')
                businessAttributesCode = indicatorappinfo.get('businessAttributesCode')
                menuName=indicatorappinfo.get('menuName')

                # print(mockmenuName,menuName,mockbusinessAttributes,businessAttributesCode)
                if mockmenuName==menuName and mockbusinessAttributesCode==businessAttributesCode:
                    WhetherCreate=False
                    break

            if WhetherCreate:

                # 根据名称找到 场景id和菜单id
                for meuninfo in meuninfolist:
                    menuId = meuninfo.get('menuId')
                    menuName = meuninfo.get('menuName')
                    appSceneId = meuninfo.get('id')

                    if menuName==mockmenuName:
                        break

                # 将mock信息中的业务名称、业务属性、属性编码啥的写入，然后创建场景
                json_data = {
                    'id': '',
                    'appSceneId': appSceneId,
                    'menuId': menuId,
                    'businessName': mockdatainfo.get('businessName'),
                    'businessAttributes': mockdatainfo.get('businessAttributes'),
                    'businessAttributesCode': mockdatainfo.get('businessAttributesCode'),
                    'indicatorId': '',
                    'indicatorCode': f"M_nlNbi",  #写死
                    'indicatorGroupId': f"2",  # 写死
                    'remark': '',
                }

                self.indicatorappadd(json_data=json_data)

    def batchicatorLibrarystatuschange(self):
        '''
        批量更新指标定义
        :return:
        '''

        indicatorLibrarylist=self.indicatorLibrarypage(groupId=3).get('data').get('records')

        indicatorLibraryIds=[i.get('id') for i in indicatorLibrarylist]

        for indicatorLibraryId in indicatorLibraryIds:
            self.icatorLibrarystatuschange(icatorLibraryId=indicatorLibraryId,statustype='publish')

    def add_indicatorappby_devset(self):
        '''
        使用dev的配置完成配置
        1.复制配置数据，生成调用配置应用列表的接口
        2.将接口数据解析，从新配置到该页面
        :return:
        '''

        appSceneId = "978" # 注意格式是字符串形式

        indicatorCode='M_dN7Wh'
        indicatorGroupId='45'

        meuninfolist=self.scenelist().get('data')
        for meuninfo in meuninfolist:
            id=meuninfo.get('id')
            if appSceneId==id:
                menuId=meuninfo.get('menuId')
                # return 1111
                break
        # menuId = 1839599045216047106  # 菜单id，可变的！！

        devindicator_list=self.dev_get_point_code()
        for devindicatorinfo in devindicator_list:
            businessName=devindicatorinfo.get('businessName')
            businessAttributes=devindicatorinfo.get('businessAttributes')
            businessAttributesCode=devindicatorinfo.get('businessAttributesCode')
            menuName=devindicatorinfo.get('menuName')

            json_data = {
                'id': '',
                'appSceneId': appSceneId,
                'menuId': menuId,
                'businessName': businessName,
                'businessAttributes': businessAttributes,
                'businessAttributesCode': businessAttributesCode,
                'indicatorId': '',
                'indicatorCode': f"{indicatorCode}", # M_m8vnk
                'indicatorGroupId': f"{indicatorGroupId}",  # 25
                'remark': '',
            }

            self.indicatorappadd(json_data=json_data)

    def bacthadd_indicatorapp(self):
        '''
        批量新增app应用
        已知：appSceneId、indicatorGroupId、menuId，指标应用、指标定义分类，菜单id
        获取一个指标应用已添加业务名称内容的列表
        根据 indicatorGroupId 指标定义列表 接口获取  获取indicatorCode和indicatorName，
        调用接口判断是否存在不存在则添加，不存在则添加
        :return:
        '''
        appSceneId=15
        indicatorGroupId=22
        menuId=1856260902562623489
        indicatorapppagelistinfo=self.indicatorapppage(appSceneId= appSceneId)
        indicatorLibrarypagelistinfo=self.indicatorLibrarypage(groupId=indicatorGroupId)
        indicator_dict={}

        businessNamelist=[]
        for j in indicatorapppagelistinfo:
            businessName=j.get('businessName')
            businessNamelist.append(businessName)

        for i in indicatorLibrarypagelistinfo:
            indicatorName=i.get('name')
            indicatorCode=i.get('code')
            if indicatorName not in businessNamelist:

                json_data={
                    'id': '',
                    'appSceneId': appSceneId,
                    'menuId': menuId,
                    'businessName': indicatorName,
                    'businessAttributes': indicatorName,
                    'businessAttributesCode': indicatorName,
                    'indicatorId': '',
                    'indicatorCode': indicatorCode,
                    'indicatorGroupId': indicatorGroupId,
                    'remark': '',
                }

                self.indicatorappadd(json_data=json_data)

    #暂时启用
    @log_function_details()
    def getindicatorpageinfo(self,appSceneId):
        '''
        获取指标应用中所有绑定指标的值
        :return: list
        '''

        # indicatorapppage=self.indicatorapppage(appSceneId= appSceneId)

        indicatorCodeList=[ i.get('indicatorCode') for i in self.indicatorapppage(appSceneId= appSceneId)]
        indicatorCodeList=list(set(indicatorCodeList))
        return indicatorCodeList

    @log_function_details()
    def getindicatortypevalue(self,indicatorCodeList):
        '''
        根据指标列表，提取其中点位类型的值
        :param groupId:
        :return:
        '''

                # 获取指标定义中信息，
        formulainfolist = [] #可能多个指标定义
        indicatorLibrarypagelistinfo=self.indicatorLibrarypage(groupId='').get('data').get('records')
        for i in indicatorLibrarypagelistinfo:
            code=i.get('code')
            formula=i.get('formula')
            if formula is None:#不为空
                continue
            if code in indicatorCodeList:
                formulainfolist.append(formula)

        formulainfolist=list(set(formulainfolist))
        # print(formulainfolist)

        # 过滤公式中的值，提取出对应的点位类型
        # pointTypeList=[]
        pointTypeCodelist=[]
        pointTypeNamelist=[]
        pointTypedict={}
        pointTypepageinfolist =self.pointTypepage().get('data').get('records')
        for i in pointTypepageinfolist:
            pointTypeCode=i.get('pointTypeCode')
            pointTypeName=i.get('pointTypeName')

            if pointTypeCode is None:#不为空
                continue
            if not pointTypeCode: #pointTypeCode 不为空
                continue
            for j in formulainfolist :

                if pointTypeCode in j :

                    pointTypeCodelist.append(pointTypeCode)
                    pointTypeNamelist.append(pointTypeName)
                    pointTypedict[pointTypeCode]=pointTypeName
                    break
        # print(pointTypeCodelist)

        return pointTypedict

    @log_function_details()
    def getobjmodeldata(self,deviceCode,pointTypeNamelist):
        '''
        根据设备和对应的点位，获取设备下对应点位的物模型值列表
        :return:
        '''

        identifierlist=[]

        pointCodepage=self.pointCodepage(deviceCode=deviceCode).get('data').get('records')
        calPointCodepage=self.calPointCodepage(deviceCode=deviceCode).get('data').get('records')
        pointCodepageinfolist=pointCodepage+calPointCodepage


        for i in pointCodepageinfolist:
            pointTypeName=i.get('pointTypeName')
            # print(pointTypeName,pointTypeNamelist)
            if pointTypeName in pointTypeNamelist:
                identifier=i.get('identifier')
                identifierlist.append(identifier)

        return identifierlist


if __name__ == '__main__':
    task=IndicatorWay()
    # result=task.indicatorapppage('')

    # task.add_indicatorappby_devset()

    # task.add_indicatorappby_devset2()

    # task.run_bacthadd_indicatorapp()

    # task.add_indicatorappby_devset()

    task.batchicatorLibrarystatuschange()
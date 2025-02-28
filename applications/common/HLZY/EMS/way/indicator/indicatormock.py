# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/12/6
Description: <Brief description of the file>
"""
from applications.common.HLZY.EMS.outway.indicator.indicator import Indicator
from applications.common.HLZY.EMS.outway.indicator.pointType import PointType
from public.file_tool.exl_way import read_excel_data
from public.logging_tool.log_control import *

class IndicatorMockWay(PointType,Indicator):


    def readindicatorinfoexl(self):
        '''
        读取exl表数据
        :return:
        '''
        file_name='D:\测试文档\EMS\苏南码头\数据配置总览.xlsx'
        sheet_name='点位类型1'
        exl_data=read_excel_data(file_name=file_name, sheet_name=sheet_name, datatype='list', loc=[2,1])

        pointTypeUnitpage=self.pointTypeUnitpage().get('data').get('records')
        pointTypeUnitdict={}
        for itme in pointTypeUnitpage:
            pointTypeUnitdict[itme.get('unit')]={
                'unitId':itme.get('id'),
                'unit':itme.get('unit'),
                'unitName':itme.get('unitName')
            }

        real_datadict= {}
        cycle_datadict= {}

        pointTypeUnit_Noneinfo={
            'unitId':"",
            'unit':"",
            'unitName':""
        }

        for i in exl_data:
            real_data=i[0] # 实时
            real_unit_info=pointTypeUnitdict.get(i[1],pointTypeUnit_Noneinfo) #单位id

            if real_data:
                real_datadict[real_data] = real_unit_info

            if len(i)>=3:
                cycle_data=i[2] # 周期
                cycle_unit_info=pointTypeUnitdict.get(i[3],pointTypeUnit_Noneinfo) #单位if

                if cycle_data:
                    cycle_datadict[cycle_data] = cycle_unit_info

        # sumdatalist=real_datalist+cycle_datalist
        return real_datadict, cycle_datadict

    def batchadd_PointType(self):
        '''
        批量新增点位类型
        根据数据表偶or其他配置先获取要创建的点位类型
        :return:
        '''

        pointTypeUnitIdList=[
  "972",
  "973",
  "974",
  "975",
  "976",
  "977",
  "978",
  "979",
  "980",
  "981",
  "982",
  "983",
  "984",
  "985",
  "986",
  "987",
  "988",
  "989",
  "990",
  "991",
  "992",
  "993",
  "994",
  "995",
  "996",
  "997",
  "998",
  "999",
  "1000",
  "1001",
  "1002",
  "1003",
  "1004",
  "1005",
  "1006",
  "1007",
  "1008",
  "1009",
  "1010",
  "1011",
  "1012",
  "1013",
  "1014",
  "1015",
  "1016",
  "1017",
  "1018",
  "1019",
  "1020",
  "1021",
  "1022",
  "1023",
  "1024",
  "1026",
  "1025",
  "1027",
  "1028",
  "1029",
  "1030",
  "1031",
  "1032",
  "1033",
  "1034",
  "1035",
  "1036",
  "1037",
  "1038",
  "1039",
  "1040",
  "1041",
  "1042"
] #单位列表 展开

        pointTypeadddata=self.readindicatorinfoexl()[2] # 获取需要创建的指标定义名称
        for i in range(len(pointTypeadddata)):
            pointTypename1=pointTypeadddata[i]
            for j in range(i+1,len(pointTypeadddata)):
                pointTypename2=pointTypeadddata[j]
                if pointTypename1 in pointTypename2:
                    pointTypeadddata[j]='电用量'

        # print(pointTypeadddata)

        pointTypepage= self.pointTypepage().get('data').get('records')
        pointTypedict={}
        for pointTypeinfo in pointTypepage:
            pointTypeName=pointTypeinfo.get('pointTypeName')
            pointTypeCode=pointTypeinfo.get('pointTypeCode')
            pointTypedict[pointTypeName]=pointTypeCode

        for pointTypeaddname in pointTypeadddata:
            if pointTypeaddname not in pointTypedict.keys():
                json_data = {    'id': '',    'pointTypeName': f'{pointTypeaddname}',
                             'pointTypeUnitIdList': pointTypeUnitIdList,} #单位暂时写死
                self.pointTypeadd(json_data=json_data)
            else:
                WARNING.logger.warning(f'点位类型：{pointTypeaddname}已存在')

    def addindicatorby_name(self,indicatoraddname,groupId):
        '''
        根据 指标名称 创建 指标定义
        :param indicatoraddname:
        :param groupId:
        :return:
        '''
        json_data={
            "groupId":groupId,
            "name":indicatoraddname,
            "type":1 # 暂时写死基础指标
        }

        indicatorLibrarypage=self.indicatorLibrarypage().get('data').get('records')
        indicatorLibrarynames=[i.get('name') for i  in indicatorLibrarypage]

        if indicatoraddname not in indicatorLibrarynames:
            indicatorLibraryId=self.indicatorLibraryadd(json_data=json_data).get('data')
            pass

        else:
            WARNING.logger.warning(f'指标定义名称：{indicatoraddname}已经存在')
            # return


        # 创建指标名称
        indicatorLibrarypage = self.indicatorLibrarypage().get('data').get('records')
        for itmes in indicatorLibrarypage:
            name = itmes.get('name')
            if indicatoraddname == name:
                return itmes

    def addindicatormodel(self,datatype,indicatoraddname,indicatoraddunitinfo, pointTypeCode):
        '''
        数据更新的模板
        :return:
        '''

        # 获取exl表数据
        # indicatorinfo=self.readindicatorinfoexl()
        # real_datalist, cycle_datalist=indicatorinfo[0],indicatorinfo[1]

        unitId = indicatoraddunitinfo.get('unitId',"")
        unit = indicatoraddunitinfo.get('unit',"")
        unitName = indicatoraddunitinfo.get('unitName',"")

        # --------以下信息都需要改---------
        groupId = 48  #指标定义分组id
        indicatorLibrary = 1  # 基础指标 写死暂时
        taskId_byday = 15 #按日更新任务的Id
        # deviceGroupDimensionIds="0,3,4,5,6" #设备分组维度 设备编号、电表啥的
        deviceGroupDimensionIds="0,1,43,2" #设备分组维度 设备编号、电表啥的

        # 添加指标定义数据
        indicatorbasicinfo=self.addindicatorby_name(indicatoraddname=indicatoraddname,groupId=groupId)
        indicatorLibraryId=indicatorbasicinfo.get('id')
        indicatorLibrarycode=indicatorbasicinfo.get('code')


        # 公式模板
        if datatype=='real':
            if '最大' in indicatoraddname:
                formula=f'MAX({pointTypeCode})'
            elif '最小' in indicatoraddname:
                formula = f'MIN({pointTypeCode})'
            elif '平均' in indicatoraddname:
                formula = f'AVG({pointTypeCode})'
            elif '总共' in indicatoraddname:
                formula = f'SUM({pointTypeCode})'
            else: #取实时
                formula = f'LAST({pointTypeCode})'
            # deviceGroupDimensionIds=f"{deviceGroupDimensionIds}"

            indicatorTimeWindowDTO = {
                "indicatorId": f"{indicatorLibraryId}",
                "windowType": 3,
                "intervalCategory": 1,
                "interval": 15,
                "timeGroupDimensionFunction": "SUM"
            }

            calculateWay=2
            taskId=""

        elif datatype == 'cycle':
            formula=f'MAX({pointTypeCode})-MIN({pointTypeCode})'

            indicatorTimeWindowDTO={
                'indicatorId': f"{indicatorLibraryId}",
                'windowType': 1,
                'timeCycleDefineId': '1',
                'timeGroupDimensionFunction': 'SUM',
            }
            calculateWay=1
            taskId=taskId_byday
            # deviceGroupDimensionIds=f"{deviceGroupDimensionIds}"

        else:
            WARNING.logger.warning(f'{pointTypeCode}数据类型有误')
            return None

        json_data = {
            'id': f'{indicatorLibraryId}',
            'name': f'{indicatoraddname}',
            'code': f'{indicatorLibrarycode}',
            'type':f"{indicatorLibrary}",
            'groupId': f'{groupId}',
            'unitId': f'{unitId}',
            'unit': f'{unit}',
            'unitName': f'{unitName}',
            'decimalNumber': 4,
            'formula': f'{formula}',
            'deviceGroupDimensionIds': f"{deviceGroupDimensionIds}",
            'deviceGroupDimensionFunction': 'SUM',
            'logicType': 1,
            'calculateWay': f"{calculateWay}",
            'taskId': f"{taskId}",
            'publishStatus': 0,
            'contrastSwitch': 0,
            'trialStatus': 0,
            'useCount': 0,
            'description': "初始化脚本批量创建",
            'indicatorTimeWindowDTO': indicatorTimeWindowDTO,
            'filterConditionDTOList': [],
            'dataItemVOS': [
                {
                    'code': f'{pointTypeCode}',
                    'name': f'{indicatoraddname}',
                    'type': 1,
                },
            ],
        }

        # print(json_data)
        self.icatorLibraryupdate(json_data=json_data)

    def bacthadd_indicator(self):
        '''
        批量新增指标定义数据
        1.读取exl，获取需要创建的指标定义名称
        2.根据名称查询点位类型，根据exl表中数据，获取对应的计算格式 max（点位1）-min（点位1）
        3.先获取已经创建的指标的名称，判断是否已经创建，没有创建则创建点位，创建点位
        :return:
        '''

        # 获取exl表数据
        indicatorinfo=self.readindicatorinfoexl()
        real_data, cycle_data=indicatorinfo[0],indicatorinfo[1]

        pointTypepage= self.pointTypepage().get('data').get('records')
        pointTypedict={} #查询点位类型名称和点位类型code
        for pointTypeinfo in pointTypepage:
            pointTypeName=pointTypeinfo.get('pointTypeName')
            pointTypeCode=pointTypeinfo.get('pointTypeCode')
            pointTypedict[pointTypeName]=pointTypeCode

            #模板添加
            for real_name,real_unit_info in real_data.items():
                if pointTypeName in real_name:
                    self.addindicatormodel(datatype='real',indicatoraddname=real_name,indicatoraddunitinfo=real_unit_info, pointTypeCode=pointTypeCode)

            for cycle_name,cycle_unit_info in cycle_data.items():
                if pointTypeName in cycle_name:

                    self.addindicatormodel(datatype='cycle',indicatoraddname=cycle_name,indicatoraddunitinfo=cycle_unit_info, pointTypeCode=pointTypeCode)

        return 1

if __name__ == '__main__':

    task=IndicatorMockWay()
    # task.readindicatorinfoexl()
    # task.batchadd_PointType()
    task.bacthadd_indicator()
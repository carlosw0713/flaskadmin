# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/11/27
Description: <Brief description of the file>
"""
from httpx import delete

from applications.common.HLZY.EMS.outway.device.device import DeviceData
from applications.common.HLZY.EMS.outway.indicator.indicator import Indicator

from applications.common.HLZY.IOT import *

class DeviceWay(DeviceData,Indicator):


    def getdeviceNamebycode(self):
        '''
        根据设备编号返回设备名称
        :return:
        '''
        devicepage=self.devicepage().get('data').get('records')
        devicedict={}
        for deviceinfo in devicepage:
            devicedict['deviceCode']=deviceinfo.get('deviceName')
        return devicedict


    def batchaddcalPointCode_Specified_sum(self):
        '''
        添加方式2，将指定的采集点列表，统一相加然后同步到，某个设备的计算点下
        2.1 入参 被计算设备列表（一个或者多个）列表形式、计算点设备编码
        2.2 循环批量设备，将多个设备中 相同点位类型的采集点依次获取出来 生成计算公式。
        2.3 调用创建计算点接口
        :return:
        '''
        adddevicecodelist=["dev_ele_a"]
        Specifieddevicecode="V1736496191424"
        SpecifieddevicecodeName="mock总"

        sumpointcodeinfolist=[]
        for adddevicecode in adddevicecodelist:
            pointcodeinfolist = self.pointCodepage(deviceCode=adddevicecode).get('data').get('records')
            sumpointcodeinfolist.extend(pointcodeinfolist)

        calpointcodeinfolist = self.calpointCodepage(deviceCode=Specifieddevicecode).get('data').get('records')
        calpointNames = [i.get('pointName') for i in calpointcodeinfolist]

        # 获取点位类型关系集合
        pointTypeUnitdict = {}
        pointTypeUnitpagelist = self.pointTypeUnitpage().get('data').get('records')
        for i in pointTypeUnitpagelist:
            pointTypeUnitdict[i.get('unit')] = i.get('id')

        # 同步数据集
        Synchronousdatadict={}
        for pointcodeinfo in sumpointcodeinfolist:
            pointName=pointcodeinfo.get('pointName')
            pointCode=pointcodeinfo.get('pointCode')
            pointTypeId=pointcodeinfo.get('pointTypeId')
            pointTypeName=pointcodeinfo.get('pointTypeName')
            unitId=pointcodeinfo.get('unitId')
            unit=pointcodeinfo.get('unit')

            # 获取计算点类型关系信息
            if Synchronousdatadict.get(pointTypeId) is None:

                Synchronousdatadict[pointTypeId]={
                    'dataItemVOS' :[
                    {
                        'colPointName': pointName,
                        'colPointCode': pointCode,
                        'type': 1,  # 采集点
                    }]
                }
                Synchronousdatadict[pointTypeId]['formula']=pointCode


                Synchronousdatadict[pointTypeId]['pointTypeUnitId'] = f'{pointTypeUnitdict.get(unit, "")}'
                Synchronousdatadict[pointTypeId]['pointTypeId'] = pointTypeId
                Synchronousdatadict[pointTypeId]['unitId'] = unitId
                Synchronousdatadict[pointTypeId]['deviceCode'] = Specifieddevicecode
                Synchronousdatadict[pointTypeId]['pointName']= f"{SpecifieddevicecodeName}_总_{pointTypeName}"

            else:
                dataItemVOSdict={
                        'colPointName': pointName,
                        'colPointCode': pointCode,
                        'type': 1,  # 采集点
                    }

                Synchronousdatadict[pointTypeId]['dataItemVOS'].append(dataItemVOSdict)
                Synchronousdatadict[pointTypeId]['formula'] = f"{Synchronousdatadict[pointTypeId]['formula']}+{pointCode}"

        # 循环遍历创建计算点
        for pointCode,Synchronousdata in Synchronousdatadict.items():
            # formula=Synchronousdata.get('formula')
            # dataItemVOS=Synchronousdata.get('dataItemVOS')
            pointName=Synchronousdata.get('pointName')

            json_data = {
                'cycleUnit': 's',# 采集周期暂时写死
                'cycle': '900',# 采集周期暂时写死
                'formula': Synchronousdata.get('formula'),
                'dataItemVOS': Synchronousdata.get('dataItemVOS'),
                'pointName': Synchronousdata.get('pointName'),
                'pointTypeId': Synchronousdata.get('pointTypeId'),
                'unitId': Synchronousdata.get('unitId'),
                'pointTypeUnitId': Synchronousdata.get('pointTypeUnitId'),#
                'deviceCode': Synchronousdata.get('deviceCode'),
            }

            if pointName in calpointNames: #如果存在则跳过
                continue

            self.calPointCode(json_data=json_data)


    def run_batchaddcalPointCode(self):
        '''
        添加方式1，直接将采集点所有数据直接同步到计算点
        1.1 根据设备A，查询设备采集点列表
        1.2 添加到设备B，调用添加计算点方法，依次将值添加到B，保持一直添加到位
        :return:
        '''

        deviceA='dev_bgl_el'# 数据源设备A code
        # deviceA='dev_all_ele_aa'# 数据源设备A code
        deviceB='V1734337461638' #迁移数据设备B code

        pointcodeinfolist=self.pointCodepage(deviceCode=deviceA).get('data').get('records')
        calpointcodeinfolist=self.calpointCodepage(deviceCode=deviceB).get('data').get('records')

        pointTypeUnitdict={}
        pointTypeUnitpagelist=self.pointTypeUnitpage().get('data').get('records')
        for i in pointTypeUnitpagelist:
            pointTypeUnitdict[i.get('unit')]=i.get('id')
        # print(pointTypeUnitdict)


        calpointNames=[i.get('pointName') for i in calpointcodeinfolist]

        # 循环添加计算点,将采集点信息同步过去
        for pointcodeinfo in pointcodeinfolist:
            pointName=pointcodeinfo.get('pointName')
            pointCode=pointcodeinfo.get('pointCode')
            pointTypeId=pointcodeinfo.get('pointTypeId')
            unitId=pointcodeinfo.get('unitId')
            unit=pointcodeinfo.get('unit')

            json_data = {
                'cycleUnit': 's',# 采集周期暂时写死
                'cycle': '222',# 采集周期暂时写死
                'formula': pointCode,
                'dataItemVOS': [
                    {
                        'colPointName': pointName,
                        'colPointCode': pointCode,
                        'type': 1, #采集点
                    },

                ],
                'pointName': pointName,
                'pointTypeId': pointTypeId,
                'unitId': unitId,
                'pointTypeUnitId': f'{pointTypeUnitdict.get(unit, "")}',#
                'deviceCode': deviceB,
            }
            # print(json_data)
            if pointName in calpointNames:
                continue

            self.calPointCode(json_data=json_data)


    def printfpointCode(self):
        '''
        根据设备id打印出所有指标点代码
        打印出指标点代码
        :return:
        '''

        pointTypeNamelist=['A相电压',"B相电压","C相电压"]
        pointTypeNamelist=['异常数据点']
        deviceCode=['dev_ele_a']
        pointcodeinfolist = self.pointCodepage(deviceCode=deviceCode).get('data').get('records')
        calpointcodeinfolist=self.calpointCodepage(deviceCode=deviceCode).get('data').get('records')
        pointCodelist=[i.get('pointCode') for i in pointcodeinfolist if i.get('pointTypeName') in pointTypeNamelist]
        calpointCodelist=[i.get('pointCode') for i in calpointcodeinfolist if i.get('pointTypeName') in pointTypeNamelist]


        # taos语句
        sumpointCodelist=pointCodelist+calpointCodelist
        print(sumpointCodelist)
        for pointCode in sumpointCodelist:
            print(f"DROP TABLE `ems`.`{pointCode}`;")

        for pointCode in sumpointCodelist:
            print(f"SELECT `_timestamp`,`value` FROM  `ems`.`{pointCode}` order by `_timestamp` ASC limit 200;")

        for pointCode in sumpointCodelist: #注意时间范围
            print(f" DELETE FROM  `ems`.`{pointCode}` WHERE `_timestamp` >= '2024-11-01' AND `_timestamp` <= '2025-01-11';")

if __name__ == '__main__':
    task=DeviceWay()
    # task.run_batchaddcalPointCode()
    task.printfpointCode()

    # task.run_batchaddcalPointCode_Specified_sum()
# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/12/18
Description: <Brief description of the file>
"""
from datetime import datetime

from applications.common.HLZY.EMS.outway.device.device import DeviceData


class PointCodeCompute(DeviceData):


    def Calculatethevalueofeachnode(self,calPointCode,PointCodelist,startTime,endTime):
        '''
        判断A和B（列表）每个节点的值是否一致
        :return:
        '''

        cal_json_data = {
            'pointCode': calPointCode,
            'startTime': startTime,
            'endTime': endTime,
            'intervalType': 'default'
        }

        calPointCodeinfolist = self.pointCodehistoryData(params=cal_json_data).get('data').get('list')

        calupdatatimelist=[i.get('updateTime') for i in calPointCodeinfolist]

        PointCodelistvaluedict={}
        for PointCode in PointCodelist:
            PointCode_json_data = {
                'pointCode': PointCode,
                'startTime': startTime,
                'endTime': endTime,
                'intervalType': 'default'
            }

            PointCodeinfolist = self.pointCodehistoryData(params=PointCode_json_data).get('data').get('list')

            for PointCodeinfo in PointCodeinfolist:
                if PointCodeinfo.get('updateTime') in calupdatatimelist:
                    if  PointCodelistvaluedict.get(PointCodeinfo.get('updateTime')) is None:
                        PointCodelistvaluedict[PointCodeinfo.get('updateTime')]=PointCodeinfo.get('newValue')
                    else:
                        PointCodelistvaluedict[PointCodeinfo.get('updateTime')]+=PointCodeinfo.get('newValue')


        for calPointCodeinfo in calPointCodeinfolist:
            calPointCodevalue=calPointCodeinfo.get('newValue')
            calPointCodeTime=calPointCodeinfo.get('updateTime')

            PointCodelistvalue=round(PointCodelistvaluedict.get(calPointCodeTime),2)
            if calPointCodevalue==PointCodelistvalue:
                print(f"计算值正确时间:{calPointCodeTime},计算点值{calPointCodevalue}，采集点总值{PointCodelistvalue} 差值:{calPointCodevalue-PointCodelistvalue}")

            else:
                print(f"计算值不正确,时间:{calPointCodeTime},计算点值{calPointCodevalue}，采集点总值{PointCodelistvalue} 差值:{calPointCodevalue-PointCodelistvalue}")


    def assert_calpointcodeTure(self):
        '''
        判断计算点的值是否计算正确
        1.根据计算点
        :return:
        '''

        calPointCodeId=1
        calPointCodedetails=self.calPointCodedetails(calPointCodeId=calPointCodeId)
        PointCodeList=[i.get('colPointCode') for i in calPointCodedetails.get('data').get('dataItemVOS')]
        calPointCode=calPointCodedetails.get('data').get('pointCode')

        startTime= int(datetime.strptime("2024-12-18 00:00:00", "%Y-%m-%d %H:%M:%S").timestamp() * 1000)
        endTime= int(datetime.strptime("2024-12-18 23:59:59", "%Y-%m-%d %H:%M:%S").timestamp() * 1000)

        self.Calculatethevalueofeachnode(calPointCode,PointCodeList,startTime,endTime)

if __name__ == '__main__':
    task=PointCodeCompute()
    task.assert_calpointcodeTure()


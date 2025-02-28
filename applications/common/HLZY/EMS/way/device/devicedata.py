# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2025/1/2
Description: <Brief description of the file>
"""

from datetime import datetime, timedelta

from applications.common.HLZY.EMS.outway.device.device import DeviceData
from public.logging_tool.log_control import *

class DeviceDataWay(DeviceData):

    def calculate_time_difference(self,date_str1, date_str2):
        # 定义日期格式
        date_format = "%Y-%m-%d %H:%M:%S"

        # 将日期字符串转换为 datetime 对象
        datetime1 = datetime.strptime(date_str1, date_format)
        datetime2 = datetime.strptime(date_str2, date_format)

        # 计算时间差
        time_difference = datetime2 - datetime1

        if time_difference is None:
            WARNING.logger.error(f'!!!!!!!!!!')
            return 0

        return int(time_difference.seconds)/100


    def getSynchronizationcounts_by_date(self,pointCode,date):
        '''
        获取当天的同步次数
        :param pointCode:
        :param date:
        :return:
        '''

        startTime=int(datetime.strptime(f"{date} 00:00:00",
                                           "%Y-%m-%d %H:%M:%S").timestamp() * 1000),
        endTime=int(datetime.strptime(f"{date} 23:59:59",
                                         "%Y-%m-%d %H:%M:%S").timestamp() * 1000),

        params = {'pointCode': pointCode, 'startTime': startTime, 'endTime': endTime,
                  'intervalType': 'default', }

        pointCodehistoryData=self.pointCodehistoryData(params=params).get('data').get('list')
        if len(pointCodehistoryData)==0:
            WARNING.logger.warning(f'采集点：{pointCode} 找不到数据')
            return 0

        return len(pointCodehistoryData)

    def getavgSynchronizationtime(self,pointCode):
        '''
        获取平均同步时间
        :param pointCode:
        :return:
        '''

        startTime = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        endTime = startTime + timedelta(days=1) - timedelta(microseconds=1)

        startTime=int(startTime.timestamp()*1000)
        endTime=int(endTime.timestamp()*1000)

        params = {'pointCode': pointCode, 'startTime': startTime, 'endTime': endTime,
                  'intervalType': 'default', }

        pointCodehistoryData=self.pointCodehistoryData(params=params).get('data').get('list')
        if len(pointCodehistoryData)==0:
            WARNING.logger.warning(f'采集点：{pointCode} 找不到数据')
            return 0

        for pointindex in range(1,len(pointCodehistoryData)):
            # 计算并打印时间差

            date_str1=pointCodehistoryData[pointindex-1].get('updateTime')
            date_str2=pointCodehistoryData[pointindex].get('updateTime')
            time_diff = self.calculate_time_difference(date_str1, date_str2)


            return time_diff


    def assert_Synchronizationtime_by_gatway(self):
        '''
        判断同步时间根据网关
        :return:
        '''

        pointCodepage=self.pointCodepage().get('data').get('records')
        Synchronizationtimetypedict={}
        for pointCodepageinfo in pointCodepage:
            deviceCode=pointCodepageinfo.get('deviceCode')
            gatwaycode=str(deviceCode).split('_')[0]
            pointCode=pointCodepageinfo.get('pointCode')

            if Synchronizationtimetypedict.get(gatwaycode) is None:
                Synchronizationtime=self.getavgSynchronizationtime(pointCode=pointCode)
                Synchronizationtimetypedict[gatwaycode]=Synchronizationtime

                # print(Synchronizationtime)
                if Synchronizationtime is None:
                    WARNING.logger.warning(f"网关:{deviceCode},没有找到数据")
                    Synchronizationtimetypedict[gatwaycode] = None
                    continue
                elif Synchronizationtime>=800 and Synchronizationtime<=1000:
                    INFO.logger.INFO(f"网关:{gatwaycode},同步时间:{Synchronizationtime}")
                    pass
                else:
                    ERROR.logger.error(f"网关:{gatwaycode},同步时间不正确{Synchronizationtime}")

            else:
                continue

    def assert_Synchronizationcount_by_date(self):
        '''
        判断点位同步次数是否正确
        :return:
        '''
        date='2025-01-07'

        assertcount=96 #判断同步次数
        pointCodepage=self.pointCodepage().get('data').get('records')
        Synchronizationcounttypedict={}
        for pointCodepageinfo in pointCodepage:
            deviceCode=pointCodepageinfo.get('deviceCode')
            gatwaycode=str(deviceCode).split('_')[0]
            pointCode=pointCodepageinfo.get('pointCode')

            if Synchronizationcounttypedict.get(deviceCode) is None:
                Synchronizationcount = self.getSynchronizationcounts_by_date(pointCode=pointCode,date=date)
                Synchronizationcounttypedict[deviceCode]=Synchronizationcount
            else:
                continue

            if Synchronizationcount!=assertcount:
                ERROR.logger.error(f"设备{deviceCode}，同步次数不正确，实际同步次数{Synchronizationcount},期望同步次数{assertcount}")

            else:
                pass


if __name__ == '__main__':
    task=DeviceDataWay()
    task.assert_Synchronizationcount_by_date()


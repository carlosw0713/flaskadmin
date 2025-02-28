# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/12/31
Description: <专门用于指标数据的查询和统计>
"""
from datetime import datetime

from applications.common.HLZY.EMS.outway.device.device import DeviceData
from applications.common.HLZY.EMS.outway.indicator.indicator import Indicator
from public.file_tool.exl_way import read_excel_data
from public.logging_tool.log_control import *



class IndicatorQuery(Indicator,DeviceData):


    def readreportexlinfo(self):
        '''
        读取报表exl信息
        :return:
        '''

        file_name = 'D:\测试文档\EMS\苏南码头\苏南报表数据.xlsx'
        # sheet_name = '电日报表'
        sheet_name = '水日报表'
        exl_data = read_excel_data(file_name=file_name, sheet_name=sheet_name, datatype='list', loc=[1, 1])

        exldatadict={}
        for exlinfo in exl_data:
            exldatadict[exlinfo[0]]=[exlinfo[1],exlinfo[2],exlinfo[3]]
            # print(exlinfo)

        return exldatadict


    def getdeviceNamebycode(self):
        '''
        根据设备编号返回设备名称
        :return:
        '''
        devicepage=self.devicepage().get('data').get('records')
        devicedict={}
        for deviceinfo in devicepage:
            devicedict[deviceinfo.get('deviceCode')]=deviceinfo.get('deviceName')
        return devicedict


    def bacthqueryinicator_byrule(self):
        """
        批量查询指标数据
        根据日期和设备分组
        :return:
        """
        caltimedata = '2024-12-31'
        # queryindicatornames=['正有功电度','按月_正向有功电度','按年_正向有功电度']
        queryindicatornames=['水体积流量','按月_水体积流量','按年_水体积流量']

        # 获取指标和设备名称的关联信息
        deviceNamebycodeinfo=self.getdeviceNamebycode()

        # 获取需要查询指标的id
        indicatoridinfodict={}
        indicatorLibrarypage=self.indicatorLibrarypage().get('data').get('records')

        for queryindicatorname in queryindicatornames:

            for indicatorLibraryinfo in indicatorLibrarypage:
                indicatorId=indicatorLibraryinfo.get('id')
                timeType=indicatorLibraryinfo.get('timeType')
                indicatorname=indicatorLibraryinfo.get('name')

                # if queryindicatorname in indicatorname:
                if queryindicatorname == indicatorname:
                    # INFO.logger.info(f"指标名称：{indicatorname}，id：{indicatorId}")


                    startTime=int(datetime.strptime(f"{caltimedata} 00:00:00","%Y-%m-%d %H:%M:%S").timestamp() * 1000)
                    endTime=int(datetime.strptime(f"{caltimedata} 23:59:59","%Y-%m-%d %H:%M:%S").timestamp() * 1000)

                    if timeType=='month':
                        startTime = int(datetime.strptime(f"{caltimedata[0:7]}-01 00:00:00",
                                                          "%Y-%m-%d %H:%M:%S").timestamp() * 1000)
                        endTime = int(datetime.strptime(f"{caltimedata[0:7]}-31 23:59:59",
                                                        "%Y-%m-%d %H:%M:%S").timestamp() * 1000)

                    if timeType=='year':
                        startTime=int(datetime.strptime(f"{caltimedata[0:4]}-01-01 00:00:00","%Y-%m-%d %H:%M:%S").timestamp() * 1000)
                        endTime=int(datetime.strptime(f"{caltimedata[0:4]}-12-31 23:59:59","%Y-%m-%d %H:%M:%S").timestamp() * 1000)


                    # 根据id查询数据
                    json_data = {
                        'indicatorId': indicatorId,
                        'startTime': startTime,
                        'endTime': endTime,
                        'paramDTOS': []
                    }
                    # 获取基础指标数据
                    icatordata = self.icatorLibraryquerydata(json_data=json_data).get('data')
                    for icatorinfo in icatordata:
                        deviceCode=icatorinfo.get('设备编号')
                        deviceName=deviceNamebycodeinfo.get(deviceCode)

                        deviceNameandCode=f"{deviceName}/{deviceCode}"
                        value=round(float(icatorinfo.get('value')),3) #保留三位小数
                        if indicatoridinfodict.get(deviceNameandCode) is None:
                            indicatoridinfodict[deviceNameandCode]={}
                            indicatoridinfodict[deviceNameandCode][f"{indicatorname}"]=value
                        else:
                            indicatoridinfodict[deviceNameandCode][f"{indicatorname}"] = value

        return indicatoridinfodict


    def print_query(self):
        '''
        打印查询结果
        :return:
        '''

        exldata=self.readreportexlinfo()

        for deviceNameCode,indicatorinfo in self.bacthqueryinicator_byrule().items():
            deviceName=deviceNameCode.split('/')[0]
            indicatorvalues=list(indicatorinfo.values())
            # print(f"设备名称：{deviceName}，数据：{indicatorinfo}")

            whilebreak=True

            for name,exlvalue in exldata.items():

                # 格式化名称
                name=name.replace('Ⅱ','II')
                name=name.replace('Ⅰ','I')
                deviceName=deviceName.replace('Ⅰ','I')
                deviceName=deviceName.replace('Ⅱ','II')


                if deviceName in name :

                    if exlvalue==indicatorvalues:
                        INFO.logger.info(
                            f"设备名称：{deviceNameCode}，指标名称：{name}，数据集：{exlvalue}，实际数据集：{indicatorvalues}")

                    else:
                        ERROR.logger.error(f"设备名称：{deviceNameCode}，指标名称：{name}，数据集：{exlvalue}，实际数据集：{indicatorvalues}")
                    whilebreak=False

                    break

            if whilebreak:
                WARNING.logger.warning(f"在报表中未找到该设备名称,设备名称：{deviceNameCode}，实际数据集：{indicatorvalues}")


if __name__ == '__main__':
    task=IndicatorQuery()
    task.print_query()

    # task.readreportexlinfo()



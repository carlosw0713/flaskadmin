# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/12/13
Description: <Brief description of the file>
"""

from applications.common.HLZY.IOT import *
from applications.common.HLZY.IOT.outway.device.device import Device
from public.file_tool.exl_way import *

class DeviceMockWay(Device):

    def __init__(self):
        self.cookies = IOT_INFO.get('cookies')
        self.headers = IOT_INFO.get('headers')
        self.uri = IOT_INFO.get('uri')

    def write_deviceinfo_exl(self):
        '''
        获取当前设备信息，并写入exl表中
        需要指定主网关名称和子网关名称列表
        返回主网关、子网关的设备名称和编号
        :return:
        '''

        productname="总检测设备"
        productsubnamelist=["水检测设备","气检测设备","电检测设备"]

        productsubnamelist.append(productname)

        devicelist=self.iotdevicepage().get('data').get('records')

        deviceexl_info=[]
        for items in devicelist:
            productName=items.get('productName')

            if productName in productsubnamelist:
                deviceexl_info.append([productName,items.get('deviceCode'),items.get('deviceName')])

        file_name=r"D:\pythonproject\HLZY\static\exl\iotdevice\iotdeviceinfo.xlsx"
        sheet_name="设备列表"
        exl_data=deviceexl_info
        append_excel_data(file_name, sheet_name, exl_data, loc=None, savecopy=False)



    def run_addiotproduct(self,productNames):
        '''
        创建产品\
        1.查询是否存在存在返回code
        2.不存在创建产品返回code
        :return:
        '''
        productInfodict={}

        productinfolist=self.iotproductpage().get('data').get('records')

        for productName in productNames:
            ifcreate = True
            for productinfo in productinfolist:

                if productName == productinfo.get('productName'):
                    productInfodict[productName]=productinfo.get('productCode')

                    self.iotproductpublish(productinfo.get('productCode')) #产品发布

                    ifcreate=False

                    break
            if ifcreate:
                productCode = self.iotproductgenerateid()
                productInfodict[productName] = productCode
                if "总" in productName:
                    deviceType=2
                    json_data = {'deviceType': f"{deviceType}", 'productCode': f'{productCode}',
                                 'productName': f'{productName}',
                                 'protocolCode': "HLSC_MQTT", 'remark': '测试批量创建', }
                else:
                    deviceType=3
                    json_data = {'deviceType': f"{deviceType}", 'productCode': f'{productCode}',
                                 'productName': f'{productName}',
                                 'protocolCode': "", 'remark': '测试批量创建', }
                self.iotproduct(json_data)

                self.iotproductpublish(productCode)  # 产品发布

        return productInfodict




    def run_devicemock(self):
        '''
        1.创建主产品，创建主设备，返回主设备的（可手动）
        2.读取exl表数据，
        2.1第一行是产品，匹配获取产品点位判断是否存在不在则创建产品
        2.2第二三行是设备id和名称，设备id需要拼接主设备的ID
        :return:
        '''

        productNames=["总检测设备","电检测设备","水检测设备","气检测设备"]

        productinfodict=self.run_addiotproduct(productNames=productNames)


        file_name=r"D:\pythonproject\HLZY\static\exl\iotdevice\iotdeviceinfo.xlsx"
        sheet_name="设备列表"

        deviceexlinfolist=read_excel_data(file_name=file_name,sheet_name="设备列表")

        for deviceexlinfo in deviceexlinfolist:
            productName=deviceexlinfo[0]
            deviceCode=deviceexlinfo[1]
            deviceName=deviceexlinfo[2]
            productCode=productinfodict.get(productName)
            json_data = {'productCode': f'{productCode}', 'deviceCode': f'{deviceCode}',
                         'deviceName': f'{deviceName}', }
            self.iotdevicesave(json_data=json_data)

    def run_bacthdeliotdevice(self):
        '''
        批量删除列表设备
        :return:
        '''

        deltag='' #设备编号介绍

        iotdevicepageinfolist=self.iotdevicepage().get('data').get('records')
        for iotdevicepageinfo in iotdevicepageinfolist:
            deviceCode=iotdevicepageinfo.get('deviceCode')
            if deltag in deviceCode:
                self.deliotdevic(deviceCode)

if __name__ == '__main__':
    task=DeviceMockWay()
    # task.write_deviceinfo_exl()

    task.run_devicemock()

    # task.run_bacthdeliotdevice()


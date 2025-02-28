# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2025/2/6
Description: <Brief description of the file>
"""

from applications.common.HLZY.IOT import *
from applications.common.HLZY.IOT.outway.device.device import Device
from public.file_tool.exl_way import *

class DeviceWay(Device):

    def __init__(self):
        self.cookies = IOT_INFO.get('cookies')
        self.headers = IOT_INFO.get('headers')
        self.uri = IOT_INFO.get('uri')

    def run_batchaddiotdevicesave(self):
        productCode = '0naxVhZ7'
        data_tag = '1111'
        spc_tag = 'w'
        for i in range(100):
            deviceCode = f'device_{spc_tag}_{data_tag}_{i}'
            deviceName = f'设备_{spc_tag}_{data_tag}_{i}'
            json_data = {'productCode': f'{productCode}', 'deviceCode': f'{deviceCode}', 'deviceName': f'{deviceName}', }
            self.iotdevicesave(json_data=json_data)


    def run_bacthaddiotdevice(self):
        '''
        批量给产品添加设备
        :return:
        '''

        # 网关设备编号和子设备编号
        productCodes = {'productCode': 'cluqSMNO', 'subproductCode': 'W2QKMpmR'}
        gatewaydevice_num=80
        subgatewaydevicenum = 10
        startindex=1
        whetheradd=False #是否添加数据

        spc_tag='YC'
        binddeviceinfolist = []
        deviceinfolist=[]

        for l in range(startindex, gatewaydevice_num + 1):  # 主网关绑定设备
            deviceCode = f'device{l}_{spc_tag}'
            deviceName = f'设备{l}_{spc_tag}'
            json_data = {'productCode': f'{productCodes.get("productCode")}', 'deviceCode': f'{deviceCode}',
                         'deviceName': f'{deviceName}', }
            if whetheradd:
                self.iotdevicesave(json_data=json_data)

            deviceinfolist.append([deviceCode])

            # 过滤 直连设备 没有子设备
            if productCodes.get("subproductCode") is None:
                continue

            subdeviceCodelist=[]
            for j in range(startindex, subgatewaydevicenum + 1):  # 子网关绑定设备
                subdeviceCode = f'device{l}_{spc_tag}_{j}'
                deviceName = f'设备{l}_{spc_tag}_{j}'
                json_data = {'productCode': f'{productCodes.get("subproductCode")}', 'deviceCode': f'{subdeviceCode}',
                             'deviceName': f'{deviceName}', }
                if whetheradd:
                    self.iotdevicesave(json_data=json_data)

                subdeviceCodelist.append(subdeviceCode)
            subdeviceCodelist.insert(0,deviceCode)
            binddeviceinfolist.append(subdeviceCodelist)#添加设备信息


        # 储存为csv文件
        device_csvfile_name = os.path.join(BASE_DIR, 'static', 'csv', 'deviceyc',
                                               f"压测产品文件_{gatewaydevice_num}test.csv")
        binddevice_csvfile_name = os.path.join(BASE_DIR, 'static', 'csv', 'deviceyc',
                                               f"压测设备文件_{gatewaydevice_num}test.csv")

        append_csv_data(file_name=device_csvfile_name, csv_data=deviceinfolist, loc=[1,1], savecopy=False)
        append_csv_data(file_name=binddevice_csvfile_name, csv_data=binddeviceinfolist, loc=[1,1], savecopy=False)


if __name__ == '__main__':
    task=DeviceWay()
    task.run_bacthaddiotdevice()
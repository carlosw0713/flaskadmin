# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/11/22
Description: <Brief description of the file>
"""
import json

from applications.common.HLZY.IOT.outway.device.device import Device


def run_getiotthingspage_jmeterdata():
    '''
    获取物模型数据，并构建jemter脚本
    :return:
    '''

    productCode = 'W2QKMpmR'
    iotthingspageinfolist = Device().iotthingspage(productCode)

    devicedetainfo = {}
    pulish_data = {
        "ver": "1.0",
        "msgId": " ${__time(,)}",
        "data": {
            # "${subdeviceCode}": {
            #     "LA_voltage": '${__Random(1,9,)}'
            # }
        },
        "ts": '${__time(/1000,)}'
    }

    data_dict = {}
    for iotthingspageinfo in iotthingspageinfolist:
        identifier = iotthingspageinfo.get('identifier')
        devicedetainfo[identifier] = '${__Random(1,1000,)}'

    subdevicecodestr=""
    for i in range(1, 11):
        # print(pulish_data["data"])\

        subdevicestr= '${'+f'subdeviceCode{i}'+'}'
        subdevicecodestr += f',subdeviceCode{i}'

        pulish_data["data"][subdevicestr] = devicedetainfo
        # pulish_data = json.dumps(pulish_data)
        # print(pulish_data)
    pulish_data = json.dumps(pulish_data)
    print(subdevicecodestr)
    print(pulish_data)

if __name__ == '__main__':
    run_getiotthingspage_jmeterdata()
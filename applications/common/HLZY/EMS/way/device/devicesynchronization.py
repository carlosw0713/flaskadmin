# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/12/27
Description: <Brief description of the file>
"""
import json
import random
import string

from applications.common.HLZY.EMS.outway.device.device import DeviceData
from applications.common.HLZY.EMS.outway.device.devicesynchronization import DeviceSynchronization
from applications.common.HLZY.EMS.outway.indicator.indicator import Indicator
from public.logging_tool.log_control import *


class DeviceSynchronizationWay(DeviceSynchronization,DeviceData,Indicator):

    def generate_random_string(self,length=6):
        characters = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(length))
        return random_string
    def deviceSynchronization_jsonmodel(self,gatewayName,modelName,deviceName,devicecode,gatewayCode):
        '''
        设备批量同步信息模板
        :param gatewayName:网关名称
        :param modelName: 点位类型名称
        :param deviceName:设备名称
        :param devicecode:设备编码
        :param gatewayCode:网关编码
        :return:
        '''

        # ------使用一个设备进行点位类型同步，获取同步采集点的json入参信息------
        # 采集点不相同时需要改变！！！！！
        json_data = [
            {
                'pointCode': 'col_Zb1mQK',
                'pointName': '5#分变Ⅰ段_A相功率因数',
                'pointTypeId': '36',
                'pointTypeUnitId': None,
                'pointTypeName': 'A相功率因数',
                'unit': None,
                'gatewayCode': 'HLGW1012424003096',
                'subDeviceCode': 'HLGW2426003096_RS48511',
                'identifier': 'COSa',
                'dataType': 'float',
                'pointCodeLevel': 'A相功率因数>5#分变Ⅰ段>5#分变高压',
                'unitOptions': [],
                'type': '1',
                'deviceCode': 'HLGW2426003096_RS48512',
            },
            {
                'pointCode': 'col_sApyJd',
                'pointName': '5#分变Ⅰ段_总功率因数',
                'pointTypeId': '35',
                'pointTypeUnitId': None,
                'pointTypeName': '总功率因数',
                'unit': None,
                'gatewayCode': 'HLGW1012424003096',
                'subDeviceCode': 'HLGW2426003096_RS48511',
                'identifier': 'COS',
                'dataType': 'float',
                'pointCodeLevel': '总功率因数>5#分变Ⅰ段>5#分变高压',
                'unitOptions': [],
                'type': '1',
                'deviceCode': 'HLGW2426003096_RS48512',
            },
            {
                'pointCode': 'col_RUs5rD',
                'pointName': '5#分变Ⅰ段_B相功率因数',
                'pointTypeId': '37',
                'pointTypeUnitId': None,
                'pointTypeName': 'B相功率因数',
                'unit': None,
                'gatewayCode': 'HLGW1012424003096',
                'subDeviceCode': 'HLGW2426003096_RS48511',
                'identifier': 'COSb',
                'dataType': 'float',
                'pointCodeLevel': 'B相功率因数>5#分变Ⅰ段>5#分变高压',
                'unitOptions': [],
                'type': '1',
                'deviceCode': 'HLGW2426003096_RS48512',
            },
            {
                'pointCode': 'col_pvrdyZ',
                'pointName': '5#分变Ⅰ段_C相功率因数',
                'pointTypeId': '38',
                'pointTypeUnitId': None,
                'pointTypeName': 'C相功率因数',
                'unit': None,
                'gatewayCode': 'HLGW1012424003096',
                'subDeviceCode': 'HLGW2426003096_RS48511',
                'identifier': 'COSc',
                'dataType': 'float',
                'pointCodeLevel': 'C相功率因数>5#分变Ⅰ段>5#分变高压',
                'unitOptions': [],
                'type': '1',
                'deviceCode': 'HLGW2426003096_RS48512',
            },
            {
                'pointCode': 'col_ObtxyM',
                'pointName': '5#分变Ⅰ段_当前需量',
                'pointTypeId': '954',
                'pointTypeUnitId': '10',
                'pointTypeName': '当前需量',
                'unit': 'kW',
                'gatewayCode': 'HLGW1012424003096',
                'subDeviceCode': 'HLGW2426003096_RS48511',
                'identifier': 'D',
                'dataType': 'float',
                'pointCodeLevel': '当前需量>5#分变Ⅰ段>5#分变高压',
                'unitOptions': [
                    {
                        'label': 'kW (千瓦)',
                        'value': '10',
                    },
                    {
                        'label': 'MW (兆瓦)',
                        'value': '11',
                    },
                    {
                        'label': 'W (瓦)',
                        'value': '12',
                    },
                ],
                'type': '1',
                'deviceCode': 'HLGW2426003096_RS48512',
            },
            {
                'pointCode': 'col_ZuKU2Z',
                'pointName': '5#分变Ⅰ段_平电度',
                'pointTypeId': '3',
                'pointTypeUnitId': '1',
                'pointTypeName': '平电度',
                'unit': 'kWh',
                'gatewayCode': 'HLGW1012424003096',
                'subDeviceCode': 'HLGW2426003096_RS48511',
                'identifier': 'FkWhP',
                'dataType': 'float',
                'pointCodeLevel': '平电度>5#分变Ⅰ段>5#分变高压',
                'unitOptions': [
                    {
                        'label': 'kWh (千瓦时)',
                        'value': '1',
                    },
                    {
                        'label': 'MWh (兆瓦时)',
                        'value': '2',
                    },
                    {
                        'label': 'Wh (瓦时)',
                        'value': '3',
                    },
                    {
                        'label': 'kvarh (千乏时)',
                        'value': '4',
                    },
                    {
                        'label': 'Mvarh (兆乏时)',
                        'value': '5',
                    },
                    {
                        'label': 'varh (乏时)',
                        'value': '6',
                    },
                    {
                        'label': 'kVAh (千伏安时)',
                        'value': '7',
                    },
                    {
                        'label': 'MVAh (兆伏安时)',
                        'value': '8',
                    },
                    {
                        'label': 'VAh (伏安时)',
                        'value': '9',
                    },
                ],
                'type': '1',
                'deviceCode': 'HLGW2426003096_RS48512',
            },
            {
                'pointCode': 'col_8ESh7e',
                'pointName': '5#分变Ⅰ段_A相电流',
                'pointTypeId': '25',
                'pointTypeUnitId': '19',
                'pointTypeName': 'A相电流',
                'unit': 'A',
                'gatewayCode': 'HLGW1012424003096',
                'subDeviceCode': 'HLGW2426003096_RS48511',
                'identifier': 'Ia',
                'dataType': 'float',
                'pointCodeLevel': 'A相电流>5#分变Ⅰ段>5#分变高压',
                'unitOptions': [
                    {
                        'label': 'A (安培)',
                        'value': '19',
                    },
                    {
                        'label': 'KV (千伏特)',
                        'value': '21',
                    },
                ],
                'type': '1',
                'deviceCode': 'HLGW2426003096_RS48512',
            },
            {
                'pointCode': 'col_FnDUEO',
                'pointName': '5#分变Ⅰ段_B相电流',
                'pointTypeId': '26',
                'pointTypeUnitId': '19',
                'pointTypeName': 'B相电流',
                'unit': 'A',
                'gatewayCode': 'HLGW1012424003096',
                'subDeviceCode': 'HLGW2426003096_RS48511',
                'identifier': 'Ib',
                'dataType': 'float',
                'pointCodeLevel': 'B相电流>5#分变Ⅰ段>5#分变高压',
                'unitOptions': [
                    {
                        'label': 'A (安培)',
                        'value': '19',
                    },
                    {
                        'label': 'KV (千伏特)',
                        'value': '21',
                    },
                ],
                'type': '1',
                'deviceCode': 'HLGW2426003096_RS48512',
            },
            {
                'pointCode': 'col_vKRLJ5',
                'pointName': '5#分变Ⅰ段_C相电流',
                'pointTypeId': '27',
                'pointTypeUnitId': '19',
                'pointTypeName': 'C相电流',
                'unit': 'A',
                'gatewayCode': 'HLGW1012424003096',
                'subDeviceCode': 'HLGW2426003096_RS48511',
                'identifier': 'Ic',
                'dataType': 'float',
                'pointCodeLevel': 'C相电流>5#分变Ⅰ段>5#分变高压',
                'unitOptions': [
                    {
                        'label': 'A (安培)',
                        'value': '19',
                    },
                    {
                        'label': 'KV (千伏特)',
                        'value': '21',
                    },
                ],
                'type': '1',
                'deviceCode': 'HLGW2426003096_RS48512',
            },
            {
                'pointCode': 'col_NoEP6V',
                'pointName': '5#分变Ⅰ段_总有功功率',
                'pointTypeId': '13',
                'pointTypeUnitId': '10',
                'pointTypeName': '总有功功率',
                'unit': 'kW',
                'gatewayCode': 'HLGW1012424003096',
                'subDeviceCode': 'HLGW2426003096_RS48511',
                'identifier': 'P',
                'dataType': 'float',
                'pointCodeLevel': '总有功功率>5#分变Ⅰ段>5#分变高压',
                'unitOptions': [
                    {
                        'label': 'kW (千瓦)',
                        'value': '10',
                    },
                    {
                        'label': 'MW (兆瓦)',
                        'value': '11',
                    },
                    {
                        'label': 'W (瓦)',
                        'value': '12',
                    },
                    {
                        'label': 'kvar (千乏)',
                        'value': '13',
                    },
                    {
                        'label': 'Mvar (兆乏)',
                        'value': '14',
                    },
                    {
                        'label': 'var (乏)',
                        'value': '15',
                    },
                    {
                        'label': 'kVA (千伏安)',
                        'value': '16',
                    },
                    {
                        'label': 'MVA (兆伏安)',
                        'value': '17',
                    },
                    {
                        'label': 'VA (伏安)',
                        'value': '18',
                    },
                ],
                'type': '1',
                'deviceCode': 'HLGW2426003096_RS48512',
            },
            {
                'pointCode': 'col_HrPN6R',
                'pointName': '5#分变Ⅰ段_A相有功功率',
                'pointTypeId': '14',
                'pointTypeUnitId': '10',
                'pointTypeName': 'A相有功功率',
                'unit': 'kW',
                'gatewayCode': 'HLGW1012424003096',
                'subDeviceCode': 'HLGW2426003096_RS48511',
                'identifier': 'Pa',
                'dataType': 'float',
                'pointCodeLevel': 'A相有功功率>5#分变Ⅰ段>5#分变高压',
                'unitOptions': [
                    {
                        'label': 'kW (千瓦)',
                        'value': '10',
                    },
                    {
                        'label': 'MW (兆瓦)',
                        'value': '11',
                    },
                    {
                        'label': 'W (瓦)',
                        'value': '12',
                    },
                    {
                        'label': 'kvar (千乏)',
                        'value': '13',
                    },
                    {
                        'label': 'Mvar (兆乏)',
                        'value': '14',
                    },
                    {
                        'label': 'var (乏)',
                        'value': '15',
                    },
                    {
                        'label': 'kVA (千伏安)',
                        'value': '16',
                    },
                    {
                        'label': 'MVA (兆伏安)',
                        'value': '17',
                    },
                    {
                        'label': 'VA (伏安)',
                        'value': '18',
                    },
                ],
                'type': '1',
                'deviceCode': 'HLGW2426003096_RS48512',
            },
            {
                'pointCode': 'col_CJLEbu',
                'pointName': '5#分变Ⅰ段_B相有功功率',
                'pointTypeId': '15',
                'pointTypeUnitId': '10',
                'pointTypeName': 'B相有功功率',
                'unit': 'kW',
                'gatewayCode': 'HLGW1012424003096',
                'subDeviceCode': 'HLGW2426003096_RS48511',
                'identifier': 'Pb',
                'dataType': 'float',
                'pointCodeLevel': 'B相有功功率>5#分变Ⅰ段>5#分变高压',
                'unitOptions': [
                    {
                        'label': 'kW (千瓦)',
                        'value': '10',
                    },
                    {
                        'label': 'MW (兆瓦)',
                        'value': '11',
                    },
                    {
                        'label': 'W (瓦)',
                        'value': '12',
                    },
                    {
                        'label': 'kvar (千乏)',
                        'value': '13',
                    },
                    {
                        'label': 'Mvar (兆乏)',
                        'value': '14',
                    },
                    {
                        'label': 'var (乏)',
                        'value': '15',
                    },
                    {
                        'label': 'kVA (千伏安)',
                        'value': '16',
                    },
                    {
                        'label': 'MVA (兆伏安)',
                        'value': '17',
                    },
                    {
                        'label': 'VA (伏安)',
                        'value': '18',
                    },
                ],
                'type': '1',
                'deviceCode': 'HLGW2426003096_RS48512',
            },
            {
                'pointCode': 'col_zljd5Q',
                'pointName': '5#分变Ⅰ段_C相有功功率',
                'pointTypeId': '16',
                'pointTypeUnitId': '10',
                'pointTypeName': 'C相有功功率',
                'unit': 'kW',
                'gatewayCode': 'HLGW1012424003096',
                'subDeviceCode': 'HLGW2426003096_RS48511',
                'identifier': 'Pc',
                'dataType': 'float',
                'pointCodeLevel': 'C相有功功率>5#分变Ⅰ段>5#分变高压',
                'unitOptions': [
                    {
                        'label': 'kW (千瓦)',
                        'value': '10',
                    },
                    {
                        'label': 'MW (兆瓦)',
                        'value': '11',
                    },
                    {
                        'label': 'W (瓦)',
                        'value': '12',
                    },
                    {
                        'label': 'kvar (千乏)',
                        'value': '13',
                    },
                    {
                        'label': 'Mvar (兆乏)',
                        'value': '14',
                    },
                    {
                        'label': 'var (乏)',
                        'value': '15',
                    },
                    {
                        'label': 'kVA (千伏安)',
                        'value': '16',
                    },
                    {
                        'label': 'MVA (兆伏安)',
                        'value': '17',
                    },
                    {
                        'label': 'VA (伏安)',
                        'value': '18',
                    },
                ],
                'type': '1',
                'deviceCode': 'HLGW2426003096_RS48512',
            },
            {
                'pointCode': 'col_lsIswr',
                'pointName': '5#分变Ⅰ段_峰电度',
                'pointTypeId': '2',
                'pointTypeUnitId': '1',
                'pointTypeName': '峰电度',
                'unit': 'kWh',
                'gatewayCode': 'HLGW1012424003096',
                'subDeviceCode': 'HLGW2426003096_RS48511',
                'identifier': 'PkWhP',
                'dataType': 'float',
                'pointCodeLevel': '峰电度>5#分变Ⅰ段>5#分变高压',
                'unitOptions': [
                    {
                        'label': 'kWh (千瓦时)',
                        'value': '1',
                    },
                    {
                        'label': 'MWh (兆瓦时)',
                        'value': '2',
                    },
                    {
                        'label': 'Wh (瓦时)',
                        'value': '3',
                    },
                    {
                        'label': 'kvarh (千乏时)',
                        'value': '4',
                    },
                    {
                        'label': 'Mvarh (兆乏时)',
                        'value': '5',
                    },
                    {
                        'label': 'varh (乏时)',
                        'value': '6',
                    },
                    {
                        'label': 'kVAh (千伏安时)',
                        'value': '7',
                    },
                    {
                        'label': 'MVAh (兆伏安时)',
                        'value': '8',
                    },
                    {
                        'label': 'VAh (伏安时)',
                        'value': '9',
                    },
                ],
                'type': '1',
                'deviceCode': 'HLGW2426003096_RS48512',
            },
            {
                'pointCode': 'col_EMJks8',
                'pointName': '5#分变Ⅰ段_总无功功率',
                'pointTypeId': '17',
                'pointTypeUnitId': '10',
                'pointTypeName': '总无功功率',
                'unit': 'kW',
                'gatewayCode': 'HLGW1012424003096',
                'subDeviceCode': 'HLGW2426003096_RS48511',
                'identifier': 'Q',
                'dataType': 'float',
                'pointCodeLevel': '总无功功率>5#分变Ⅰ段>5#分变高压',
                'unitOptions': [
                    {
                        'label': 'kW (千瓦)',
                        'value': '10',
                    },
                    {
                        'label': 'MW (兆瓦)',
                        'value': '11',
                    },
                    {
                        'label': 'W (瓦)',
                        'value': '12',
                    },
                    {
                        'label': 'kvar (千乏)',
                        'value': '13',
                    },
                    {
                        'label': 'Mvar (兆乏)',
                        'value': '14',
                    },
                    {
                        'label': 'var (乏)',
                        'value': '15',
                    },
                    {
                        'label': 'kVA (千伏安)',
                        'value': '16',
                    },
                    {
                        'label': 'MVA (兆伏安)',
                        'value': '17',
                    },
                    {
                        'label': 'VA (伏安)',
                        'value': '18',
                    },
                ],
                'type': '1',
                'deviceCode': 'HLGW2426003096_RS48512',
            },
            {
                'pointCode': 'col_JWPXcA',
                'pointName': '5#分变Ⅰ段_A相无功功率',
                'pointTypeId': '18',
                'pointTypeUnitId': '10',
                'pointTypeName': 'A相无功功率',
                'unit': 'kW',
                'gatewayCode': 'HLGW1012424003096',
                'subDeviceCode': 'HLGW2426003096_RS48511',
                'identifier': 'Qa',
                'dataType': 'float',
                'pointCodeLevel': 'A相无功功率>5#分变Ⅰ段>5#分变高压',
                'unitOptions': [
                    {
                        'label': 'kW (千瓦)',
                        'value': '10',
                    },
                    {
                        'label': 'MW (兆瓦)',
                        'value': '11',
                    },
                    {
                        'label': 'W (瓦)',
                        'value': '12',
                    },
                    {
                        'label': 'kvar (千乏)',
                        'value': '13',
                    },
                    {
                        'label': 'Mvar (兆乏)',
                        'value': '14',
                    },
                    {
                        'label': 'var (乏)',
                        'value': '15',
                    },
                    {
                        'label': 'kVA (千伏安)',
                        'value': '16',
                    },
                    {
                        'label': 'MVA (兆伏安)',
                        'value': '17',
                    },
                    {
                        'label': 'VA (伏安)',
                        'value': '18',
                    },
                ],
                'type': '1',
                'deviceCode': 'HLGW2426003096_RS48512',
            },
            {
                'pointCode': 'col_Kk2rua',
                'pointName': '5#分变Ⅰ段_B相无功功率',
                'pointTypeId': '19',
                'pointTypeUnitId': '10',
                'pointTypeName': 'B相无功功率',
                'unit': 'kW',
                'gatewayCode': 'HLGW1012424003096',
                'subDeviceCode': 'HLGW2426003096_RS48511',
                'identifier': 'Qb',
                'dataType': 'float',
                'pointCodeLevel': 'B相无功功率>5#分变Ⅰ段>5#分变高压',
                'unitOptions': [
                    {
                        'label': 'kW (千瓦)',
                        'value': '10',
                    },
                    {
                        'label': 'MW (兆瓦)',
                        'value': '11',
                    },
                    {
                        'label': 'W (瓦)',
                        'value': '12',
                    },
                    {
                        'label': 'kvar (千乏)',
                        'value': '13',
                    },
                    {
                        'label': 'Mvar (兆乏)',
                        'value': '14',
                    },
                    {
                        'label': 'var (乏)',
                        'value': '15',
                    },
                    {
                        'label': 'kVA (千伏安)',
                        'value': '16',
                    },
                    {
                        'label': 'MVA (兆伏安)',
                        'value': '17',
                    },
                    {
                        'label': 'VA (伏安)',
                        'value': '18',
                    },
                ],
                'type': '1',
                'deviceCode': 'HLGW2426003096_RS48512',
            },
            {
                'pointCode': 'col_XotKqi',
                'pointName': '5#分变Ⅰ段_C相无功功率',
                'pointTypeId': '20',
                'pointTypeUnitId': '10',
                'pointTypeName': 'C相无功功率',
                'unit': 'kW',
                'gatewayCode': 'HLGW1012424003096',
                'subDeviceCode': 'HLGW2426003096_RS48511',
                'identifier': 'Qc',
                'dataType': 'float',
                'pointCodeLevel': 'C相无功功率>5#分变Ⅰ段>5#分变高压',
                'unitOptions': [
                    {
                        'label': 'kW (千瓦)',
                        'value': '10',
                    },
                    {
                        'label': 'MW (兆瓦)',
                        'value': '11',
                    },
                    {
                        'label': 'W (瓦)',
                        'value': '12',
                    },
                    {
                        'label': 'kvar (千乏)',
                        'value': '13',
                    },
                    {
                        'label': 'Mvar (兆乏)',
                        'value': '14',
                    },
                    {
                        'label': 'var (乏)',
                        'value': '15',
                    },
                    {
                        'label': 'kVA (千伏安)',
                        'value': '16',
                    },
                    {
                        'label': 'MVA (兆伏安)',
                        'value': '17',
                    },
                    {
                        'label': 'VA (伏安)',
                        'value': '18',
                    },
                ],
                'type': '1',
                'deviceCode': 'HLGW2426003096_RS48512',
            },
            {
                'pointCode': 'col_CczrKL',
                'pointName': '5#分变Ⅰ段_尖电度',
                'pointTypeId': '5',
                'pointTypeUnitId': '1',
                'pointTypeName': '尖电度',
                'unit': 'kWh',
                'gatewayCode': 'HLGW1012424003096',
                'subDeviceCode': 'HLGW2426003096_RS48511',
                'identifier': 'TkWhP',
                'dataType': 'float',
                'pointCodeLevel': '尖电度>5#分变Ⅰ段>5#分变高压',
                'unitOptions': [
                    {
                        'label': 'kWh (千瓦时)',
                        'value': '1',
                    },
                    {
                        'label': 'MWh (兆瓦时)',
                        'value': '2',
                    },
                    {
                        'label': 'Wh (瓦时)',
                        'value': '3',
                    },
                    {
                        'label': 'kvarh (千乏时)',
                        'value': '4',
                    },
                    {
                        'label': 'Mvarh (兆乏时)',
                        'value': '5',
                    },
                    {
                        'label': 'varh (乏时)',
                        'value': '6',
                    },
                    {
                        'label': 'kVAh (千伏安时)',
                        'value': '7',
                    },
                    {
                        'label': 'MVAh (兆伏安时)',
                        'value': '8',
                    },
                    {
                        'label': 'VAh (伏安时)',
                        'value': '9',
                    },
                ],
                'type': '1',
                'deviceCode': 'HLGW2426003096_RS48512',
            },
            {
                'pointCode': 'col_i83cDK',
                'pointName': '5#分变Ⅰ段_A相电压',
                'pointTypeId': '29',
                'pointTypeUnitId': '21',
                'pointTypeName': 'A相电压',
                'unit': 'KV',
                'gatewayCode': 'HLGW1012424003096',
                'subDeviceCode': 'HLGW2426003096_RS48511',
                'identifier': 'Ua',
                'dataType': 'float',
                'pointCodeLevel': 'A相电压>5#分变Ⅰ段>5#分变高压',
                'unitOptions': [
                    {
                        'label': 'KV (千伏特)',
                        'value': '21',
                    },
                    {
                        'label': 'mV (毫伏)',
                        'value': '22',
                    },
                    {
                        'label': 'V (伏特)',
                        'value': '23',
                    },
                ],
                'type': '1',
                'deviceCode': 'HLGW2426003096_RS48512',
            },
            {
                'pointCode': 'col_aUd4mK',
                'pointName': '5#分变Ⅰ段_AB线电压',
                'pointTypeId': '32',
                'pointTypeUnitId': '21',
                'pointTypeName': 'AB线电压',
                'unit': 'KV',
                'gatewayCode': 'HLGW1012424003096',
                'subDeviceCode': 'HLGW2426003096_RS48511',
                'identifier': 'Uab',
                'dataType': 'float',
                'pointCodeLevel': 'AB线电压>5#分变Ⅰ段>5#分变高压',
                'unitOptions': [
                    {
                        'label': 'KV (千伏特)',
                        'value': '21',
                    },
                    {
                        'label': 'mV (毫伏)',
                        'value': '22',
                    },
                    {
                        'label': 'V (伏特)',
                        'value': '23',
                    },
                ],
                'type': '1',
                'deviceCode': 'HLGW2426003096_RS48512',
            },
            {
                'pointCode': 'col_Enpjd0',
                'pointName': '5#分变Ⅰ段_B相电压',
                'pointTypeId': '30',
                'pointTypeUnitId': '21',
                'pointTypeName': 'B相电压',
                'unit': 'KV',
                'gatewayCode': 'HLGW1012424003096',
                'subDeviceCode': 'HLGW2426003096_RS48511',
                'identifier': 'Ub',
                'dataType': 'float',
                'pointCodeLevel': 'B相电压>5#分变Ⅰ段>5#分变高压',
                'unitOptions': [
                    {
                        'label': 'KV (千伏特)',
                        'value': '21',
                    },
                    {
                        'label': 'mV (毫伏)',
                        'value': '22',
                    },
                    {
                        'label': 'V (伏特)',
                        'value': '23',
                    },
                ],
                'type': '1',
                'deviceCode': 'HLGW2426003096_RS48512',
            },
            {
                'pointCode': 'col_CJGnXS',
                'pointName': '5#分变Ⅰ段_BC线电压',
                'pointTypeId': '33',
                'pointTypeUnitId': '21',
                'pointTypeName': 'BC线电压',
                'unit': 'KV',
                'gatewayCode': 'HLGW1012424003096',
                'subDeviceCode': 'HLGW2426003096_RS48511',
                'identifier': 'Ubc',
                'dataType': 'float',
                'pointCodeLevel': 'BC线电压>5#分变Ⅰ段>5#分变高压',
                'unitOptions': [
                    {
                        'label': 'KV (千伏特)',
                        'value': '21',
                    },
                    {
                        'label': 'mV (毫伏)',
                        'value': '22',
                    },
                    {
                        'label': 'V (伏特)',
                        'value': '23',
                    },
                ],
                'type': '1',
                'deviceCode': 'HLGW2426003096_RS48512',
            },
            {
                'pointCode': 'col_gpV76o',
                'pointName': '5#分变Ⅰ段_C相电压',
                'pointTypeId': '31',
                'pointTypeUnitId': '21',
                'pointTypeName': 'C相电压',
                'unit': 'KV',
                'gatewayCode': 'HLGW1012424003096',
                'subDeviceCode': 'HLGW2426003096_RS48511',
                'identifier': 'Uc',
                'dataType': 'float',
                'pointCodeLevel': 'C相电压>5#分变Ⅰ段>5#分变高压',
                'unitOptions': [
                    {
                        'label': 'KV (千伏特)',
                        'value': '21',
                    },
                    {
                        'label': 'mV (毫伏)',
                        'value': '22',
                    },
                    {
                        'label': 'V (伏特)',
                        'value': '23',
                    },
                ],
                'type': '1',
                'deviceCode': 'HLGW2426003096_RS48512',
            },
            {
                'pointCode': 'col_oqWQa6',
                'pointName': '5#分变Ⅰ段_CA线电压',
                'pointTypeId': '34',
                'pointTypeUnitId': '21',
                'pointTypeName': 'CA线电压',
                'unit': 'KV',
                'gatewayCode': 'HLGW1012424003096',
                'subDeviceCode': 'HLGW2426003096_RS48511',
                'identifier': 'Uca',
                'dataType': 'float',
                'pointCodeLevel': 'CA线电压>5#分变Ⅰ段>5#分变高压',
                'unitOptions': [
                    {
                        'label': 'KV (千伏特)',
                        'value': '21',
                    },
                    {
                        'label': 'mV (毫伏)',
                        'value': '22',
                    },
                    {
                        'label': 'V (伏特)',
                        'value': '23',
                    },
                ],
                'type': '1',
                'deviceCode': 'HLGW2426003096_RS48512',
            },
            {
                'pointCode': 'col_3Pzvrp',
                'pointName': '5#分变Ⅰ段_谷电度',
                'pointTypeId': '4',
                'pointTypeUnitId': '1',
                'pointTypeName': '谷电度',
                'unit': 'kWh',
                'gatewayCode': 'HLGW1012424003096',
                'subDeviceCode': 'HLGW2426003096_RS48511',
                'identifier': 'VkWhP',
                'dataType': 'float',
                'pointCodeLevel': '谷电度>5#分变Ⅰ段>5#分变高压',
                'unitOptions': [
                    {
                        'label': 'kWh (千瓦时)',
                        'value': '1',
                    },
                    {
                        'label': 'MWh (兆瓦时)',
                        'value': '2',
                    },
                    {
                        'label': 'Wh (瓦时)',
                        'value': '3',
                    },
                    {
                        'label': 'kvarh (千乏时)',
                        'value': '4',
                    },
                    {
                        'label': 'Mvarh (兆乏时)',
                        'value': '5',
                    },
                    {
                        'label': 'varh (乏时)',
                        'value': '6',
                    },
                    {
                        'label': 'kVAh (千伏安时)',
                        'value': '7',
                    },
                    {
                        'label': 'MVAh (兆伏安时)',
                        'value': '8',
                    },
                    {
                        'label': 'VAh (伏安时)',
                        'value': '9',
                    },
                ],
                'type': '1',
                'deviceCode': 'HLGW2426003096_RS48512',
            },
            {
                'pointCode': 'col_q4PPKd',
                'pointName': '5#分变Ⅰ段_A相电流总谐波畸变率',
                'pointTypeId': '958',
                'pointTypeUnitId': '973',
                'pointTypeName': 'A相电流总谐波畸变率',
                'unit': '%',
                'gatewayCode': 'HLGW1012424003096',
                'subDeviceCode': 'HLGW2426003096_RS48511',
                'identifier': 'XBia',
                'dataType': 'float',
                'pointCodeLevel': 'A相电流总谐波畸变率>5#分变Ⅰ段>5#分变高压',
                'unitOptions': [
                    {
                        'label': '% (百分比)',
                        'value': '973',
                    },
                ],
                'editpointTypeName': False,
                'type': '1',
                'deviceCode': 'HLGW2426003096_RS48512',
            },
            {
                'pointCode': 'col_pJmgDw',
                'pointName': '5#分变Ⅰ段_B相电流总谐波畸变率',
                'pointTypeId': '959',
                'pointTypeUnitId': '973',
                'pointTypeName': 'B相电流总谐波畸变率',
                'unit': '% (百分比)',
                'gatewayCode': 'HLGW1012424003096',
                'subDeviceCode': 'HLGW2426003096_RS48511',
                'identifier': 'XBib',
                'dataType': 'float',
                'pointCodeLevel': 'B相电流总谐波畸变率>5#分变Ⅰ段>5#分变高压',
                'unitOptions': [
                    {
                        'label': '% (百分比)',
                        'value': '973',
                    },
                ],
                'editpointTypeName': False,
                'editUnit': False,
                'type': '1',
                'deviceCode': 'HLGW2426003096_RS48512',
            },
            {
                'pointCode': 'col_eJHm8d',
                'pointName': '5#分变Ⅰ段_C相电流总谐波畸变率',
                'pointTypeId': '960',
                'pointTypeUnitId': '973',
                'pointTypeName': 'C相电流总谐波畸变率',
                'unit': '% (百分比)',
                'gatewayCode': 'HLGW1012424003096',
                'subDeviceCode': 'HLGW2426003096_RS48511',
                'identifier': 'XBic',
                'dataType': 'float',
                'pointCodeLevel': 'C相电流总谐波畸变率>5#分变Ⅰ段>5#分变高压',
                'unitOptions': [
                    {
                        'label': '% (百分比)',
                        'value': '973',
                    },
                ],
                'editpointTypeName': False,
                'editUnit': False,
                'type': '1',
                'deviceCode': 'HLGW2426003096_RS48512',
            },
            {
                'pointCode': 'col_JWD4ed',
                'pointName': '5#分变Ⅰ段_A相电压总谐波畸变率',
                'pointTypeId': '955',
                'pointTypeUnitId': '973',
                'pointTypeName': 'A相电压总谐波畸变率',
                'unit': '% (百分比)',
                'gatewayCode': 'HLGW1012424003096',
                'subDeviceCode': 'HLGW2426003096_RS48511',
                'identifier': 'XBua',
                'dataType': 'float',
                'pointCodeLevel': 'A相电压总谐波畸变率>5#分变Ⅰ段>5#分变高压',
                'unitOptions': [
                    {
                        'label': '% (百分比)',
                        'value': '973',
                    },
                ],
                'editpointTypeName': False,
                'editUnit': False,
                'type': '1',
                'deviceCode': 'HLGW2426003096_RS48512',
            },
            {
                'pointCode': 'col_J4qGPU',
                'pointName': '5#分变Ⅰ段_B相电压总谐波畸变率',
                'pointTypeId': '956',
                'pointTypeUnitId': '973',
                'pointTypeName': 'B相电压总谐波畸变率',
                'unit': '% (百分比)',
                'gatewayCode': 'HLGW1012424003096',
                'subDeviceCode': 'HLGW2426003096_RS48511',
                'identifier': 'XBub',
                'dataType': 'float',
                'pointCodeLevel': 'B相电压总谐波畸变率>5#分变Ⅰ段>5#分变高压',
                'unitOptions': [
                    {
                        'label': '% (百分比)',
                        'value': '973',
                    },
                ],
                'editpointTypeName': False,
                'editUnit': False,
                'type': '1',
                'deviceCode': 'HLGW2426003096_RS48512',
            },
            {
                'pointCode': 'col_mYYrFe',
                'pointName': '5#分变Ⅰ段_C相电压总谐波畸变率',
                'pointTypeId': '957',
                'pointTypeUnitId': '973',
                'pointTypeName': 'C相电压总谐波畸变率',
                'unit': '%',
                'gatewayCode': 'HLGW1012424003096',
                'subDeviceCode': 'HLGW2426003096_RS48511',
                'identifier': 'XBuc',
                'dataType': 'float',
                'pointCodeLevel': 'C相电压总谐波畸变率>5#分变Ⅰ段>5#分变高压',
                'unitOptions': [
                    {
                        'label': '% (百分比)',
                        'value': '973',
                    },
                ],
                'editUnit': False,
                'type': '1',
                'deviceCode': 'HLGW2426003096_RS48512',
            },
            {
                'pointCode': 'col_KXJdSi',
                'pointName': '5#分变Ⅰ段_负无功电度',
                'pointTypeId': '12',
                'pointTypeUnitId': '1',
                'pointTypeName': '负无功电度',
                'unit': 'kWh',
                'gatewayCode': 'HLGW1012424003096',
                'subDeviceCode': 'HLGW2426003096_RS48511',
                'identifier': 'kVarhN',
                'dataType': 'float',
                'pointCodeLevel': '负无功电度>5#分变Ⅰ段>5#分变高压',
                'unitOptions': [
                    {
                        'label': 'kWh (千瓦时)',
                        'value': '1',
                    },
                    {
                        'label': 'MWh (兆瓦时)',
                        'value': '2',
                    },
                    {
                        'label': 'Wh (瓦时)',
                        'value': '3',
                    },
                    {
                        'label': 'kvarh (千乏时)',
                        'value': '4',
                    },
                    {
                        'label': 'Mvarh (兆乏时)',
                        'value': '5',
                    },
                    {
                        'label': 'varh (乏时)',
                        'value': '6',
                    },
                    {
                        'label': 'kVAh (千伏安时)',
                        'value': '7',
                    },
                    {
                        'label': 'MVAh (兆伏安时)',
                        'value': '8',
                    },
                    {
                        'label': 'VAh (伏安时)',
                        'value': '9',
                    },
                ],
                'editUnit': False,
                'type': '1',
                'deviceCode': 'HLGW2426003096_RS48512',
            },
            {
                'pointCode': 'col_8l6YXr',
                'pointName': '5#分变Ⅰ段_正无功电度',
                'pointTypeId': '11',
                'pointTypeUnitId': '1',
                'pointTypeName': '正无功电度',
                'unit': 'kWh',
                'gatewayCode': 'HLGW1012424003096',
                'subDeviceCode': 'HLGW2426003096_RS48511',
                'identifier': 'kVarhP',
                'dataType': 'float',
                'pointCodeLevel': '正无功电度>5#分变Ⅰ段>5#分变高压',
                'unitOptions': [
                    {
                        'label': 'kWh (千瓦时)',
                        'value': '1',
                    },
                    {
                        'label': 'MWh (兆瓦时)',
                        'value': '2',
                    },
                    {
                        'label': 'Wh (瓦时)',
                        'value': '3',
                    },
                    {
                        'label': 'kvarh (千乏时)',
                        'value': '4',
                    },
                    {
                        'label': 'Mvarh (兆乏时)',
                        'value': '5',
                    },
                    {
                        'label': 'varh (乏时)',
                        'value': '6',
                    },
                    {
                        'label': 'kVAh (千伏安时)',
                        'value': '7',
                    },
                    {
                        'label': 'MVAh (兆伏安时)',
                        'value': '8',
                    },
                    {
                        'label': 'VAh (伏安时)',
                        'value': '9',
                    },
                ],
                'type': '1',
                'deviceCode': 'HLGW2426003096_RS48512',
            },
            {
                'pointCode': 'col_axTSG7',
                'pointName': '5#分变Ⅰ段_负有功电度',
                'pointTypeId': '6',
                'pointTypeUnitId': '1',
                'pointTypeName': '负有功电度',
                'unit': 'kWh',
                'gatewayCode': 'HLGW1012424003096',
                'subDeviceCode': 'HLGW2426003096_RS48511',
                'identifier': 'kWhN',
                'dataType': 'float',
                'pointCodeLevel': '负有功电度>5#分变Ⅰ段>5#分变高压',
                'unitOptions': [
                    {
                        'label': 'kWh (千瓦时)',
                        'value': '1',
                    },
                    {
                        'label': 'MWh (兆瓦时)',
                        'value': '2',
                    },
                    {
                        'label': 'Wh (瓦时)',
                        'value': '3',
                    },
                    {
                        'label': 'kvarh (千乏时)',
                        'value': '4',
                    },
                    {
                        'label': 'Mvarh (兆乏时)',
                        'value': '5',
                    },
                    {
                        'label': 'varh (乏时)',
                        'value': '6',
                    },
                    {
                        'label': 'kVAh (千伏安时)',
                        'value': '7',
                    },
                    {
                        'label': 'MVAh (兆伏安时)',
                        'value': '8',
                    },
                    {
                        'label': 'VAh (伏安时)',
                        'value': '9',
                    },
                ],
                'type': '1',
                'deviceCode': 'HLGW2426003096_RS48512',
            },
            {
                'pointCode': 'col_Rv7Tal',
                'pointName': '5#分变Ⅰ段_正有功电度',
                'pointTypeId': '1',
                'pointTypeUnitId': '1',
                'pointTypeName': '正有功电度',
                'unit': 'kWh',
                'gatewayCode': 'HLGW1012424003096',
                'subDeviceCode': 'HLGW2426003096_RS48511',
                'identifier': 'kWhP',
                'dataType': 'float',
                'pointCodeLevel': '正有功电度>5#分变Ⅰ段>5#分变高压',
                'unitOptions': [
                    {
                        'label': 'kWh (千瓦时)',
                        'value': '1',
                    },
                    {
                        'label': 'MWh (兆瓦时)',
                        'value': '2',
                    },
                    {
                        'label': 'Wh (瓦时)',
                        'value': '3',
                    },
                    {
                        'label': 'kvarh (千乏时)',
                        'value': '4',
                    },
                    {
                        'label': 'Mvarh (兆乏时)',
                        'value': '5',
                    },
                    {
                        'label': 'varh (乏时)',
                        'value': '6',
                    },
                    {
                        'label': 'kVAh (千伏安时)',
                        'value': '7',
                    },
                    {
                        'label': 'MVAh (兆伏安时)',
                        'value': '8',
                    },
                    {
                        'label': 'VAh (伏安时)',
                        'value': '9',
                    },
                ],
                'type': '1',
                'deviceCode': 'HLGW2426003096_RS48512',
            },
        ]


        for item in json_data:

            pointCodeAttributename=item.get('pointCodeLevel').split('>')[0]
            if pointCodeAttributename==modelName:
                item["pointCode"]=f"col_{self.generate_random_string(length=6)}"
                item['pointName']=f"{deviceName}_{modelName}"
                item['gatewayCode']=gatewayCode
                item['subDeviceCode']=f"{devicecode}"
                item['pointCodeLevel']=f"{modelName}>{deviceName}>{gatewayName}"
                item['deviceCode']=devicecode

                return item

    def deviceSynchronization_bymodel(self,devicecode):
        '''
        通过模板同步数据
        1.获取json模板
        2.获取所有子设备和分组信息。设备code和对应的网关code
        3.将信息替换json模板然后创建
        :return:
        '''

        # devicecode="HLGW1012426003172_RS48511"

        gatewayCode=devicecode.split("_")[0]

        # 设备code和设备名关系表
        devicepage =self.devicepage().get('data').get('records')
        devicedict={}
        for itme in devicepage:
            devicedict[itme.get('deviceCode')]=itme.get('deviceName')

        deviceName=devicedict.get(devicecode)

        # 设备同步信息查询，
        params = {'size': '1000', 'current': '1', 'gatewayCode': gatewayCode,
                  'deviceCode': devicecode, 'subDeviceName': deviceName, }
        pointCodegetThingsModelsDetailPage=self.pointCodegetThingsModelsDetailPage(params=params).get('data').get('records')


        addpointCodegetThingsModelinfo=[]
        for pointCodegetThingsModelsDetailPageinfo in pointCodegetThingsModelsDetailPage:
            gatewayName=pointCodegetThingsModelsDetailPageinfo.get('gatewayName')
            modelName=pointCodegetThingsModelsDetailPageinfo.get('modelName')
            exist=pointCodegetThingsModelsDetailPageinfo.get('exist')

            if exist==True: #判断是否已经创建了采集点
                continue
            # productCode=pointCodegetThingsModelsDetailPageinfo.get('productCode')

            # 获取单个点位匹配后的点位信息,然后依次添加搭配；列表
            itme=self.deviceSynchronization_jsonmodel(
                gatewayName=gatewayName,modelName=modelName,
                deviceName=deviceName,devicecode=devicecode,
                gatewayCode=gatewayCode)
            addpointCodegetThingsModelinfo.append(itme)

        # 当某个设备下已经添加过该点位信息时
        if len(addpointCodegetThingsModelinfo)==0:
            WARNING.logger.warning(f"{deviceName}/{devicecode},该设备下已经添加过该点位信息")
            return "该设备下已经添加过该点位信息"

        # print(addpointCodegetThingsModelinfo)
        # return 1
        # 同步新增采集点
        self.pointCode(json_data=addpointCodegetThingsModelinfo,requsetmethod='POST')

    def batchdeviceSynchronization_bymodel(self):
        '''
        批量通过模板同步数据
        1.获取每个设备中需要同步点位的json入参信息。
        2.根据关键字查询需要同步的设备信息，获取设备code和对应的网关code信息
        3.将json入参中的网关和设备信息与需要同步的设备信息的网关code和设备code进行替换，生成新的入参
        2.调用同步更新的接口，同步采集点。
        :return:
        '''

        devicepage=self.devicepage(deviceCode="HLGW").get('data').get('records')
        devicecodelist=[i.get("deviceCode") for i in devicepage]


        for devicecode in devicecodelist:
            # devicecode='HLGW1012426003186_RS48511'
            if 'HLGW1012424003096' not in devicecode:
                continue

            try:
                self.deviceSynchronization_bymodel(devicecode=devicecode)
            except Exception as e:
                WARNING.logger.warning(f"{devicecode},同步采集点失败，失败原因：{e}")


    def firstpointtypeunit(self):
        '''
        根据点位类型获取，第一个单位值
        :return:{点位类型：单位id}
        '''

        pointTypepinfodict={}

        pointTypepage=self.pointTypepage().get('data').get('records')
        for pointTypepageinfo in pointTypepage:
            pointTypeId=pointTypepageinfo.get('id')
            pointTypeUnits=pointTypepageinfo.get('pointTypeUnits')
            if len(pointTypeUnits)==0:
                pointTypeUnitId=''
            else:
                pointTypeUnitId=pointTypeUnits[0].get('unitId')

            pointTypepinfodict[pointTypeId]=pointTypeUnitId

        return pointTypepinfodict


    def batchchangepointTypeinfo(self):
        '''
        批量更新设备点位信息
        :return:
        '''

        firstpointtypeunit=self.firstpointtypeunit() # 获取点位类型的第一个单位id

        pointCodepage=self.pointCodepage().get('data').get('records')
        for pointCodepageinfo in pointCodepage:
            id=pointCodepageinfo.get('id')
            pointName=pointCodepageinfo.get('pointName')
            pointTypeId=pointCodepageinfo.get('pointTypeId')
            pointTypeName=pointCodepageinfo.get('pointTypeName')
            deviceCode=pointCodepageinfo.get('deviceCode')
            pointTypeUnitId=pointCodepageinfo.get('pointTypeUnitId',"")
            deviceName=pointCodepageinfo.get('deviceName')
            pointCodeLevel=pointCodepageinfo.get('pointCodeLevel')
            gatewayname=str(pointCodeLevel).split('>')[2]

            # 统一更新点位id
            # if pointTypeId=='954':
            # if '功功率' in pointTypeName:
            #     pointTypeUnitId='10'
            #     json_data = {
            #         'id': f'{id}',
            #         'pointName': f'{pointName}',
            #         'pointTypeId': f'{pointTypeId}',
            #         'pointTypeUnitId': f'{pointTypeUnitId}',
            #     }


            # 统一更改名字
            if '4#分变' in gatewayname:
                json_data = {
                    'id': f'{id}',
                    'pointName': f"{deviceName}_{pointTypeName}", # 点位名称默认名字 设备名称加物模型名称（点位类型）
                    'pointTypeId': f'{pointTypeId}',
                    'pointTypeUnitId': f'{firstpointtypeunit.get(pointTypeId)}',
                }

                # 更新点位设备信息
                self.pointCode(requsetmethod='PUT',json_data=json_data)



if __name__ == '__main__':
    task=DeviceSynchronizationWay()
    # task.batchchangepointTypeinfo()

    # print(task.generate_random_string())

    task.batchdeviceSynchronization_bymodel()










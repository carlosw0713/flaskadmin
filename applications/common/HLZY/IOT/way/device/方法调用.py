# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2025/3/10
Description: <Brief description of the file>
"""
from applications.common.HLZY.IOT.way.device.iotdevicealarm import iotdevicedataalarm

kwargs = {
    'auth_info': {'data': {'username': 'admin', 'password': 'bMv0b7CLc4UJjh0='},
                  'host': 'https://iiot.inco-plat.com'},
    'input_params': {'devicetimetype': {'HLGW': 900, 'dev': 240, 'NO': 57600},
                     'userinfo': 'https://iot-cluster-dev.heilansc.cn',
                     'alarmdeviceinfolist': []},

    'notification_config': {
        'webhook': 'https://oapi.dingtalk.com/robot/send?access_token=d93246056e51aed5a10bc70daad371de93557d4f1b41d5662c0506dc0e306932',
        'secret': 'SECe47d5a33a263cfc88e9a667c46da0cf7854fd683cd84cebe31e7e524b8b60cc4'
    }
}

iotdevicedataalarm(**kwargs)
print('直接调用方法执行')
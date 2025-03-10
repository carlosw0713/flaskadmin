# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2025/3/10
Description: <Brief description of the file>
"""
import requests

def generate_curl_command(response):
    # 获取请求的URL
    url = response.url

    # 获取请求的方法
    method = response.request.method

    # 获取请求的头部信息
    headers = response.request.headers

    # 构建curl命令的基本部分
    curl_command = f"curl -X {method} '{url}'"

    # 添加头部信息到curl命令中
    for header, value in headers.items():
        curl_command += f" -H '{header}: {value}'"

    # 如果是POST请求，添加POST数据到curl命令中
    if method == 'POST':
        data = response.request.body
        if data:
            try:
                # 尝试解码数据（通常是JSON）
                data_str = data.decode('utf-8')
                # 将数据转义并添加到curl命令中
                curl_command += f" -d '{data_str}'"
            except UnicodeDecodeError:
                # 如果无法解码，直接添加二进制数据
                curl_command += f" --data-binary '{data}'"

    # 返回生成的curl命令
    return curl_command


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

host='http://127.0.0.1:5000'
resp=requests.post(f'{host}/hlzyscript/iotdevicealarm', json=kwargs)
print(f'响应结果{resp.json()}\n')


print(f"获取curl\n{generate_curl_command(resp)}")
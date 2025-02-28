# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/12/26
Description: <Brief description of the file>
"""
from public.file_tool.exl_way import append_csv_data
from applications.common.HLZY.IOT import *
class GatewaySet:

    def __init__(self):
        self.uri= ""
        self.herader= ""
        self.cookies= ""


    def test1(self):
        import requests

        cookies = {
            'jxl_ga': 'GA1.1.1342519037.1733798712',
            'jxl_ga_3YK6Y5HC9N': 'GS1.1.1733798711.1.1.1733799482.0.0.0',
            'hb_MA-B8B4-DCBCC6752B4F_source': 'op.heilansc.cn',
        }

        headers = {
            'Accept': 'application/json',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Authorization': 'Bearer l60of7Lf48V4Hm0nG5GZN0uSkdkM8Pch',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=UTF-8',
            # Requests sorts cookies= alphabetically
            # 'Cookie': 'jxl_ga=GA1.1.1342519037.1733798712; jxl_ga_3YK6Y5HC9N=GS1.1.1733798711.1.1.1733799482.0.0.0; hb_MA-B8B4-DCBCC6752B4F_source=op.heilansc.cn',
            'Origin': 'https://676baa14979de6bc68a4db8d.iot.heilansc.com:83',
            'Referer': 'https://676baa14979de6bc68a4db8d.iot.heilansc.com:83/edge-computing/apps/device/cloud',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
            'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        json_data = {
            'device_supervisor': {
                'clouds': {
                    '0000676cf497bbff': {
                        '_id': '0000676cf497bbff',
                        'name': '苏南码头正式环境',
                        'type': 'Standard MQTT',
                        'cacheSize': 10000,
                        'enable': 1,
                        'args': {
                            'host': '222.191.251.12',
                            'port': 1883,
                            'clientId': 'HLGW1012426003172',
                            'auth': 1,
                            'tls': 0,
                            'cleanSession': 0,
                            'mqttVersion': 'v3.1.1',
                            'keepalive': 60,
                            'key': '',
                            'cert': '',
                            'rootCA': '',
                            'verifyServer': 0,
                            'verifyClient': 0,
                            'username': 'HLGW1012426003172@hlsc',
                            'passwd': 'HLGW1012426003172&hlsc',
                            'willQos': 0,
                            'willRetain': 0,
                            'willTopic': '',
                            'willPayload': '',
                        },
                    },
                },
            },
        }

        response = requestSession.put('https://676baa14979de6bc68a4db8d.iot.heilansc.com:83/v1/api/dsconfig', cookies=cookies,
                                headers=headers, json=json_data)

        resp = response.json()
        curl = generate_curl_command(response)
        if resp.get('code') == 0:
            INFO.logger.info(f"成功，返回信息：{resp}")
            return resp
        else:
            ERROR.logger.error(f"失败，返回信息：{resp}")


if __name__ == '__main__':
    task=GatewaySet()
    task.test1()
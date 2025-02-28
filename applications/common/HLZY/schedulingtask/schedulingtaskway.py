# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/11/13
Description: <Brief description of the file>
"""
from applications.common.HLZY.IOT import *

class SchedulingTaskWay:

    def __init__(self):

        self.cookies = {
            'access_token': 'd55a8615-3417-495a-8950-2707b629123a',
        }

        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Authorization': 'Bearer e2abf2c3-bbcf-4369-9d06-2b3b4d39a68a',
            'Connection': 'keep-alive',
            # 'Cookie': 'access_token=d55a8615-3417-495a-8950-2707b629123a',
            'Referer': 'https://iiot-tk-4u.heilansc.cn/products/productCenter',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            'X-Biz-App-Name': 'IOT',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        self.uri='https://iiot-tk-4u.heilansc.cn'


    def websvcjobAdmintrigger(self):
        '''
        执行调度任务 executorParam 2024/2024-11/2024-11-13
        :return:
        '''

        json_data = {
            'id': '12', #执行任务id
            'executorParam': '2024-11',
        }

        response = requests.post(f'{self.uri}/api/ems-biz-websvc/jobAdmin/trigger',
                                 cookies=self.cookies, headers=self.headers, json=json_data)

        resp = response.json()
        curl = generate_curl_command(response)
        result = resp.get('data')
        if resp.get('code') == 0:
            INFO.logger.info(f"iot产品删除设备成功，")
            return result
        else:
            ERROR.logger.error(f"iot产品删除设备失败，返回信息：{resp}")


if __name__ == '__main__':
    task=SchedulingTaskWay()
# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/11/21
Description: <Brief description of the file>
"""
import math


def calculate_power_factor(active_power, reactive_power):
    """
    计算功率因数

    :param active_power: 正向有功电量 (单位: kW)
    :param reactive_power: 正向无功电量 (单位: kVAR)
    :return: 功率因数 (PF)
    """
    if active_power == 0:
        return 0  # 避免除以零的情况

    # 计算视在功率
    apparent_power = math.sqrt(active_power**2 + reactive_power**2)

    # 计算功率因数
    power_factor = active_power / apparent_power

    return power_factor

def get_data():
    import requests

    cookies = {
        'access_token': 'a552b78a-1e4b-42d8-bafe-cefb57a830a2',
        'tenant_id': '1854087719241240577',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Authorization': 'Bearer a552b78a-1e4b-42d8-bafe-cefb57a830a2',
        'Connection': 'keep-alive',
        # Already added when you pass json=
        # 'Content-Type': 'application/json',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'access_token=a552b78a-1e4b-42d8-bafe-cefb57a830a2; tenant_id=1854087719241240577',
        'Origin': 'https://saas-ems-test.heilansc.cn',
        'Referer': 'https://saas-ems-test.heilansc.cn/energeManage/peakValley',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'TENANT-ID': '1854087719241240577',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'X-Biz-App-Name': 'EMS',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    json_data = {
        'timeType': 'day',
        'startTime': '2024-10-21 00:00:00',
        'endTime': '2024-11-21 23:59:59',
        'energyId': '24',
        'energyDimensionId': '2',
        'businessAttributesCode': '电',
        'menuId': '1856260902562623489',
        'dimensionId': '1',
        'groupId': '20',
        'dataType': 1,
    }

    response = requests.post(
        'https://saas-ems-test.heilansc.cn/api/ems-analysis-websvc/cumulativeAnalysis/peakValleyAnalysis',
        cookies=cookies, headers=headers, json=json_data)

    resp=response.json()
    if resp.get('code') == 0:
        data=resp['data']
        return data
    else:
        Exception (resp['message'])

def runtest():

    data=get_data()
    for item in data:
        total=item['total']
        var=item['var']
        cos=item['cos']
        pf=calculate_power_factor(total,var)
        print(pf)
        if pf !=cos:
            print(item)




if __name__ == '__main__':

    # runtest()
    print(calculate_power_factor(2566,2588))


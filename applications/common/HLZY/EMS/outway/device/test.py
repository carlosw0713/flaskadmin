# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/11/22
Description: <Brief description of the file>
"""

from applications.common.HLZY.IOT import *

def add_indicator(json_data):
    '''
    指标应用添加
    :param json_data:
    :return:
    '''
    import requests

    cookies = {
        'access_token': '4d0c3b6a-747b-44ff-b40d-2e009ee06270',
        'tenant_id': '1854087719241240577',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Authorization': 'Bearer 4d0c3b6a-747b-44ff-b40d-2e009ee06270',
        'Connection': 'keep-alive',
        # Already added when you pass json=
        # 'Content-Type': 'application/json',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'access_token=4d0c3b6a-747b-44ff-b40d-2e009ee06270; tenant_id=1854087719241240577',
        'Origin': 'https://saas-ems-test.heilansc.cn',
        'Referer': 'https://saas-ems-test.heilansc.cn/indicator/indicatorApply',
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



    response = requests.post('https://saas-ems-test.heilansc.cn/api/ems-analysis-websvc/indicator-app/add', cookies=cookies, headers=headers, json=json_data)

    resp = response.json()
    curl = generate_curl_command(response)
    if resp.get('code') == 0:
        INFO.logger.info(f"指标应用添加成功，请求信息{json_data}")
        result = resp.get('data')
        return result
    else:
        ERROR.logger.error(f"指标应用添加失败，返回信息：{resp}\n请求信息{json_data}")

def run_bacthadd():
    json_data = {
        'id': '',
        'appSceneId': '17',
        'menuId': '1839599045216047106',
        'businessName': '能源驾驶舱',
        'businessAttributes': '能耗',
        'businessAttributesCode': '电',

        'indicatorId': '',
        'indicatorCode': 'M_LOlOJ',
        'indicatorGroupId': '25',
        'remark': '',
    }

    businessAttributeslist=['能耗','碳排','用量','负荷']
    businessAttributesCodelist=['电','水','气']

    for businessAttributes in businessAttributeslist:

        for businessAttributesCode in businessAttributesCodelist:

            json_data['businessAttributes']=businessAttributes
            json_data['businessAttributesCode']=businessAttributesCode

            add_indicator(json_data=json_data)





if __name__ == '__main__':
    run_bacthadd()


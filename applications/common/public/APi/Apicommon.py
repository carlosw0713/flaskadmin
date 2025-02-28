#!usrbinenv python
# -*- coding: utf-8 -*-
# @Time    : 2024716 16:48
# @Author  : carlos
# @Email   : carlos.w.0713@outlook.com
# @File    : Apicommon.py
# @IDE     : PyCharm
# @REMARKS : 备注
import json

import requests
# 创建一个全局的Session对象
requestSession = requests.Session()
# 设置所有的请求都将不验证SSL证书
requestSession.verify = False

def get_keys_by_value(dictionary, value):
    """根据值获取字典中的键"""
    keys = [key for key, val in dictionary.items() if val == value]
    return keys

def extract_dict_items(source_dict, keys_to_extract):
        """
        从给定的字典中提取指定键的键值对。

        :param source_dict: 原始字典
        :param keys_to_extract: 需要提取的键的列表
        :return: 包含指定键值对的新字典
        """
        # 创建一个新的空字典来存储提取的键值对
        extracted_dict = {}

        # 遍历要提取的键的列表
        for key in keys_to_extract:
            # 检查键是否在源字典中
            if key in source_dict:
                # 如果存在，将其添加到新字典中
                extracted_dict[key] = source_dict[key]

        return extracted_dict

def Byurldownload_file(url, local_filename):
    """
    通过给定的 URL 下载文件并保存到本地。

    :param url: str, 文件的下载 URL
    :param local_filename: str, 本地保存文件的路径和文件名
    """
    response = requestSession.get(url, stream=True)
    if response.status_code == 200:
        with open(local_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(f"文件已成功下载到 {local_filename}")
    else:
        print("下载失败，状态码:", response.status_code)

def find_diffs(dict_a, dict_b):
    """
    比较两个字典并返回它们之间的不同之处。

    :param dict_a: 第一个字典
    :param dict_b: 第二个字典
    :return: 一个字典，其中包含了两个输入字典中不同的键及其对应的值。
    """
    diffs = {}

    # 获取所有键的集合
    all_keys = set(dict_a.keys()) | set(dict_b.keys())

    # 遍历所有可能的键
    for key in all_keys:
        # 检查键在两个字典中的值是否相同
        if (key in dict_a and key not in dict_b) or (key in dict_b and key not in dict_a) or (dict_a.get(key) != dict_b.get(key)):


            value_a = dict_a.get(key)
            value_b = dict_b.get(key)

            # 如果不同，将键和值添加到结果字典中
            if value_a=='' and value_b =='':
                continue
            if value_a is None and value_b is None:
                continue

            diffs[key] = {'dict_a': value_a, 'dict_b': value_b}

    diffs=json.dumps(diffs)
    return diffs


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

def print_dict_by_key(dictionary):
    # 遍历字典的键
    for key in dictionary.keys():
        # 获取对应的值
        value = dictionary[key]
        # 打印键和值
        print(f"{key}: {value}")

import json


def triple_quote_string_to_dict(triple_quoted_string):
    """
    将包含最外层三引号的字符串转换为字典格式

    参数:
    triple_quoted_string (str): 包含最外层三引号的字符串

    返回:
    dict: 解析后的字典
    """
    # 去除最外层的三引号
    json_string = triple_quoted_string.strip("'''")


    # 将JSON字符串解析为字典
    try:
        # json_string=json_string.replace('"', '"') # 注意替换下
        # print(json_string)
        result_dict = json.loads(json_string)

    except json.JSONDecodeError as e:
        raise ValueError("Invalid JSON format") from e

    return result_dict


if __name__ == '__main__':
    import json

    dict_b = '''{
  "couponType": "FULLCUT",
  "imageUrl": null,
  "brandId": 6533,
  "name": "carlos-优惠券-会员等级6发放",
  "note": null,
  "labelIds": [
    52
  ],
  "productLimit": "ALL",
  "shopLimit": "ALL",
  "validTimeRule": {
    "timeEnum": "TODAY",
    "days": 100,
    "fixed": false
  },
  "useMoneyLimit": false,
  "addFeedFlag": false,
  "orderTypeLimit": [
    2
  ],
  "dayUseLimit": 11,
  "orderUseLimit": 11,
  "enablePayChannel": false,
  "remark": null,
  "cancelStatus": 0,
  "canTrans": false,
  "receiveInform": true,
  "pastDueInform": true,
  "shareFlag": true,
  "couponValue": 20,
  "payOrderAvailable": false,
  "availableTime": {
    "fullTime": true
  },
  "shopIds": [],
  "limitType": "SHOP",
  "productIds": [],
  "categoryIds": [],
  "transRule": {},
  "cancelNum": null,
  "brandCancelNum": null
}'''
    dict_a = '''{
  "templateId": 1686,
  "brandId": 6533,
  "name": "carlos-优惠券-会员等级6发放",
  "imageUrl": null,
  "shopId": null,
  "createUserId": 17,
  "updateUserId": 17,
  "createChannel": "MANAGE",
  "createUserInfo": {
    "userId": 17,
    "userType": "SUPER_ADMIN",
    "username": "string",
    "nickname": "super star",
    "mobile": "17855337260",
    "email": "[]",
    "parentId": 0,
    "avatar": null,
    "shopValid": null,
    "qrCode": "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=gQEq8DwAAAAAAAAAAS5odHRwOi8vd2VpeGluLnFxLmNvbS9xLzAyRDJjek1yZTFjemwxMDAwMHcwNzIAAgT0a09fAwQAAAAA",
    "coreDishAdvice": null,
    "authInvalidAlarmConfig": null,
    "cpcDeliveryAlarmConfig": null,
    "shopAbnormalAlarmConfig": null,
    "dishAbnormalAlarmConfig": null,
    "rateAlarmConfig": null,
    "shopAbnormalAlarmOneHourConfig": null,
    "activityAlarmConfig": null,
    "isOpen": true,
    "createTime": 1596269410000,
    "urls": null,
    "comboLimitConfig": null,
    "roleCode": null,
    "notice": null,
    "isSupplyUser": null,
    "supplyRoleInfos": null,
    "shFlag": true,
    "allBrandFlag": true
  },
  "updateUserInfo": {
    "userId": 17,
    "userType": "SUPER_ADMIN",
    "username": "string",
    "nickname": "super star",
    "mobile": "17855337260",
    "email": "[]",
    "parentId": 0,
    "avatar": null,
    "shopValid": null,
    "qrCode": "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=gQEq8DwAAAAAAAAAAS5odHRwOi8vd2VpeGluLnFxLmNvbS9xLzAyRDJjek1yZTFjemwxMDAwMHcwNzIAAgT0a09fAwQAAAAA",
    "coreDishAdvice": null,
    "authInvalidAlarmConfig": null,
    "cpcDeliveryAlarmConfig": null,
    "shopAbnormalAlarmConfig": null,
    "dishAbnormalAlarmConfig": null,
    "rateAlarmConfig": null,
    "shopAbnormalAlarmOneHourConfig": null,
    "activityAlarmConfig": null,
    "isOpen": true,
    "createTime": 1596269410000,
    "urls": null,
    "comboLimitConfig": null,
    "roleCode": null,
    "notice": null,
    "isSupplyUser": null,
    "supplyRoleInfos": null,
    "shFlag": true,
    "allBrandFlag": true
  },
  "productLimit": "ALL",
  "productIds": [],
  "orderTypeLimit": [
    2
  ],
  "limitType": "SHOP",
  "shopLimit": "ALL",
  "shopIds": [],
  "categoryIds": [],
  "couponType": "FULLCUT",
  "couponValue": 20,
  "discountValue": null,
  "useLimit": null,
  "validTimeRule": {
    "fixed": false,
    "startTime": null,
    "endTime": null,
    "timeEnum": "TODAY",
    "delay": null,
    "days": 100,
    "timeUnit": null
  },
  "availableTime": {
    "weeks": null,
    "times": null,
    "fullTime": true,
    "list": null,
    "months": null,
    "memberBirthDay": null
  },
  "remark": null,
  "canTrans": false,
  "transTitle": null,
  "transIcon": null,
  "transRule": {
    "transferNum": null,
    "createdCantUseFlag": null
  },
  "receiveInform": true,
  "pastDueInform": true,
  "couponUseLimit": null,
  "shopDtos": null,
  "categoryDtos": null,
  "productDtos": null,
  "useMoneyLimit": false,
  "cancelStatus": 0,
  "cancelType": null,
  "cancelNum": null,
  "productCalculateType": 0,
  "productDiscount": null,
  "note": null,
  "labelIds": [
    52
  ],
  "brandCancelType": null,
  "brandCancelNum": null,
  "addFeedFlag": false,
  "deliveryDiscountMethod": null,
  "deliveryDailyUseLimit": false,
  "deliveryDailyUseTimes": 0,
  "deliveryExclusionRule": null,
  "dayUseLimit": 11,
  "orderUseLimit": 11,
  "shareFlag": true,
  "enablePayChannels": null
}'''
    dict_a1 = triple_quote_string_to_dict(dict_a)
    dict_b1 = triple_quote_string_to_dict(dict_b)
    # dict_a1 = dict_a
    # dict_b1 = dict_b

    diffs = find_diffs(dict_a1, dict_b1)
    diffs2=find_diffs(dict_b1, dict_a1)
    print(diffs)
    print(diffs2)

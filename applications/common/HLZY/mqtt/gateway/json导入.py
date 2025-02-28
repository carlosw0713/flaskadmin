# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/12/26
Description: <Brief description of the file>
"""

with open(r'D:\pythonproject\HLZY\backend\mqtt\gateway\cloud.txt', mode='r', encoding='utf-8') as f:
    json_text=f.read()

    Serialnumber='HLGW1012236000464' #替换的文字

    json_text=json_text.replace('HLGW1012426003191',Serialnumber)

with open('cloud_test.json', mode='w', encoding='utf-8') as f:
    f.write(json_text)

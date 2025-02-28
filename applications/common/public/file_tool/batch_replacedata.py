#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/23 18:15
# @Author  : carlos
# @Email   : carlos.w.0713@outlook.com
# @File    : batch_replacedata.py
# @IDE     : PyCharm
# @REMARKS : 备注

import os
import re


def batch_replace_in_py_files(directory, old_string, new_string):
    """
    在指定目录下所有 .py 文件中批量替换字符串。

    参数:
    directory (str): 需要搜索的目录路径。
    old_string (str): 需要被替换的旧字符串。
    new_string (str): 替换后的新字符串。
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                print(f"修改文件: {file}")
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                    # print(file_content)
                # 使用正则表达式进行替换
                updated_content = re.sub(re.escape(old_string), new_string, file_content)

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
if __name__ == '__main__':


    # 使用示例
    directory = r'D:\pythonproject\pear-admin-flask-master\applications\common\HLZY'  # 替换为实际的目录路径
    old_string = "from applications.common.HLZY.IOT import *"
    # old_string = "requests.post('https://sss-stage.sh-internal.com/"
    new_string = "from applications.common.HLZY.IOT import *"



    batch_replace_in_py_files(directory, old_string, new_string)


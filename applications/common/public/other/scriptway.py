#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/12 09:38
# @Author  : carlos
# @Email   : carlos.w.0713@outlook.com
# @File    : scriptway.py
# @IDE     : PyCharm
# @REMARKS : 备注


class ScriptWay():

    def extract_dict_items(self,source_dict, keys_to_extract):
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
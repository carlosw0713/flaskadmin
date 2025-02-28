#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : carlos
# @Email   : carlos.w.0713@outlook.com
import os

import yaml

class YamlWay:
    """ 获取 yaml 文件中的数据 """

    def get_yaml_data(self,yaml_file) -> dict:
        """
        获取 yaml 中的数据
        :param: fileDir:
        :return:
        """
        # 判断文件是否存在
        if os.path.exists(yaml_file):
            data = open(yaml_file, 'r', encoding='utf-8')
            res = yaml.load(data, Loader=yaml.FullLoader)

        else:
            raise FileNotFoundError("文件路径不存在")
        return res

    def write_json_to_yaml(self,json_data, yaml_file):
        # 将JSON数据解析为Python字典或列表
        # data = json.loads(json_data)
        data = json_data

        # 打开YAML文件进行写入
        with open(yaml_file, 'w', encoding='utf-8') as f:
            # 使用yaml.safe_dump函数将数据写入YAML文件
            yaml.safe_dump(data, f, default_flow_style=False,allow_unicode=True)

if __name__ == '__main__':
    task = YamlWay()


    shiheng_path1= r"/Users/carlos/PycharmProjects/shiheng/settings/shiheng/attributeinfoyaml.yaml"
    print(task.get_yaml_data(file_dir=shiheng_path1))

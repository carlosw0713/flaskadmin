"""
-*- coding: utf-8 -*-

@Author : carlos
@Time : 2023/captchacode/13 captchacode:42
@file_tool : file_way.py
@talk : 干什么的？
"""
import os
import re
from typing import Text


from public.other.time_way import *
from settings.path import *

class FileWAY():

    def root_path(self):
        """ 获取 根路径 """
        current_path=os.path.abspath(__file__)
        path = self.root_dirname_number(current_path,3) #目前文件是根目录的三级目录路径
        return path

    def current_path(self):
        '''
        获取当前目录
        :return:
        '''
        current_path = os.path.abspath(__file__)
        return current_path

    def mkdir(self, path: str):
        """
        文件夹不存在就创建
        避免文件不存在时删除报错
        :param path:
        :return:
        """
        folder = os.path.exists(path)
        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)

            return path
        else:
            return False

    def get_all_files(self,file_path=None,file_type='.py',datatype='file') -> list:
        """
        获取文件路径
        :param file_path: 目录路径
        :param : 是否过滤文件为 yaml格式， True则过滤
        :return:
        """
        filenames = []
        # 获取所有文件下的子文件名称

        for root, dirs, files in os.walk(file_path):
            if datatype=='file':
                for file in files:
                    if file.endswith(f'{file_type}'):
                        file_path = os.path.join(root, file)
                        filenames.append(file_path)

            if datatype=='dir':
                return dirs
        return filenames

    def root_dirname_number(self,path, number: int):
        '''
        获取输入路径的第几级父路径
        :param path:
        :param number:
        :return:
        '''

        if number == 0:
            return path
        for i in range(number):
            path = os.path.dirname(path)

        return path

    def run_del_schedule(self,dir_list,history_day=6):
        '''
        删除日志 指定日期的 指定日志文件
        :param directory: 指定日志目录
        :param after_days: 指定删除天数
        :return:
        '''

        today = TimeWay().now_time_day()
        history_day = TimeWay().now_time_day(before=history_day)  #转换日期格式

        for directory in dir_list:

            for filename in os.listdir(directory):

                try:
                    file_date_str = filename.split('.')[0] # 需要正则提取
                    file_date_str = re.findall('\d.*',file_date_str)[0]
                    file_date_str=str(file_date_str).split('_')[0] # 日志文件精确度到天 %Y-%m-%d_%H-%M-%S --》 %Y-%m-%d
                except:
                    continue

                try:
                    if TimeWay().compare_time(time_a=history_day,time_b=file_date_str,format="%Y-%m-%d"): # 比较a,b两时间  a>b 返回ture
                        file_path = os.path.join(directory, filename)
                        if os.path.exists(file_path):
                            os.remove(file_path)
                            # INFO.logger.info(f"清除历史文件 :{file_path}")
                            print(f"删除日志文件 : {filename}")
                except Exception as e:

                    raise (f'删除日志文件失败，失败原因：{e}')

    import os

    def delete_files_in_directory(self,directory_path):
        '''
        删除指定目录下所有文件
        :param directory_path:
        :return:
        '''
        # 遍历目录下的所有文件
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)

            # 检查是否为文件
            if os.path.isfile(file_path):
                # 删除文件
                os.remove(file_path)

    def get_files_with_extension(self,directory_path, extension):
        # 存储文件名和路径
        files_info = {}

        # 遍历目录及其子目录下的所有文件
        for root, dirs, files in os.walk(directory_path):
            for filename in files:
                # 获取文件完整路径
                file_path = os.path.join(root, filename)

                # 检查文件后缀是否匹配
                if filename.endswith(extension):
                    filename=filename.split(f'{extension}')[0] # 去掉文件名后缀
                    # 添加文件名和路径到列表
                    files_info[filename]=file_path

        print(files_info)
        return files_info



if __name__ == '__main__':
    pass


    task=FileWAY()
    # for dir in list(task.get_all_files(file_path=rf"C:\Users\AIYONG\Desktop\UI-TEST\dpttrade_web_ui_test\pages",datatype='dir')):
    #     print(dir)

    print(task.get_all_files(file_path=task.root_path(),datatype='dir'))
    print(task.root_path())
    task.run_del_schedule(dir_list=[LOGS])

# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/12/16
Description: <用户信息相关>
"""

from applications.common.HLZY.IOT import *
class UserInfo():

    def __init__(self):
        self.cookies = EMS_INFO.get('cookies')
        self.headers = EMS_INFO.get('headers')
        self.uri = EMS_INFO.get('uri')

    def adminuserpermissioninfo(self):
        '''
        用户所有信息
        菜单
        权限
        角色
        个人信息
        :return:
        '''

        response = requestSession.get(f'{self.uri}/api/admin/user/permission-info', cookies=self.cookies,
                                      headers=self.headers)

        resp = response.json()
        curl = generate_curl_command(response)
        if resp.get('code') == 0:
            INFO.logger.info(f"用户所有信息成功")
            return resp
        else:
            ERROR.logger.error(f"用户所有信息失败，返回信息：{resp}")

    def getmenuchildreninfo(self,dictinfo,children):
        '''
        获取页面信息
        :return:
        '''

        if children:
            for child in children:
                dictinfo[child.get('name')]={
                    'path':child.get('path'),
                    'menuId':child.get('menuId')
                }
                # print(child.get('name'))
                self.getmenuchildreninfo(dictinfo,child.get('children'))
        # return dictinfo


    def usermenuinfo(self):
        '''
        用户菜单表获取
        :return:
        '''

        adminusermenuinfo=self.adminuserpermissioninfo().get('data').get('menus')

        usermenuinfodict={}

        for usermenuinfo in adminusermenuinfo:
            name=usermenuinfo.get('name')
            path=usermenuinfo.get('path')
            menuId=usermenuinfo.get('menuId')

            children=usermenuinfo.get('children')
            usermenuinfodict[name]={
                'path':path,
                'menuId':menuId
            }

            self.getmenuchildreninfo(usermenuinfodict,children)

        return usermenuinfodict

if __name__ == '__main__':
    task=UserInfo()
    print(task.usermenuinfo())








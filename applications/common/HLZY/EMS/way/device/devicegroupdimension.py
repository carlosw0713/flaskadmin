# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/11/28
Description: <Brief description of the file>
"""

from applications.common.HLZY.EMS.outway.device.devicegroupdimension import DeviceGroupDimension

class DeviceGroupDimensionWay(DeviceGroupDimension):

    def grouptreechildrennamelist(self,data,children):
        '''
        存储子维度信息
        :param groupinfo:
        :param children: 子维度中的
        :return:
        '''


        for itme in children:
            groupName=itme.get('groupName')
            childreninfo=itme.get('children')
            data.append(groupName)

            if childreninfo!=None:
                self.grouptreechildrennamelist(data,childreninfo)

        return data

    def grouptreechildrendevicelist(self,data,children,groupname):
        '''
        存储子维度 设备信息
        :param groupinfo:
        :param children: 子维度中的
        :return:
        '''

        devicelist=[]
        for itme in children:
            id=itme.get('id')
            code=itme.get('code')
            if int(id)<0:#设备的id为负数
                name=itme.get('name')
                devicelist.append(name)
            if code!="无":
                print(f'"{code}"',end=",")


        data[groupname]=devicelist


        for itme in children:
            groupName=itme.get('name')
            childreninfo=itme.get('children')

            if childreninfo!=None:
                self.grouptreechildrendevicelist(data,childreninfo,groupName)

        return data


    def deviceGroupDimenpage(self):
        '''
        获取指定维度下的所有分组信息
        :return:
        '''
        group1Name='上海'
        devicegrouptreeinfolist=self.grouptree(dimensionId=1).get('data')

        data=[]
        for devicegrouptreeinfo in devicegrouptreeinfolist:
            groupName=devicegrouptreeinfo['groupName']
            childreninfo=devicegrouptreeinfo['children']

            if groupName==group1Name:

                data=self.grouptreechildrennamelist(data,childreninfo)
                print(data)

                return data

    def groupDeviceTreedictinfo(self):
        '''
        获取每个组织树下的设备信息
        :return:
        '''

        group1Name='海澜智云'
        devicegrouptreeinfolist=self.groupDeviceTree(dimensionId=15).get('data')

        data={}
        for devicegrouptreeinfo in devicegrouptreeinfolist:
            groupname=devicegrouptreeinfo['name']
            code=devicegrouptreeinfo['code']
            childreninfo=devicegrouptreeinfo['children']

            if groupname==group1Name:

                data=self.grouptreechildrendevicelist(data,childreninfo,groupname)
                print(data)
                return data



if __name__ == '__main__':

    task=DeviceGroupDimensionWay()
    # task.deviceGroupDimenpage()
    task.groupDeviceTreedictinfo()


# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/11/11
Description: <Brief description of the file>
"""

from applications.common.HLZY import *

class Device():

    def __init__(self,auth_info):
        IOT_INFO=auth_info
        self.cookies = IOT_INFO.get('cookies')
        self.headers = IOT_INFO.get('headers')
        self.uri = IOT_INFO.get('uri')

    def iotdevicesubDevicePage(self,parentDeviceCode):
        '''
        获取网关子设备
        :return:
        '''

        params = {'size': '1000', 'current': '1', 'parentDeviceCode': parentDeviceCode, 'subDeviceCode': '',
                  'sortOrder': 'false', }
        response = requestSession.get(f'{self.uri}/api/iot/device/subDevicePage', params=params, cookies=self.cookies,
                                      headers=self.headers)

        resp = response.json()
        
        if resp.get('code') == 0:
            INFO.logger.info(f" 获取网关子设备成功，返回信息")
            return resp
        else:
            ERROR.logger.error(f"获取网关子设备失败，返回信息：{resp}")

    def iotdevicesave(self,json_data):
        '''
        iot产品添加设备
        :param json_data:
        :return:
        '''

        # json_data = {'productCode': '0naxVhZ7', 'deviceCode': 'device_1111_1', 'deviceName': '设备_1111_1', }
        response = requestSession.post(f'{self.uri}/api/iot/device/save', cookies=self.cookies, headers=self.headers,
                                       json=json_data)

        resp = response.json()
        
        result = resp.get('data')
        if resp.get('code') == 0:
            INFO.logger.info(f"iot产品添加设备成功，请求信息信息：{json_data}")
            return result
        else:
            ERROR.logger.error(f"iot产品添加设备失败，返回信息：{resp}")

    def deliotdevic(self,deviceCode):
        '''
        IOT产品删除设备
        :return:
        '''
        
        params = {
            'deviceCode': f'{deviceCode}'
        }

        response = requestSession.delete(f'{self.uri}/api/iot/device', params=params, cookies=self.cookies,
                                   headers=self.headers)

        resp = response.json()
        
        result = resp.get('data')
        if resp.get('code') == 0:
            INFO.logger.info(f"iot产品删除设备成功，请求信息信息：{deviceCode}")
            return result
        else:
            ERROR.logger.error(f"iot产品删除设备失败，返回信息：{resp}")

    def iotproductpublish(self,productCode):
        '''
        iot产品发布上线
        :return:
        '''
        params = {
            'productCode': f'{productCode}',
        }

        response = requestSession.post(f'{self.uri}/api/iot/product/publish', params=params,
                                 cookies=self.cookies, headers=self.headers)

        resp = response.json()
        
        result = resp.get('data')
        if resp.get('code') == 0:
            INFO.logger.info(f"产品{productCode}发布上线成功")
            return result
        else:
            ERROR.logger.error(f"产品{productCode}发布上线失败，返回信息：{resp}")

    def iotproductgenerateid(self):

        '''
        获取产品设备id
        :return:
        '''
        response = requestSession.get(f'{self.uri}/api/iot/product/generate/id', cookies=self.cookies,
                                headers=self.headers)

        resp = response.json()
        
        result = resp.get('data')
        if resp.get('code') == 0:
            INFO.logger.info(f"成功，返回信息")
            return result
        else:
            ERROR.logger.error(f"获取设备id失败，返回信息：{resp}")

    def iotproduct(self,json_data):
        '''
        产品创建
        :return:
        '''

        # json_data = {'deviceType': 1, 'productCode': '12312312', 'productName': 'cess',
        #              'protocolCode': 'HLSC_MQTT', 'remark': '111111111111111', }
        response = requestSession.post(f'{self.uri}/api/iot/product', cookies=self.cookies, headers=self.headers,
                                       json=json_data)

        resp = response.json()
        
        result = resp.get('data')
        if resp.get('code') == 0:
            INFO.logger.info(f"产品创建成功，返回信息")
            return result
        else:
            ERROR.logger.error(f"产品创建失败，返回信息：{resp}")

    def iotthingspage(self,productCode):
        '''
        产品物模型数据
        :return:
        '''
        params = {
            'size': '1000',
            'current': '1',
            'productCode': productCode,
        }

        response = requestSession.get(f'{self.uri}/api/iot/things/page', params=params, cookies=self.cookies,
                                headers=self.headers)

        resp = response.json()
        
        if resp.get('code') == 0:
            result = resp.get('data').get('records')  # 返回设备列表
            INFO.logger.info(f"产品物模型数据查询成功，返回信息")
            return result
        else:
            ERROR.logger.error(f"产品物模型数据查询失败，返回信息：{resp}")


    def iotthings(self,json_data):
        '''
        添加物模型
        :param json_data:
        :return:
        '''

        # json_data = {
        #     'specs': {
        #         'correct': False,
        #     },
        #     'modelType': 1,
        #     'rwType': 0,
        #     'identifier': 'a111',
        #     'modelName': '11',
        #     'dataType': 'float',
        #     'productCode': 'xiI8wkyc',
        # }

        response = requestSession.post(f'{self.uri}/api/iot/things', cookies=self.cookies,
                                 headers=self.headers, json=json_data)

    def iotproductpage(self):
        '''
        IOT产品列表
        :return:
        '''

        params = {'size': '100', 'current': '1', 'sortOrder': 'false', }
        response = requestSession.get(f'{self.uri}/api/iot/product/page', params=params, cookies=self.cookies,
                                      headers=self.headers)

        resp = response.json()
        
        if resp.get('code') == 0:
            INFO.logger.info(f"IOT产品列表查询成功，返回信息：{resp}")
            return resp
        else:
            ERROR.logger.error(f"IOT产品列表查询失败，返回信息：{resp}")

    def iotproductpublish(self,productCode):
        '''
        产品发布
        :param productCode:
        :return:
        '''

        params = {'productCode': f'{productCode}', }
        response = requestSession.post(f'{self.uri}/api/iot/product/publish', params=params, cookies=self.cookies,
                                      headers=self.headers)
        resp = response.json()
        
        if resp.get('code') == 0:
            INFO.logger.info(f" 产品发布成功，返回信息：{resp}")
            return resp
        else:
            ERROR.logger.error(f" 产品发布失败，返回信息：{resp}")

    def iotdevicepage(self,deviceCode=None,productCode=None):
        '''
        设备列表查询
        :return:
        '''

        params = {
            'size': '1000',
            'current': '1',
            'sortOrder': 'false',
        }
        if deviceCode:
            params['deviceCode'] = deviceCode

        if productCode:
            params['productCode'] = productCode

        response = requestSession.get(f'{self.uri}/api/iot/device/page', params=params, cookies=self.cookies,headers=self.headers)

        resp = response.json()
        

        if resp.get('code') == 0:
            INFO.logger.info(f"设备列表查询成功，返回信息")
            return resp
        else:
            ERROR.logger.error(f"设备列表查询失败，返回信息：{resp}")


    def run_addiotproduct(self):
        '''
        创建产品
        :return:
        '''
        productCode=self.iotproductgenerateid()
        productName='网关主设备100个'
        deviceType=2 #1.直连设备、2.网关设备、3.网关子设备
        protocolCode='HLSC_MQTT' #mqtt协议和opc协议
        json_data = {'deviceType': 2, 'productCode': f'{productCode}', 'productName': f'{productName}',
                     'protocolCode': protocolCode, 'remark': '111111111111111', }
        self.iotproduct(json_data)



    def run_readiotdeviceinfo(self):
        '''
        读取设备信息，保存至csv表中
        :return:
        '''

        spc_tag='YC'
        iotdevicepageinfolist = self.iotdevicepage(deviceCode='YC')
        # firest_row=['deviceCode0','deviceCode1','deviceCode2','deviceCode3','deviceCode4','deviceCode5','deviceCode6','deviceCode7']
        firest_row=['deviceCode','subdeviceCode']

        for iotdevicepageinfo in iotdevicepageinfolist:
            deviceCode = iotdevicepageinfo.get('deviceCode')


    def run_getiotthingspage_jmeterdata(self):
        '''
        获取物模型数据，并构建jemter脚本
        :return:
        '''

        productCode='0naxVhZ7'
        iotthingspageinfolist=self.iotthingspage(productCode)

        devicedetainfo={}
        pulish_data={
            "ver": "1.0",
            "msgId":" ${__time(,)}",
            "data": {
                "${subdeviceCode}": {
                    "LA_voltage": '${__Random(1,9,)}'
                }
            },
            "ts": '${__time(/1000,)}'
            }
        for iotthingspageinfo in iotthingspageinfolist:
            identifier=iotthingspageinfo.get('identifier')
            devicedetainfo[identifier]='${__Random(1,1000,)}'

        pulish_data["data"]["${subdeviceCode}"]=devicedetainfo
        pulish_data=json.dumps(pulish_data)
        print(pulish_data)


    def run_autobacthaddiotdevice(self):
        '''
        批量给产品添加设备
        1.获取子设备中的物模型
        2.根据网关id和物模型标识添加设备
        :return:
        '''
        productCode='0naxVhZ7' #设备ID
        mainproductCode='dev'

        productidentifierlist=[]
        iotthingspageinfolist=self.iotthingspage(productCode=productCode)
        for iotthingspageinfo in iotthingspageinfolist:
            identifier=iotthingspageinfo.get('identifier')
            if mainproductCode:
                productidentifier=f"{mainproductCode}_{identifier[:-2]}"
            else:
                productidentifier=f"{identifier[:-2]}" #xx_water_aa_2 去除_2
            productidentifierlist.append(productidentifier)

        for productidentifier in list(set(productidentifierlist)):
            json_data = {'productCode': f'{productCode}', 'deviceCode': f"{productidentifier}", 'deviceName': f'设备{productidentifier}', }
            self.iotdevicesave(json_data=json_data)


    def run_create_generate_payload_byiotdevice(self):
        '''
        根据iot设备，输出推送数据格式
        :return:
        '''

        productCode='8yRwLkiA'#产品ID
        maindeviceCode='dev_' #主网关id，后面加个_,直连设备就为“”
        identifiertype='all' # all:所有物模型，spc:特殊物模型

        iotdevicepageinfolist=self.iotdevicepage(productCode=productCode)

        pulish_data={
            "ver": "1.0",
            "msgId":" ${__time(,)}",
            "data": {
                "测试设备id": {
                    "LA_voltage": '1.22'
                }
            },
            "ts": '${__time(/1000,)}'
            }
        data_dict={}
        productidentifierlist = []
        iotthingspageinfolist = self.iotthingspage(productCode=productCode)
        for iotdevicepageinfo in iotdevicepageinfolist:
            iotdeviceCode=iotdevicepageinfo.get('deviceCode')

            iotthingsdict={}#物模型列表
            for iotthingspageinfo in iotthingspageinfolist:
                identifier = iotthingspageinfo.get('identifier')
                if identifiertype == 'all':  # 添加全部
                    iotthingsdict[identifier] = '10'
                    # iotthingsdict[identifier] = random.randint(1, 100)

                elif identifiertype=='spc':
                    # print(iotdeviceCode.replace(f'{maindeviceCode}',''))
                    if iotdeviceCode.replace(f'{maindeviceCode}','') in identifier: # 判断是否包含主设备标识
                        iotthingsdict[identifier] = '10'
                        # iotthingsdict[identifier] = random.randint(1, 100)

            data_dict[iotdeviceCode]=iotthingsdict

        pulish_data['data']=data_dict
        INFO.logger.info(f"打印推送数据\n{pulish_data}")






if __name__ == '__main__':
    task=Device()
    # task.run_addiotproduct()

    task.run_bacthaddiotdevice()

    # task.run_getiotthingspage()

    # task.run_create_generate_payload_byiotdevice()

    # task.iotdevicepage()

    # task.run_batchaddiotdevicesave()
    # task.run_bacthdeliotdevice()
    # task.iotproductpublish('6tigy2q0')
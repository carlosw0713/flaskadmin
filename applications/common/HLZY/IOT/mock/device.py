# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/12/6
Description: <Brief description of the file>
"""


from applications.common.HLZY.IOT import *
class Device:

    def __init__(self):
        self.cookies = IOT_INFO.get('cookies')
        self.headers = IOT_INFO.get('headers')
        self.uri = IOT_INFO.get('uri')

    def iotdevicepage(self):

        params = {    'size': '100',    'current': '1',    'productCode': '',    'sortOrder': 'false',}
        response = requestSession.get(f'{self.uri}/api/iot/device/page', params=params, cookies=self.cookies, headers=self.headers)

        resp=response.json()
        curl=generate_curl_command(response)
        if resp.get('code')==0:
            INFO.logger.info(f"成功，返回信息：{resp}")
            return resp
        else:
            ERROR.logger.error(f"失败，返回信息：{resp}")


    def mockmodelinfo(self):
        '''
        输出mockemodel数据
        :return:
        '''
        iotdevicepage=self.iotdevicepage().get('data').get('records')

        data={}
        for i in iotdevicepage:
            deviceCode=i.get('deviceCode')

            data[deviceCode]={'test_point':1}

        print(data)


if __name__ == '__main__':
    Device().mockmodelinfo()



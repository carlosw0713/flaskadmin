# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/11/11
Description: <Brief description of the file>
"""
import threading
from ctypes.wintypes import PUSHORT

import paho.mqtt.client as mqtt
import json
import random
import time
import uuid

from public.other.time_way import TimeWay
from applications.common.HLZY.IOT import *

class Push_Mqtt():

    def __init__(self):

        mqtt_clientIdStr = "dev" # 网关ID
        self.mqtt_clientIdStr=mqtt_clientIdStr
        # MQTT 服务器参数
        mqtt_broker = "10.1.1.140" #服务地址
        mqtt_port = 1883 #端口
        mqtt_keepalive = 600
        self.mqtt_topic = f"/gateway/{mqtt_clientIdStr}/report/data"

        # 用户验证信息

        mqtt_username = f"{mqtt_clientIdStr}@hlsc"
        mqtt_password = f"{mqtt_clientIdStr}&hlsc"
        mqtt_clientid = f"{mqtt_clientIdStr}"

        # 创建 MQTT 客户端实例
        self.client = mqtt.Client(client_id=mqtt_clientid)
        self.client.username_pw_set(username=mqtt_username, password=mqtt_password)

        # 注册回调函数
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish

        # 连接到 MQTT Broker
        self.client.connect(mqtt_broker, mqtt_port, mqtt_keepalive)


    # MQTT 客户端回调函数
    def on_connect(self,client, userdata, flags, rc):
        if rc == 0:
            print("Successfully connected to MQTT Broker.")
            client.subscribe(self.mqtt_topic)  # 如果需要订阅，可以在这里添加订阅
        else:
            print(f"Failed to connect, return code {rc}")

    # 推送消息中
    def on_publish(self,client, userdata, mid):
        print(f"消息推送中：, mid: {mid}")


    def generate_payloaddata(self,data,datatype):
        '''
        设置推送数据类型
        将推送中的数据设备不同内容如何返回
        :param datatype:为None 不动直接返回，为0则随机，其余为固定值
        :return:
        '''

        if datatype==None:
            return data

        datadict = data.get('data')
        # rd_value= random.randint(10, 99)
        rd_value= 0
        for key, value in datadict.items():
            for key2, value2 in value.items():
                if datatype==0:
                    value2 = random.randint(30, 99)+rd_value
                    # value2 = 550
                    datadict[key][key2] = value2
                else:
                    value2 = datatype
                    datadict[key][key2] = value2
        data['data']=datadict
        return data


    # 动态生成 payload
    def generate_payload(self,ts):
        '''
        推送数据
        :param parameter:
        :return:
        '''

        msg_id = str(uuid.uuid4())  # 使用 UUID 作为 msgId
        datatype=0

        # data={'ver': '1.0', 'msgId': ' ${__time(,)}', 'data': {'dev_all_ele_aa': {'AB_LV': 90, 'BC_LV': 18, 'CA_LV': 16, 'Cos': 66, 'L10__I': 29, 'L1A_Cos': 2, 'L1A_I': 45, 'L1A_Naee': 97, 'L1A_P': 11, 'L1A_Paee': 61, 'L1A_Pree': 71, 'L1A_Q': 52, 'L1A_S': 29, 'L1A_WQN': 41, 'L1B_Cos': 26, 'L1B_I': 50, 'L1B_Naee': 13, 'L1B_P': 28, 'L1B_Paee': 10, 'L1B_Pree': 9, 'L1B_Q': 11, 'L1B_S': 25, 'L1B_WQN': 26, 'L1C_Cos': 57, 'L1C_I': 63, 'L1C_Naee': 41, 'L1C_P': 40, 'L1C_Paee': 98, 'L1C_Pree': 9, 'L1C_Q': 69, 'L1C_S': 3, 'L1C_WQN': 72, 'L1T_Cos': 3, 'L1T_Naee': 52, 'L1T_P': 79, 'L1T_Paee': 100, 'L1T_Pree': 71, 'L1T_Q': 88, 'L1T_S': 52, 'L1T_WQN': 47, 'L2A_Cos': 54, 'L2A_I': 79, 'L2A_Naee': 29, 'L2A_Nree': 52, 'L2A_P': 5, 'L2A_Paee': 19, 'L2A_Pree': 68, 'L2A_Q': 42, 'L2A_S': 97, 'L2B_Cos': 59, 'L2B_I': 27, 'L2B_Naee': 48, 'L2B_Nree': 76, 'L2B_P': 79, 'L2B_Paee': 8, 'L2B_Pree': 2, 'L2B_Q': 45, 'L2B_S': 6, 'L2C_Cos': 12, 'L2C_I': 23, 'L2C_Naee': 29, 'L2C_Nree': 77, 'L2C_P': 30, 'L2C_Paee': 54, 'L2C_Pree': 20, 'L2C_Q': 26, 'L2C_S': 55, 'L2_Cos': 97, 'L2_Naee': 44, 'L2_Nree': 23, 'L2_P': 48, 'L2_Paee': 97, 'L2_Pree': 81, 'L2_Q': 29, 'L2_S': 89, 'L30_I': 95, 'L3A_Cos': 22, 'L3A_I': 89, 'L3A_P': 17, 'L3A_Paee': 14, 'L3A_Q': 80, 'L3A_S': 59, 'L3B_Cos': 13, 'L3B_I': 23, 'L3B_P': 70, 'L3B_Paee': 34, 'L3B_Q': 54, 'L3B_S': 43, 'L3C_Cos': 58, 'L3C_I': 15, 'L3C_P': 43, 'L3C_Q': 67, 'L3C_S': 39, 'L3_Cos': 59, 'L3_P': 5, 'L3_Q': 52, 'L3_S': 24, 'LA_voltage': 75, 'LB_voltage': 50, 'LC_voltage': 40}}, 'ts': '${__time(/1000,)}'}
        # data={'ver': '1.0', 'msgId': ' ${__time(,)}', 'data': {'dev_xx_gas_aa': {'xx_gas_aa_1': '10', 'xx_gas_aa_2': '10'}, 'dev_xx_water_aa': {'xx_water_aa_1': '10', 'xx_water_aa_2': '10'}, 'dev_xx_ele_aa': {'xx_ele_aa_1': '10', 'xx_ele_aa_2': '10'}}, 'ts': '${__time(/1000,)}'}
        data={'ver': '1.0', 'msgId': ' ${__time(,)}', 'data': {'dev_gas_aa': {'gas_aa_1': '10', 'gas_aa_2': '10'}, 'dev_water_aa': {'water_aa_1': '10', 'water_aa_2': '10'}, 'dev_ele_aa': {'ele_aa_1': '10', 'ele_aa_2': '10'}}, 'ts': '${__time(/1000,)}'}
        # data={'ver': '1.0', 'msgId': ' ${__time(,)}', 'data': {'dev_all_ele_aa': {'L1A_Paee': '11', 'L1A_Pree': '11', 'L1A_WQN': '11', 'L1B_Naee': '11'}}, 'ts': '${__time(/1000,)}'}
        # data={'ver': '1.0', 'msgId': ' ${__time(,)}', 'data': {'dev_all_ele_aa': {'L1B_Paee': '11', 'L1B_Pree': '11', 'L2C_Paee': '11'}}, 'ts': '${__time(/1000,)}'}
        data={'ver': '1.0', 'msgId': ' ${__time(,)}', 'data': {'dev_gas_bb': {'gas_aa_1': '10', 'gas_aa_2': '10'}, 'dev_water_bb': {'water_aa_1': '10', 'water_aa_2': '10'}, 'dev_ele_bb': {'ele_aa_1': '10', 'ele_aa_2': '10'}}, 'ts': '${__time(/1000,)}'}
        # data={'ver': '1.0', 'msgId': ' ${__time(,)}', 'data': {'dev_all_ele_aa': {'L1A_Cos': '11', 'L1A_I': '11', 'L1A_P': '11', 'L1B_I': '11', 'L1C_I': '11', 'L2A_Cos': '11', 'L2A_I': '11', 'L2A_P': '11', 'L2B_I': '11', 'L2C_I': '11', 'L3A_Cos': '11', 'L3A_I': '11', 'L3A_P': '11', 'L3B_I': '11', 'L3C_I': '11', 'LA_voltage': '11', 'LB_voltage': '11', 'LC_voltage': '11'}}, 'ts': '${__time(/1000,)}'}
        # data = {'ver': '1.0', 'msgId': ' ${__time(,)}', 'data': {'dev_all_ele_aa': {'L1A_Paee': '11', 'L1A_Pree': '11', 'L1A_WQN': '11', 'L1B_Naee': '11'}}, 'ts': '${__time(/1000,)}'}
        # data={'ver': '1.0', 'msgId': ' ${__time(,)}', 'data': {'dev_ele_bb': {'elefee': '10', }}, 'ts': '${__time(/1000,)'}


        data=self.generate_payloaddata(data,datatype)
        data['ts'] = ts
        data['msgId'] = msg_id

        return json.dumps(data)

    # 发布消息
    def publish_message(self):
        '''
        消息推送
        :return:
        '''
        publishcount=1#推送次数

        for i in range(publishcount):

            tslist = TimeWay().generate_date_or_timestamp_list(
                start_time_str="2024-10-21 00:00:00", end_time_str="2024-11-25 17:10:00",
                time_unit=60*15*1,output_format="timestamp",if_nowtime=False) #获取时间列表 时间戳格式
            print(f'执行时间范围次数{len(tslist)}')

            for ts in tslist:
                time.sleep(0.02)

                payload = self.generate_payload(ts=ts) #
                result = self.client.publish(self.mqtt_topic, payload, qos=1)  # 发布消息，qos=1表示消息至少送达一次
                if result.rc == mqtt.MQTT_ERR_SUCCESS:
                    INFO.logger.info(f"推送消息成功: {payload}")
                else:
                    ERROR.logger.error(f"推送消息失败: {result.rc}")

    def publish_message_threaded2(self, ts):
        '''
        消息推送
        :param ts: 时间戳
        :return:
        '''
        payload = self.generate_payload(ts=ts)
        result = self.client.publish(self.mqtt_topic, payload, qos=1)  # 发布消息，qos=1表示消息至少送达一次
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            INFO.logger.info(f"推送消息成功: {payload}")
        else:
            ERROR.logger.error(f"推送消息失败: {result.rc}")

    def publish_message_threaded1(self):
        '''
        多线程消息推送
        :return:
        '''
        publishcount = 1  # 推送次数

        for i in range(publishcount):

            tslist = TimeWay().generate_date_or_timestamp_list(
                start_time_str="2024-10-01 00:01:00", end_time_str="2024-10-02 13:10:00",
                time_unit=60 * 15*4*24 , output_format="timestamp", if_nowtime=False)  # 获取时间列表 时间戳格式
            print(f'执行时间范围次数 {len(tslist)}')


            threads = []
            for ts in tslist:
                thread = threading.Thread(target=self.publish_message_threaded2, args=(ts,))
                threads.append(thread)
                thread.start()
                time.sleep(0.02)  # 适当延时，避免线程创建过快

            # 等待所有线程完成
            for thread in threads:
                thread.join()

    # 运行 MQTT 客户端，发布消息
    def run_publish_message(self):
        self.client.loop_start()  # 启动客户端的网络循环

        # self.publish_message()
        self.publish_message_threaded1()


# 启动脚本
if __name__ == "__main__":

    task=Push_Mqtt()

    task.run_publish_message()

    # print(int(time.time()))




# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/12/4
Description: <Brief description of the file>
"""

import threading
from ctypes.wintypes import PUSHORT
from datetime import datetime

import paho.mqtt.client as mqtt
import json
import random
import time
import uuid

from public.logging_tool.log_control import *
from public.other.time_way import TimeWay


class Push_Mqtt():

    def __init__(self):

        mqtt_clientIdStr = "dev" # 网关ID
        # mqtt_clientIdStr = "dev" # 网关ID
        self.mqtt_clientIdStr=mqtt_clientIdStr
        # MQTT 服务器参数
        # mqtt_broker = "10.1.1.140" #服务地址
        mqtt_broker = "10.1.1.144" #服务地址
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

    #MQTT 客户端回调函数
    def on_connect(self,client, userdata, flags, rc):
        if rc == 0:
            print("Successfully connected to MQTT Broker.")
            client.subscribe(self.mqtt_topic)  # 如果需要订阅，可以在这里添加订阅
        else:
            print(f"Failed to connect, return code {rc}")
    # 推送消息中
    def on_publish(self,client, userdata, mid):
        print(f"消息推送中：, mid: {mid}")


    def publish_message_by_date(self):
        '''
        按日期推送数据
        :return:
        '''

        publishcount = 1  # 推送次数
        for i in range(publishcount):

            tslist = TimeWay().generate_date_or_timestamp_list(
                start_time_str="2024-10-01 00:01:00", end_time_str="2024-10-02 13:10:00",
                time_unit=60 * 15*4*24 , output_format="timestamp", if_nowtime=False)  # 获取时间列表 时间戳格式
            print(f'执行时间范围次数 {len(tslist)}')

        return tslist


    def publish_message(self, payload):
        '''
        推送信息
        :return:
        '''

        result = self.client.publish(self.mqtt_topic, payload, qos=1)  # 发布消息，qos=1表示消息至少送达一次
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            INFO.logger.info(f"推送消息成功: {payload}")
        else :
            ERROR.logger.error(f"推送消息失败: {result.rc}")

    def run_publish_message(self):
        '''
        执行消息推送
        :return:
        '''
        self.client.loop_start()  # 启动客户端的网络循环

        # 获取基本推送模板
        self.generate_values()

    def generate_values(self):
        '''
        获取推送数据信息和进行推动
        :param ts_list:
        :return:
        '''

        # 初始化当前值为起始值
        Initial_value = 1000
        calculate_range=[0.1,0.5]
        # Initial_value = 110
        # calculate_range=[50,120]

        # 判断计算类型
        calculate_type='random'
        # 输入int则暑促整数其他则输出浮点数
        value_type='int'
        value_type='float'

        ts_list = TimeWay().generate_date_or_timestamp_list(
            start_time_str="2025-02-08 00:00:12", end_time_str="2025-02-08 23:55:00",
            time_unit=60 * 15 , output_format="timestamp", if_nowtime=False)  # 获取时间列表 时间戳格式

        input(f'请确认下你要造的数据计算类型 {calculate_type} 和起始值 {Initial_value}\n')

        # 数据模板
        data={'ver': '1.0', 'msgId': ' ${__time(,)}', 'data': {'dev_gas_bb': {'gas_aa_1': '10', 'gas_aa_2': '10'}, 'dev_water_bb': {'water_aa_1': '10', 'water_aa_2': '10'}, 'dev_ele_bb': {'ele_aa_1': '10', 'ele_aa_2': '10'}}, 'ts': '${__time(/1000,)}'}

        data_dict = {'dev_shq_el': {'EL_dosage': '11'}, 'dev_bgl_el': {'EL_dosage': '11'}, 'dev_bc8dddj': {'EL_dosage': '11'}, 'dev_qd102_el': {'EL_dosage': '11'}, 'dev_qd101_el': {'EL_dosage': '11'},
                     'dev_ysq_wt': {'WT_dosage': '11'}, 'dev_jx': {'WT_dosage': '11'}, 'dev_st_wt': {'WT_dosage': '11'}, 'dev_gsbgl_wt': {'WT_dosage': '11'}, 'dev_zjcgsshys_wt': {'WT_dosage': '11'},
                     'dev_qtglzz_gas': {'GAS_dosage': '11'}, 'dev_qtjcy_gas': {'GAS_dosage': '11'}}

        data_dict={'dev_shq_el': {'ELA_current_Xzjbl': '11', 'ELA_voltage_Xzjbl': '11', 'ELB_current_Xzjbl': '11', 'ELB_voltage_Xzjbl': '11', 'ELC_current_Xzjbl': '11', 'ELC_voltage_Xzjbl': '11'}, 'dev_bgl_el': {'ELA_current_Xzjbl': '11', 'ELA_voltage_Xzjbl': '11', 'ELB_current_Xzjbl': '11', 'ELB_voltage_Xzjbl': '11', 'ELC_current_Xzjbl': '11', 'ELC_voltage_Xzjbl': '11'}, 'dev_bc8dddj': {'ELA_current_Xzjbl': '11', 'ELA_voltage_Xzjbl': '11', 'ELB_current_Xzjbl': '11', 'ELB_voltage_Xzjbl': '11', 'ELC_current_Xzjbl': '11', 'ELC_voltage_Xzjbl': '11'}, 'dev_qd102_el': {'ELA_current_Xzjbl': '11', 'ELA_voltage_Xzjbl': '11', 'ELB_current_Xzjbl': '11', 'ELB_voltage_Xzjbl': '11', 'ELC_current_Xzjbl': '11', 'ELC_voltage_Xzjbl': '11'}, 'dev_qd101_el': {'ELA_current_Xzjbl': '11', 'ELA_voltage_Xzjbl': '11', 'ELB_current_Xzjbl': '11', 'ELB_voltage_Xzjbl': '11', 'ELC_current_Xzjbl': '11', 'ELC_voltage_Xzjbl': '11'}}

        data_dict={'dev_ele_a':{'test_point':1}}

        threads = []
        for ts in ts_list:
            msg_id = str(uuid.uuid4())

            # 内层循环：遍历字典，更新每个键的值
            for key, sub_dict in data_dict.items():
                for sub_key, value in sub_dict.items():

                    if calculate_type=='add' or calculate_type=='random': # 随机值 or递增数据
                        # 生成新的随机值，保证新值大于前一个值
                        new_value = round(random.uniform(Initial_value + calculate_range[0], Initial_value + calculate_range[1]),2)  # 随机值大于 Initial_value
                    elif calculate_type=='sub':
                        # 生成新的随机值，保证新值小于前一个值
                        new_value = round(random.uniform(Initial_value - calculate_range[0], Initial_value - calculate_range[1]),2)
                    elif calculate_type=='zation':
                        new_value = Initial_value
                    else:
                        ERROR.logger.error(f'不支持的计算类型:{calculate_type}')

                    # 更新字典
                    sub_dict[sub_key] = new_value
                    # 判断输出是否为整数
                    if value_type=='int':
                        sub_dict[sub_key] = int(new_value)

                # 更新 Initial_value，作为下一次迭代的基准
                if calculate_type=='add':
                    max_value=max(sub_dict.values())
                    Initial_value = max_value
                elif calculate_type=='sub':
                    min_value=min(sub_dict.values())
                    Initial_value = min_value
                else:
                    # ERROR.logger.error(f'不支持的计算类型:{calculate_type}')
                    pass

            data={
                'ver': '1.0',
            }
            data['msgId']=msg_id
            data['ts']=ts
            data['data']=data_dict


            # continue
            time.sleep(0.05)  # 适当延时，避免线程创建过快
            #执行推送
            self.publish_message(payload=json.dumps(data))
            continue

            # 多线程推送 暂时不用好像更慢
            thread = threading.Thread(target=self.publish_message, args=(json.dumps(data),))
            threads.append(thread)
            thread.start()


        # 等待所有线程完成
        for thread in threads:
            thread.join()

        INFO.logger.info(f'预计执行时间范围次数 {len(ts_list)},最终估值：{new_value}')






if __name__ == '__main__':
    task=Push_Mqtt()
    task.run_publish_message()

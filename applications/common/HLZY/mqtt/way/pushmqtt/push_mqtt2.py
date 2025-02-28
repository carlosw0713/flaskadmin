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

        mqtt_clientIdStr = "mock" # 网关ID
        # mqtt_clientIdStr = "dev" # 网关ID
        self.mqtt_clientIdStr=mqtt_clientIdStr
        # MQTT 服务器参数
        mqtt_broker = "222.71.114.10" #服务地址
        # mqtt_broker = "10.1.1.144" #服务地址
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

        calculate_type = 'random'
        value_type = 'float'
        # 初始化初始值
        current_value =100

        # 阈值 用于 随机值
        threshold=50

        # 计算时间间隔
        time_interval = 30*1*1
        # 计算总的时间段数
        total_intervals = int(24 * 60 / time_interval)

        # 生成时间列表
        start_time_str = "2025-02-17 00:00:00"
        end_time_str = "2025-02-17 23:59:59"

        ts_list = TimeWay().generate_date_or_timestamp_list(
            start_time_str=start_time_str, end_time_str=end_time_str,
            time_unit=time_interval * 60, output_format="timestamp", if_nowtime=False
        )  # time_unit 暂时是按秒来记得所以需要除以60


        data_dict = {'mock_gas_A':{'test_point':12},'mock_gas_B':{'test_point':12}
            ,'mock_water_A':{'test_point':12},'mock_water_B':{'test_point':12},
            'mock_ele_A':{'test_point':12},'mock_ele_B':{'test_point':12}}



        input( f'请确认下你要造的数据内容'
               f'网关ID：{self.mqtt_clientIdStr}\n'
               f'计算类型 {calculate_type} 和起始值 {current_value},时间范围为 {start_time_str} 到 {end_time_str}'
               f'\nmock公式{data_dict}')

        daycount=1000 #随便定义一个值需要大于当天最大值
        for ts in ts_list:
            msg_id = str(uuid.uuid4())

            # 每隔一天循环时段增量
            if  daycount>=total_intervals:

                # 当天最大值减去最小值的固定值
                fixed_difference = random.randint(500,2000)
                # 计算每个时间段增量值 随机
                value_increment = fixed_difference / total_intervals / len(data_dict.keys())

                # 固定
                value_increment = 50 #随机值 时使用
                # print(f'当天更新时间{ts},记录值{data_dict}')
                daycount=0
            daycount+=1


            threads=[]
            # 内层循环：遍历字典，更新每个键的值
            for key, sub_dict in data_dict.items():
                for sub_key, value in sub_dict.items():
                    if calculate_type == 'add' :   # 随机值 or 递增数据
                        # 生成新的随机值，保证新值在当前时间段的范围内
                        new_value = round(random.uniform(current_value, current_value + value_increment), 2)
                    elif calculate_type == 'random':
                        new_value = round(random.uniform(current_value, current_value + value_increment), 2)
                        # 确保变化值的绝对值不超过阈值 X
                        value=int(value)
                        if abs(new_value - value) > threshold:
                            if new_value > value:
                                new_value = value + threshold
                            else:
                                new_value = value - threshold

                    elif calculate_type == 'sub':
                        # 生成新的随机值，保证新值在当前时间段的范围内
                        new_value = round(random.uniform(current_value - value_increment, current_value), 2)
                    elif calculate_type == 'zation':
                        new_value = current_value
                    else:
                        raise ValueError(f'不支持的计算类型: {calculate_type}')

                    # 更新字典
                    sub_dict[sub_key] = new_value
                    # 判断输出是否为整数
                    if value_type == 'int':
                        sub_dict[sub_key] = int(new_value)

                # 更新 current_value，作为下一次迭代的基准
                if calculate_type == 'add':
                    current_value += value_increment
                elif calculate_type == 'sub':
                    current_value -= value_increment
                else:
                    pass

            # print(f'当前时间：{ts},当前值：{new_value}')
            # continue

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



    def run_publish_onemessage(self):
        '''
        推送单条数据
        :return:
        '''

        self.client.loop_start()

        data_dict = {'mock_ele_a': {'test_point': 10}}
        # 定义日期时间格式
        date_format = "%Y-%m-%d %H:%M:%S"
        # 使用 strptime 方法解析字符串为 datetime 对象
        ts = datetime.strptime('2025-02-05 04:45:00', date_format)
        # 将 datetime 对象转换为时间戳
        ts = str(int(ts.timestamp())*1000)
        msg_id = str(uuid.uuid4())

        data = {
            'ver': '1.0',
        }
        data['msgId'] = msg_id
        data['ts'] = ts
        data['data'] = data_dict

        self.publish_message(payload=json.dumps(data))


if __name__ == '__main__':
    task=Push_Mqtt()
    task.run_publish_message()
    # task.run_publish_onemessage()

# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2025/2/8
Description: <网关数据监听>
"""
import time
from datetime import datetime, timedelta



from applications.common.HLZY.IOT.outway.device.communicationlog import Communicationlog
from applications.common.HLZY.IOT.outway.device.device import Device
from applications.common.public.notify.dingtalk import DingTalkSendMsg
from applications.common.HLZY import *



bp = Blueprint('iotdevicealarm', __name__, url_prefix='/iotdevicealarm')




class GatewayDataAlarm(Communicationlog,Device):

    def __init__(self,auth_info):
        IOT_INFO=auth_info

        self.cookies = IOT_INFO.get('cookies')
        self.headers = IOT_INFO.get('headers')
        self.uri = IOT_INFO.get('uri')

    def get_time_range_in_milliseconds(self,count,timestamptype=1):
        """
        获取从当前时间往前推 count 分钟到当前时间的时间戳范围（毫秒级）。
        参数:
            count (int): 往前推的分钟数。
            timestamptype : 时间戳类型，返回秒级还是毫秒级
        返回:
            tuple: 一个包含起始时间和结束时间（毫秒级时间戳）的元组。
        """
        # 获取当前UTC时间
        now = datetime.now()
        # 计算起始时间
        start_time = now - timedelta(seconds=int(count))

        # 转换为毫秒级时间戳
        start_timestamp_ms = int(start_time.timestamp() * timestamptype)
        end_timestamp_ms = int(now.timestamp() * timestamptype)

        return start_timestamp_ms, end_timestamp_ms


    def devicetimetyperule(self,deviceCode,devicetimetype):
        '''
        根据设备时间规则，返回通信日志查询入参
        :return:
        '''

        for fuzzy_deviceCode, timedifference in devicetimetype.items():

            if fuzzy_deviceCode in deviceCode:

                startTime,endTime=self.get_time_range_in_milliseconds(count=timedifference,timestamptype=1000)

                json_data = {
                    'size': '1000', 'current': '1', 'deviceCode': deviceCode,
                    'startTime': startTime, 'endTime': endTime,
                }

                return json_data

        WARNING.logger.warning(f"设备：{deviceCode} 不在配置警告范围内：{devicetimetype}")

    def alarmdeviceinfo(self,alarminfo):
        '''
        获取告警信息,根据设备编号获取告警信息，
        判断规定时间内期望上报设备信息和实际上报设备信息是否一致。
        网关设备需要获取网关子设备信息
        直连设备信息不需要
        返回
        :return:
        '''


        # alarminfo={
        #     'devicetimetype': {'sn': 1 * 60,'dev': 60 * 60*24*2, 'NO': 60 *60*18} ,
        #     'userinfo':f'https://iot-cluster-dev.heilansc.cn/（用户信息、用户token、域名）',
        #     'alarmdeviceinfolist':[],
        #     'nowtime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        # }


        iotdevicepage=self.iotdevicepage().get('data').get('records')

        for iotdeviceinfo in iotdevicepage:
            deviceCode=iotdeviceinfo.get('deviceCode')
            deviceType=iotdeviceinfo.get('deviceType')

            # 只需要网关设备的直连设备，如果为网关子设备，跳过
            if deviceType not in [1,2]:
                continue

            json_data=self.devicetimetyperule(deviceCode=deviceCode,devicetimetype=alarminfo.get('devicetimetype')) # 获取告警时间
            if json_data is None:
                continue

            # ---告警规则模型---

            # 获取通信日志
            iotdevicelogPage=self.iotdevicelogPage(params=json_data).get('data').get('records')

            if len(iotdevicelogPage)==0:
                ERROR.logger.error(f'在规定时间段中，网关/直连设备{deviceCode} 没有通信日志信息')

                alarmdeviceinfo = {
                    'deviceCode': deviceCode,
                    'alarminfo': f'在规定时间段中，没有通信日志信息',
                }

                # 添加报错信息
                alarminfo['alarmdeviceinfolist'].append(alarmdeviceinfo)

                continue

            # 判断网关中的子设备信息，上报数据情况
            for iotdevicelog in iotdevicelogPage:

                logtype=iotdevicelog.get('type') # 告警类型 设备上线 1 数据上报 3
                if logtype==3:

                    logdevicedata=iotdevicelog.get('content').get('data')
                    logdevicCodelist=list(logdevicedata.keys())
                    logtimestamp=iotdevicelog.get('content').get('ts')
                    logdatetime=iotdevicelog.get('time')
                    # 判断上报的数据是否有包含该设备

                    # 获取总上报设备信息，网关设备/直连设备
                    if deviceType == 1:
                        subdeviceCodelist=[deviceCode]
                    else :
                        subdeviceCodeinfo=self.iotdevicesubDevicePage(parentDeviceCode=deviceCode).get('data').get('records')
                        subdeviceCodelist= [i.get('deviceCode') for i in subdeviceCodeinfo]

                   # 判断上报的设备信息是否包含期望上报设备
                    for subdeviceCode in subdeviceCodelist:
                        if subdeviceCode not in logdevicCodelist:
                            ERROR.logger.error(f'数据上报时间:{logdatetime}，期望上报设备{subdeviceCodelist}，实际上报设备{logdevicCodelist}')

                            alarmdeviceinfo={
                                'deviceCode':deviceCode,
                                'alarminfo':f'数据上报时间:{logdatetime}, 期望上报设备{subdeviceCodelist}，实际上报设备{logdevicCodelist}',
                            }

                            # 添加报错信息
                            alarminfo['alarmdeviceinfolist'].append(alarmdeviceinfo)

                            #结束判断通信设备是否存在的循环
                            break

                    # 结束查询通信日志的循环
                    break


        # 钉钉推送告警信息!!!!!
        if len(alarminfo.get('alarmdeviceinfolist'))>0:

            noticetext=self.alarmnoticemodel(alarminfo=alarminfo)
            return noticetext
        else:
            return None



    def alarmnoticemodel(self,alarminfo):
        '''
        钉钉消息通知模板
        :return:
        '''


        alarmdeviceinfotext=""
        for alarmdeviceinfo in alarminfo.get('alarmdeviceinfolist'):

            alarmdeviceinfotext+=f"{alarmdeviceinfo}\n"

        noticetext=(f"### 【IOT告警信息】\n"
                    f"### 当前时间{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    f"#### 用户信息:\n"
                    f"{alarminfo.get('userinfo')}\n"
                    f"#### 监控规则:\n"
                    f"{alarminfo.get('devicetimetype')}\n"
                    f"#### 告警信息:\n"
                    f"{alarmdeviceinfotext}")


        return noticetext




def iotdevicedataalarm(**kwargs):
    '''
    IOT数据告警
    :param auth_info: 用户验证信息
    :param json_data: 告警配置信息
    :return:
    '''

    auth_info=kwargs.get('auth_info')
    json_data=kwargs.get('input_params')
    notice_info=kwargs.get('notification_config')

    auth_info = loginmodel(logininfo=auth_info)
    task=GatewayDataAlarm(auth_info=auth_info)
    noticetext=task.alarmdeviceinfo(alarminfo=json_data)

    if noticetext:

        DingTalkSendMsg(notice_info=notice_info).send_ding_notification(noticetext=noticetext)


@bp.post('/')
def runtask():
    '''
    路由形式运行
    需要分布式运行避免接口超时
    '''
    from flask import  request
    from concurrent.futures import ThreadPoolExecutor


    rejson_data=request.get_json()

    # auth_info=re.get('auth_info')
    # alarminfo=re.get('alarminfo')


    executor = ThreadPoolExecutor(max_workers=5)
    executor.submit(iotdevicedataalarm,**rejson_data)

    # 立即返回任务ID给客户端
    return {"message": "任务已启动，无需等待结果"}, 202


if __name__ == '__main__':
    # runtask()

    pass
    # 方法调用






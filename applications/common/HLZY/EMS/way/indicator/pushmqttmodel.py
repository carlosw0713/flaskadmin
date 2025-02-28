# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/11/27
Description: <Brief description of the file>
"""
# from HLZY.EMS.way.indicator.indicator import Indicator
from applications.common.HLZY.EMS.way.indicator.indicatorway import IndicatorWay


class PushMQTTModel(IndicatorWay):


    def pushmqtt_model(self):
        '''
        获取指标定义信息
        1.根据需要测试的指标，获取 关联设备id、指标应用，获取指标定义值
        2.根据指标定义 和关联设备id，获取符合这个设备下、点位类型符合的采集点和计算点信息
        3.根据采集点和计算点信息，获取数据来源于那个子网关（直连设备）的那个物模型点位的值，
        最终构成 数据来源的测试数据
        :return:
        '''

        deviceCodelist=['dev_ele_a']

        # indicator='峰谷分析'
        appSceneId = 8  # 8：峰谷分析

        mqttdatamockmodel = {}
        for deviceCode in deviceCodelist:

            # 获取指标编码
            indicatorCodeList=list(set([ i.get('indicatorCode') for i in self.indicatorapppage(appSceneId= appSceneId)]))

            # indicatorCodeList = ["M_VRVXG","M_Qxnt6","M_GzRqN","M_Y5flb"]

            # 过滤公式中的值，提取出对应的点位类型
            pointTypeNamelist=self.getindicatortypevalue(indicatorCodeList=indicatorCodeList).values()


            # 根据点位类型 加设备code信息，获取采集点和计算点信息
            identifierlist=self.getobjmodeldata(deviceCode=deviceCode,pointTypeNamelist=pointTypeNamelist)


            # 根据采集点和计算点信息，获取数据来源于那个子网关（直连设备）的那个物模型点位的值，

            data_dict={}
            for j in identifierlist:

                # if len(j)>2:
                #     continue

                data_dict[j]='11'
            mqttdatamockmodel[deviceCode]=data_dict

        print(mqttdatamockmodel)

    def pushmqtt_modelbypoint(self):
        ''''
        获取设备点位类型信息，获取mqtt推送model
        '''

        deviceCodelist = [
            "V1736496191424",
        ]

        pointTypeNamelist=['正向有功电度']
        # 根据点位类型 加设备code信息，获取采集点和计算点信息
        identifierlist = self.getobjmodeldata(deviceCode=deviceCodelist, pointTypeNamelist=pointTypeNamelist)
        print(identifierlist)


if __name__ == '__main__':

    task=PushMQTTModel()
    task.pushmqtt_model()

    # task.pushmqtt_modelbypoint()
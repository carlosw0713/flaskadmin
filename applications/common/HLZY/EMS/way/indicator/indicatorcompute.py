# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/11/27
Description: <Brief description of the file>
"""
from datetime import datetime
from statistics import median

from applications.common.HLZY.EMS.outway.indicator.indicator import Indicator
from applications.common.HLZY.EMS.way.data.Abnormaldatareplacement import AbnormalDataReplacementWay
from applications.common.HLZY.EMS.outway.device.device import DeviceData
from applications.common.HLZY.IOT import *


class IndicatorComputeWay(Indicator,DeviceData):

    def runindicatorcomepute(self):
        '''
        数据计算来源
        mysql数据库、td数据库、指标定义接口返回
        入参：设备编号/维度、数据分析页Id、取值（范围、类型、计算公式）
        结果：设备/维度下，统计的数据值
        :return:
        '''

        # 设备维度
        datasourcetype='api'
        devicecode='dev_ele_aa'
        organdimensionName='上海西站'
        energydimensionName='电'

        #分析页信息
        appSceneId=14

        #取值
        Timeframe=['2024-10-26 17:10:00','2024-11-26 17:10:00']
        value_type='sum' # max,min,last,avg
        computationalformula='max+1'# 计算公式

    def getpointTypecode_byId(self,pointTypeId):
      '''
      根据点位类型id获取点位类型code
      :return:
      '''

      pointTypepage = self.pointTypepage().get('data').get('records')
      for pointTypepageinfo in pointTypepage:
         pointTypeCode = pointTypepageinfo.get('pointTypeCode')
         pointTypeName = pointTypepageinfo.get('id')

         if pointTypeId == pointTypeName:
            return pointTypeCode

    def comeputevalue(self,icatorvalueinfo):
        '''
        数据计算
        :param icatorvalueinfo:
        :return:
        '''

        INFO.logger.info(f"按点位区分的值{icatorvalueinfo}")

        pointvaluedict={}
        for pointtype,pointvaluelist in icatorvalueinfo.items():
            if not pointvaluelist:
                continue

            max_value=max(pointvaluelist)
            sum_value=sum(pointvaluelist)
            min_value=min(pointvaluelist)
            mid_value=median(pointvaluelist)
            avg_value=sum_value/len(pointvaluelist)
            pointvaluedict[pointtype]={
                'max':max_value,
                'sum':sum_value,
                'min':min_value,
                'mid':mid_value,
                'avg':avg_value,
                'dif':pointvaluelist[-1]-pointvaluelist[0] #last -first
            }

        INFO.logger.info(f"按点位计算的值{pointvaluedict}")
        return pointvaluedict

    def differentiatepoint(self,deviceCode,icatorLibraryquerydatainfolist):
        '''
        区别点位类型
        1.区分是采集点还是计算点
        :return:
        '''

        pointCodepage=self.pointCodepage(deviceCode=deviceCode).get('data').get('records')
        calPointCodepage=self.calPointCodepage(deviceCode=deviceCode).get('data').get('records')

        # print(pointCodepage)
        pointCodepage_codelist=[item['pointCode'] for item in pointCodepage]
        calpointCodepage_codelist=[item['pointCode'] for item in calPointCodepage]

        icatordict={}
        icatordict2={'pointCode':[],
                     'calpointCode':[],
                     'NopointCode':[]}

        for item in icatorLibraryquerydatainfolist:
            icatorvalue=round(float(item['value'])) #整数化
            point=item.get('point','无点位')

            # devicecode=item['设备编号']
            # groupframe=item['组织架构']

            if icatordict.get(point) is None:
                icatordict[point]=[icatorvalue]
            else:
                icatordict[point].append(icatorvalue)

        #、按点位类型相加
        for pointcode,pointvaluelist  in icatordict.items():
            if pointcode in pointCodepage_codelist:
                icatordict2['pointCode'].extend(pointvaluelist)
            elif pointcode in calpointCodepage_codelist:
                icatordict2['calpointCode'].extend(pointvaluelist)
            else:
                # WARNING.logger.warning('点位不存在：'+pointcode)
                icatordict2['NopointCode'].extend(pointvaluelist)

        # 加一层判断，如果仅无点位，则给采集点和计算点赋值,周期计算。
        if icatordict2['calpointCode'] == [] and icatordict2['pointCode'] == []:
            icatordict2['pointCode']=icatordict2['NopointCode']
            icatordict2['calpointCode']=icatordict2['NopointCode']

        # icatordict2['deviceCode']=deviceCode

        # print(icatordict2)
        return icatordict2


    def indicatorcomepute(self,json_data):
        '''
        指标计算和查询
        :return:
        '''

        pointvalueinfolist=[]
        deviceCodes=json_data.get('deviceCodes')
        for deviceCode in deviceCodes:

            icatorLibraryquerydatainfolist=self.icatorLibraryquerydata(json_data=json_data).get('data')

            # 按点位分组
            icatorvalueinfo=self.differentiatepoint(deviceCode=deviceCode,icatorLibraryquerydatainfolist=icatorLibraryquerydatainfolist)

            # 按点位计算结果
            pointvaluedict=self.comeputevalue(icatorvalueinfo=icatorvalueinfo)

            # pointvalueinfolist[deviceCode]=pointvaluedict
            pointvaluedict['deviceCode']=pointvaluedict
            pointvalueinfolist.append(pointvaluedict)

        return pointvalueinfolist



    def assert_indicatordata_bypoint(self):
        '''
        判断点位计算结果是否正确
        指定点位和日期
        1.根据点位获取真实设备和虚拟设备，
        2.获取计算点存在的其他点位和设备
        :return:
        '''

        pointCode='col_To8BpX'
        caltimedata='2025-01-06'

        # 获取计算点信息
        calPointCodepage=self.calPointCodepage(deviceCode="").get('data').get('records')
        # 获取指标定义信息
        indicatorLibrarypage=self.indicatorLibrarypage(indicatortype=1,publishStatus=1).get('data').get('records')


        for calitem in calPointCodepage:

            # 获取计算点和计算点内采集点的信息
            pointformula=calitem['formula']
            if pointCode in pointformula:

                colpointCode=calitem.get('pointCode')

                pointTypeId = calitem['pointTypeId']

                pointCodelist=str(pointformula).split("+") #1.暂时的计算点全是按点位相加，暂时写死，然后取采集点值，2.也可以通过循环查point是否都在一个计算点内

                # 获取点位类型code
                pointTypeCode = self.getpointTypecode_byId(pointTypeId=pointTypeId)
                # 找到包含是这个点位类型的指标
                for indicatorLibraryinfo in indicatorLibrarypage:
                    code=indicatorLibraryinfo['code']
                    indicatorname=indicatorLibraryinfo['name']
                    indicatorId=indicatorLibraryinfo['id']
                    decimalNumber=indicatorLibraryinfo['decimalNumber']# 保留小数位

                    taskId=indicatorLibraryinfo['taskId']
                    timeType=indicatorLibraryinfo.get('timeType','数据无值异常')
                    if taskId is None or timeType =="month": # 过滤掉非日指标
                        # WARNING.logger.warning(f"指标{code}没有任务id")
                        continue

                    # 判断点位类型是否和计算点一致
                    indicatorformula=indicatorLibraryinfo.get('formula','数据无值异常')
                    if pointTypeCode in indicatorformula:

                        basic_json_data = {
                            'indicatorId': indicatorId,
                            'startTime': int(datetime.strptime(f"{caltimedata} 00:00:00",
                                                               "%Y-%m-%d %H:%M:%S").timestamp() * 1000),
                            'endTime': int(datetime.strptime(f"{caltimedata} 23:59:59",
                                                             "%Y-%m-%d %H:%M:%S").timestamp() * 1000),
                            'paramDTOS': []
                        }

                        # 获取基础指标数据
                        basic_icatordata = self.icatorLibraryquerydata(json_data=basic_json_data).get('data')

                        colpointvalue=0 #计算点值记录
                        pointcodevaluedict={} #采集点值记录
                        for timeindex,basic_icatordatainfo in enumerate(basic_icatordata):
                            datapoint=basic_icatordatainfo['point']
                            datavalue=float(basic_icatordatainfo['value'])
                            # biz_time=basic_icatordatainfo['biz_time']

                            # 获取计算点和采集点值
                            if datapoint in pointCodelist:
                                if pointcodevaluedict.get(datapoint) is None:
                                    pointcodevaluedict[datapoint]=datavalue
                                else:
                                    pointcodevaluedict[datapoint]+=datavalue
                            elif datapoint == colpointCode:
                                colpointvalue+=datavalue

                            else:
                                # WARNING.logger.warning(f'点位：{datapoint}不在计算点内')
                                pass

                        # 按天汇总计算
                        sumpointcodevalue = round(sum(pointcodevaluedict.values()),decimalNumber)# 保留小数位和指标定义一致
                        if colpointvalue == sumpointcodevalue:
                            INFO.logger.info(
                                f'指标:{indicatorname}/{code},时间:{caltimedata},计算点位：{colpointCode},计算正确，计算点值：{colpointvalue}，采集总值：{sumpointcodevalue}\n采集点信息{pointcodevaluedict}')
                        else:
                            ERROR.logger.error(
                                f'指标:{indicatorname}/{code},时间:{caltimedata},计算点位：{colpointCode},计算错误，计算点值：{colpointvalue}，采集总值：{sumpointcodevalue}\n采集点信息{pointcodevaluedict}')

                        # # 重新初始化采集点和计算点的值
                        # colpointvalue=0
                        # pointcodevaluedict={}



    def assert_indicatorRecombinationCode_bytime(self,devicecodelist=None,caltimedata=None):
        '''
        判断周期计算取值是否正确
        判断指定日期的复合函数数据是否正确
        :return:
        '''

        if not devicecodelist:
            devicecodelist=['HLGW1012426003188_RS48512','HLGW1012426003172_RS48514']
            caltimedata = '2024-12-01'

        # 存储基础指标的值
        basicdevicecodevaluedict={} #{"M_Cy5nc":{"TEST_EL_A":1,"TEST_EL_B":2}}

        # 获取复合指标信息
        indicatorRecombinationCodelist=self.indicatorLibrarypage(indicatortype=2).get('data').get('records')

        # 获取全部指标信息
        indicatorLibrarypage=self.indicatorLibrarypage().get('data').get('records')

        # 复合指标，先判断指标的周期是月还是年，然后根据指定时间判断这个阶段的值是否计算正确
        for indicatorRecombinationCodeinfo in indicatorRecombinationCodelist:
            timetype=indicatorRecombinationCodeinfo.get('timeType')
            month_indicatorId=indicatorRecombinationCodeinfo.get('id')
            formula=indicatorRecombinationCodeinfo.get('formula')
            indicatorName=indicatorRecombinationCodeinfo.get('name')

            # 根据复合指标的计算公式获取指标code和id
            for indicatorLibraryinfo in indicatorLibrarypage:
                code=indicatorLibraryinfo.get('code')
                basicindicatorId = indicatorLibraryinfo.get('id')
                if code in formula:
                    # 按指标分组
                    basicdevicecodevaluedict[code] = {}
                    break

            basic_json_data={
                    'indicatorId': basicindicatorId,
                    'startTime':int(datetime.strptime(f"{caltimedata[:7]}-01 00:00:00", "%Y-%m-%d %H:%M:%S").timestamp()* 1000),
                    'endTime':int(datetime.strptime(f"{caltimedata[:7]}-31 23:59:59", "%Y-%m-%d %H:%M:%S").timestamp()* 1000),
                    'paramDTOS': []
                }

            basic_icatordata = self.icatorLibraryquerydata(json_data=basic_json_data).get('data')
            for item in basic_icatordata:
                devicecode=item['设备编号']
                if devicecode not in devicecodelist:
                    continue

                if basicdevicecodevaluedict[code].get(devicecode) is None:
                    basicdevicecodevaluedict[code][devicecode]=float(item['value'])
                else:
                    basicdevicecodevaluedict[code][devicecode]+=float(item['value'])

            # 按月判断值
            if timetype=='month':
                month_json_data = {
                    'indicatorId': month_indicatorId,
                    'startTime':int(datetime.strptime(f"{caltimedata[:7]}-01 00:00:00", "%Y-%m-%d %H:%M:%S").timestamp()* 1000),
                    'endTime':int(datetime.strptime(f"{caltimedata[:7]}-30 23:59:59", "%Y-%m-%d %H:%M:%S").timestamp()* 1000),
                    'paramDTOS': []
                }

                month_icatordata = self.icatorLibraryquerydata(json_data=month_json_data).get('data')
                for item in month_icatordata:
                    devicecode=item['设备编号']
                    month_value=round(float(item['value']),2)

                    basic_sumvalue=basicdevicecodevaluedict[code].get(devicecode)
                    if basic_sumvalue is None: #上面可能过滤了设备，这个写进来保险。
                        continue

                    basic_sumvalue=round(float(basic_sumvalue),2)

                    if month_value==basic_sumvalue:
                        INFO.logger.info(f'月度指标 {indicatorName} 计算正确:设备:{devicecode},基础指标计算总值{basic_sumvalue}，月指标计算总值{month_value}')
                    else:
                        # 不正确可能是每个日指标跑了调度任务，可以重新整体跑一边数据后再计算
                        ERROR.logger.error(f'月度指标 {indicatorName} 计算错误:设备:{devicecode},基础指标计算总值{basic_sumvalue}，月指标计算总值{month_value}')

            elif timetype=='year':
                pass

    def assert_indicatorinrule(self):
        '''
        判断指标查询的周期数据是否复合规律范围
        :return:
        '''

        caltimedata='2024-12-01'
        devicepage=self.devicepage(deviceCode='HLGW').get('data').get('records')
        deviceCodes=[i.get('deviceCode') for i in devicepage]
        deviceCodes=['HLGW1012426003179_RS48511', 'HLGW1012426003179_RS48512']
        indicatorLibrarypage = self.indicatorLibrarypage().get('data').get('records')

        # 按日期查询不同指标信息
        for indicatorLibraryinfo in indicatorLibrarypage:
            indicatorId = indicatorLibraryinfo.get('id')
            timeType = indicatorLibraryinfo.get('timeType')
            indicatorName = indicatorLibraryinfo.get('name')
            taskId=indicatorLibraryinfo.get('taskId')

            if taskId is None:
                continue

            startTime = int(
                datetime.strptime(f"{caltimedata[0:7]}-01 00:00:00", "%Y-%m-%d %H:%M:%S").timestamp() * 1000)
            endTime = int(datetime.strptime(f"{caltimedata[0:7]}-30 23:59:59", "%Y-%m-%d %H:%M:%S").timestamp() * 1000)

            if timeType == 'month':
                startTime = int(datetime.strptime(f"{caltimedata[0:4]}-01-01 00:00:00",
                                                  "%Y-%m-%d %H:%M:%S").timestamp() * 1000)
                endTime = int(datetime.strptime(f"{caltimedata[0:4]}-12-31 23:59:59",
                                                "%Y-%m-%d %H:%M:%S").timestamp() * 1000)

            if timeType == 'year':
                startTime = int(datetime.strptime(f"2020-01-01 00:00:00",
                                                  "%Y-%m-%d %H:%M:%S").timestamp() * 1000)
                endTime = int(datetime.strptime(f"2025-12-31 23:59:59",
                                                "%Y-%m-%d %H:%M:%S").timestamp() * 1000)
            # 根据id查询数据
            json_data = {
                'indicatorId': indicatorId,
                'startTime': startTime,
                'endTime': endTime,
                'paramDTOS': []
            }

            json_data['deviceCodes']=deviceCodes
            indicatorvaluedict=self.indicatorcomepute(json_data=json_data)
            # indicatorvaluedict['indicatorName']=indicatorName

            #判断规则是否复合
            self.assert_indicatorvaluerule(indicatorvaluedict=indicatorvaluedict,indicatorName=indicatorName)

            break

    def assert_indicatorvaluerule(self, indicatorvaluedict,indicatorName):
        '''
        判断计算规则是否满足
        :return:
        '''

        indicatorName = indicatorName
        mid_value=indicatorvaluedict.get('mid')
        min_value=indicatorvaluedict.get('min')
        max_value=indicatorvaluedict.get('max')
        print(indicatorvaluedict)

        # 判断最大值和最小值，是否和中位数差值是多少




if __name__ == '__main__':
    task=IndicatorComputeWay()
    try:
        json_data={
                'deviceCodes':['HLGW1012426003188_RS48511','HLGW1012426003188_RS48512'],
                # 'groupframe':'14',
                'startTime':int(datetime.strptime("2025-01-01 00:00:00", "%Y-%m-%d %H:%M:%S").timestamp()* 1000),
                'endTime':int(datetime.strptime("2025-01-01 23:59:59", "%Y-%m-%d %H:%M:%S").timestamp()* 1000),
                'indicatorId':'48'
            }
        # task.indicatorcomepute(json_data=json_data)

        task.assert_indicatorRecombinationCode_bytime()
    except Exception as e:
        ERROR.logger.error(f"执行报错{e}")


    # task.assert_indicatorinrule()

    # task.assert_indicatordata_bypoint()





# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/11/28
Description: <Brief description of the file>
"""

import random
from datetime import datetime

from applications.common.HLZY.EMS.outway.data.manualemploymentdata import ManualEmploymentData
from applications.common.HLZY.IOT import *
class ManualEmploymentDataWay(ManualEmploymentData):

    def __init__(self):
        self.cookies = EMS_INFO.get('cookies')
        self.headers = EMS_INFO.get('headers')
        self.uri = EMS_INFO.get('uri')

    def addmanualemploymentdataexlmodel(self):
        '''
        新增手工数据导入模板
        :return:
        '''

        manualemployment_exldata=[[]]
        firest_row = ['日期','上海', '嘉定区', '上海西站', '陈翔公路', '虹口区', '三门路', '黄浦区', '外滩', '南京东路', '青浦区']
        firest_row = ['日期','产量点A']
        exlmodeldir=os.path.join(BASE_DIR, 'static', 'exl', 'manualDataCell', 'TEST', '手动.xlsx')
        exlsavedir=os.path.join(BASE_DIR, 'static', 'exl', 'manualDataCell', 'TEST', '手动录入产量A指标.xlsx')

        manualemployment_exldata.append(firest_row)

        tslist = TimeWay().generate_date_or_timestamp_list(
        start_time_str="2024-12-01 00:00:00", end_time_str="2025-01-30 23:10:00",
        time_unit='day', output_format="data", if_nowtime=False)  # 获取时间列表 时间戳格式
        for i in tslist:
            date=str(i).split(" ")[0] # 获取时间列表 日格式
            output_data=[random.randint(50,149) for i in range(len(firest_row)-1)] #注意是len(firest_row)-1，多了日期
            row_data=[date]+output_data
            manualemployment_exldata.append(row_data)

        append_excel_data(file_name=exlsavedir, sheet_name='手工数据', exl_data=manualemployment_exldata, loc=[0,1], savecopy=False)
    def batchunitConsumeAssessBasisadd(self):
        '''
        批量新增考核指标信息
        :return:
        '''
        # json_data = {    'organizeId': 46,
        #                  'productName': '产量点A',
        #                  'type': 'day',
        #                  'energyTypeId': 43,
        #                  'basisDate': '2024-11-01',
        #                  'basisValue': 1,
        #                  'unitId': 1027,
        #                  }
        organizeIdLIst=[13]
        unitId=1
        energyTypeIdList=[11]
        productNameList=['产量点A','产量点B','产量点C']
        productNameList=['产量点C']
        tslist = TimeWay().generate_date_or_timestamp_list(
        start_time_str="2024-12-01 00:00:00", end_time_str="2025-01-30 23:10:00",
        time_unit='day', output_format="data", if_nowtime=False)  # 获取时间列表 时间戳格式
        # tslist=['2024-10-01 00:00:00','2024-11-01 00:00:00']
        # tslist=['2024-01-01 00:00:00']
        for organizeId in organizeIdLIst:

            for energyTypeId in energyTypeIdList:

                for productName in productNameList:

                    for index_value,timedata in enumerate(tslist):
                        # timedata=str(timedata).split(" ")[0]
                        # 日期时间字符串
                        # date_str = "2024-10-01 00:00:00"

                        # 将字符串转换为 datetime 对象
                        date_obj = datetime.strptime(timedata, "%Y-%m-%d %H:%M:%S")

                        # 指标值
                        # basisValue = date_obj.day
                        # basisValue = random.randint(800,1500)
                        basisValue = 300

                        index_value+=1
                        json_data = {    'organizeId': organizeId,
                         'productName': productName,
                         'type': 'day',
                         'energyTypeId': energyTypeId,
                         'basisDate': timedata,
                         'basisValue': basisValue,
                         'unitId': unitId,
                         }

                        self.unitConsumeAssessBasisadd(json_data=json_data)

    def bacthunitConsumeAssessBasisdelete(self):
        '''
        批量删除考核指标信息
        :return:
        '''

        params = {
              'size': '1000',
              'current': '1',
              # 'organizeId': '14',
              'productName': '',
              'energyTypeId': '',
              'type': 'day',
              'startTime': '2024-10-10',
              'endTime': '2025-01-30',}

        unitConsumeAssessBasispageinfolist=self.unitConsumeAssessBasispage(params=params).get('data').get('records')
        unitConsumeAssessBasisIdList=[i.get('id') for i in unitConsumeAssessBasispageinfolist]

        for unitConsumeAssessBasisId in unitConsumeAssessBasisIdList:
            self.unitConsumeAssessBasisdelete(id=unitConsumeAssessBasisId)




if __name__ == '__main__':
    task=ManualEmploymentDataWay()
    # task.addmanualemploymentdataexlmodel()

    task.batchunitConsumeAssessBasisadd()

    # task.bacthunitConsumeAssessBasisdelete()

# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/12/18
Description: <异常数据补录计算>
"""
from datetime import datetime

from applications.common.HLZY.EMS.outway.indicator.indicator import Indicator
from applications.common.HLZY.IOT import *
class AbnormalDataReplacementWay(Indicator):

   def sel_indicator_by_pointcode(self,pointTypeCode,IndicatorComputeWay):
      '''
      根据点位类型查询，指标
      :return:
      '''

      indicatorLibrarypage=self.indicatorLibrarypage().get('data').get('records')

      # 基础指标
      indicatorBasicCodelist=[]
      for indicatorLibraryinfo in indicatorLibrarypage:
         formula=indicatorLibraryinfo.get('formula','异常处理怕返回None')
         taskId=indicatorLibraryinfo.get('taskId')
         indicatorcode=indicatorLibraryinfo.get('code')

         try:
            if pointTypeCode not in formula or ('MAX' and 'MIN') not in formula:
               continue
            if taskId is None:
               continue

            # indicatorBasicCodelist.append(indicatorcode)
            indicatorBasicCodelist.append(indicatorLibraryinfo) #直接返回所有信息
         except Exception as e:
            ERROR.logger.error(f'指标库信息获取失败，{e}')


      #复合指标
      indicatorRecombinationCodelist=[]
      for indicatorcode in indicatorBasicCodelist:
         for indicatorLibraryinfo in indicatorLibrarypage:
            indicatortype=indicatorLibraryinfo.get('type')
            formula = indicatorLibraryinfo.get('formula')
            indicatorcode = indicatorLibraryinfo.get('code')
            if indicatortype ==2 and indicatorcode in formula:

               # indicatorRecombinationCodelist.append(indicatorcode)
               indicatorRecombinationCodelist.append(indicatorLibraryinfo) #执行返回所有信息

      return indicatorBasicCodelist,indicatorRecombinationCodelist

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

   def getcalpointinfo_bypointcode(self,pointcode):
      '''
      补录设备信息获取
      获取包含补录指标的采集点的计算点值
      :return:
      '''
      pointCodepage = self.pointCodepage(deviceCode='').get('data').get('records')
      calPointCodepage = self.calPointCodepage(deviceCode="").get('data').get('records')

      pointTypeId=0
      for pointCodepageinfo in pointCodepage:
         if pointcode == pointCodepageinfo.get('pointCode'):
            pointTypeId=pointCodepageinfo.get('pointTypeId')
            break

      calPointCodepagelist=[]
      for calPointCodepageinfo in calPointCodepage:
         formula=calPointCodepageinfo.get('formula')
         calpointCode=calPointCodepageinfo.get('pointCode')
         calpointTypeId=calPointCodepageinfo.get('pointTypeId')
         if pointcode in formula:
            if calpointTypeId==pointTypeId:
               calPointCodepagelist.append(calPointCodepageinfo)
            else:
               ERROR.logger.error(f'计算点{pointcode}和采集点{calpointCode}，点位类型不一致')


      return calPointCodepagelist


   def assert_indicatordata(self):
      '''
      异常指标数据判断
      入参：1.采集点，指定日期
      流程:
      1.根据采集点，获取点位类型、设备编号、被引用的计算点
      2.根据点位类型，获取关联的基础指标和复合指标，判断指标是否计算正确
      :return:
      '''

      pointcode='col_dhZjVL'
      caltimedata='2024-11-08'
      changevalue=1001.99

      calpointcodeinfolist=self.getcalpointinfo_bypointcode(pointcode=pointcode)
      pointtypeId=calpointcodeinfolist[0].get('pointTypeId')

      # 获取点位类型code
      pointTypeCode=self.getpointTypecode_byId(pointTypeId=pointtypeId)

      # 获取指标相关信息
      indicatorBasicCodelist, indicatorRecombinationCodelist=self.sel_indicator_by_pointcode(pointTypeCode=pointTypeCode)

      # 基础指标的判断
      for indicatorBasicCodeinfo in indicatorBasicCodelist:
         indicatorId=indicatorBasicCodeinfo.get('id')
         indicatorName=indicatorBasicCodeinfo.get('name')
         formula=indicatorBasicCodeinfo.get('formula')

         json_data = {
            'indicatorId': indicatorId,
            'startTime': int(datetime.strptime(f"{caltimedata} 00:00:00", "%Y-%m-%d %H:%M:%S").timestamp() * 1000),
            'endTime': int(datetime.strptime(f"{caltimedata} 23:59:59", "%Y-%m-%d %H:%M:%S").timestamp() * 1000),
            'paramDTOS': []
         }

         # 基础指标的判断
         icatorLibraryquerydatainfolist = self.icatorLibraryquerydata(json_data=json_data).get('data')
         for numbeiindex,icatorLibraryquerydata in enumerate(icatorLibraryquerydatainfolist):
            if pointcode==icatorLibraryquerydata.get('point'):
               icatorLibrarynewvalue=icatorLibraryquerydata.get('value')

               if changevalue==icatorLibrarynewvalue:
                  INFO.logger.info(f'指标：{indicatorName}，采集点{pointcode}，指定时间{caltimedata}，数据值{icatorLibrarynewvalue}，期望值{changevalue},数据正常')
               else:
                  ERROR.logger.error(f'指标：{indicatorName}，采集点{pointcode}，指定时间{caltimedata}，数据值{icatorLibrarynewvalue}，期望值{changevalue}，数据异常')
               break
            if numbeiindex==len(icatorLibraryquerydatainfolist)-1:
               ERROR.logger.error(f'指标：{indicatorName}，采集点{pointcode}，指定时间{caltimedata}，找不到数据值！！！')

      # 复合指标判断 ，直接用指标数据计算那块解决。assert_indicatorRecombinationCode_bytime

      # 计算点信息判断，



if __name__ == '__main__':
    task=AbnormalDataReplacementWay()
    task.assert_indicatordata()




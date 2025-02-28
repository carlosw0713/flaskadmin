# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/12/3
Description: <Brief description of the file>
"""
from calendar import month
from datetime import datetime

from applications.common.HLZY.EMS.outway.electriccharge.electriccharge import ElectricCharge
from applications.common.HLZY.EMS.way.indicator.indicatorcompute import IndicatorComputeWay
from applications.common.HLZY.IOT import *
class ElectricChargeWay(ElectricCharge):

    def calculate_demand_price_fee(self,demand, capacity, base_ratio, demand_price, capacity_price, active_power, discount_ratio,discountStandard):
        """
        计算需量基本电费
        :param demand: 需量（当前需量最大值）
        :param capacity: 容量
        :param base_ratio: 基准比例
        :param demand_price: 需量电价
        :param capacity_price: 容量电价
        :param active_power: 本月正向有功电量累计值
        :param discount_ratio: 折扣比例
        :return: 需量基本电费
        """
        # 需量小于容量*基准比例
        INFO.logger.info(f"[计算需量基本电费] 需量：{demand}, 容量：{capacity}, 基准比例：{base_ratio}, 需量电价：{demand_price}, 容量电价：{capacity_price}, 本月正向有功电量累计值：{active_power}, 折扣比例：{discount_ratio}, 折扣标准：{discountStandard}")
        # if demand < capacity * base_ratio:
        if False: #目前默认不走这条逻辑了。
            basic_electric_charge = capacity * base_ratio * capacity_price
            INFO.logger.info(f"[第一种]需量小于容量*基准比例,计算出的需量基本电费为：{basic_electric_charge}")

         # 需量大于等于容量*基准比例
        else:
            # 容量*折扣标准 小于 本月正向有功电量累计值
            if capacity * discountStandard <= active_power:
                # 满足条件 需量电价*需量*折扣比例
                basic_electric_charge = demand * demand_price * discount_ratio
                INFO.logger.info(f"[第二种]容量*折扣比例 小于 本月正向有功电量累计值,计算出的需量基本电费为：{basic_electric_charge}")
            else:
                # 不满足条件 需量电价*需量
                basic_electric_charge = demand * demand_price
                INFO.logger.info(f"[第三种]容量*折扣比例 大于 本月正向有功电量累计值,计算出的需量基本电费为：{basic_electric_charge}")

        # INFO.logger.info(f"计算出的需量基本电费为：{basic_electric_charge}")
        return basic_electric_charge


    def electricityPrice_by_month(self,electricityPricerulelist, month):
        """
        获取指定月份的有效 capacityPrice
        :param electricityPricerulelist: 容量电价数据
        :param month: 月份 (格式为 YYYY-MM)
        :return: capacityPrice
        """

        month=datetime.strptime(month, '%Y-%m')
        for pricing in electricityPricerulelist:
            effectiveTime=datetime.strptime(pricing['effectiveTime'], '%Y-%m-%d')
            expirationTime=datetime.strptime(pricing['expirationTime'], '%Y-%m-%d')

            if effectiveTime <= month <= expirationTime:

                return pricing
        return None

    def assert_feeinfo(self,month, echart_data, calculated_capacity_price,calculated_demand_price,calculated_capacity_price_turnover_point):
        """
        判断费用分析表是否正常
        1.判断 容量基本电费
        2.判断 需量基本电费
        3.判断 容需量成本转折点 容量基本电费/生效的需量电价
        """

        self.assert_capacity_price(month, echart_data, calculated_capacity_price)

        self.assert_demand_price(month, echart_data, calculated_demand_price)

        self.assert_capacity_price_turnover_point(month, echart_data, calculated_capacity_price_turnover_point)

    def assert_capacity_price(self, month, echart_data, calculated_capacity_price):
        """
        判断容量基本电费
        """

        # 获取 series 中 name 为 容量基本电费(元 对应月份的值
        index = echart_data['category'].index(month)
        capacity_value = echart_data['series'][5]['data'][index]
        # demand_value = echart_data['series'][2]['data'][index]

        # 比较自己计算的容量基本电费和值和echart表中基准值
        if calculated_capacity_price == capacity_value:
            INFO.logger.info(f"容量基本电费和基准值相等，计算结果为：{calculated_capacity_price},基准值为：{capacity_value}")
            return True
        else:
            ERROR.logger.error(f"容量基本电费和基准值不相等，计算结果为：{calculated_capacity_price},基准值为：{capacity_value}")
            return False
    def assert_demand_price(self,month,echart_data, calculated_demand_price):
        """
        判断需量基本电费
        """

        # 获取 series 中 name 为 容量基本电费(元 对应月份的值
        index = echart_data['category'].index(month)
        # capacity_value = echart_data['series'][5]['data'][index]
        demand_value = echart_data['series'][2]['data'][index]

        # 比较自己计算的需量基本电费和值和echart表中基准值
        if calculated_demand_price == demand_value:
            INFO.logger.info(f"需量基本电费和基准值相等，计算结果为：{calculated_demand_price},基准值为：{demand_value}")
            return True
        else:
            ERROR.logger.error(f"需量基本电费和基准值不相等，计算结果为：{calculated_demand_price},基准值为：{demand_value}")
            return False

    def assert_capacity_price_turnover_point(self,month,echart_data, calculated_capacity_price_turnover_point):
        """
        判断容需量成本转折点
        """
        # 获取 series 中 name 为 容量基本电费(元 对应月份的值
        index = echart_data['category'].index(month)
        # capacity_value = echart_data['series'][5]['data'][index]
        price_turnover_point = echart_data['series'][7]['data'][index]

        # 比较自己计算的需量成本转折点和值和echart表中基准值
        if calculated_capacity_price_turnover_point == price_turnover_point:
            INFO.logger.info(f"需量成本转折点和基准值相等，计算结果为：{calculated_capacity_price_turnover_point},基准值为：{price_turnover_point}")
            return True
        else:
            ERROR.logger.error(f"需量成本转折点和基准值不相等，计算结果为：{calculated_capacity_price_turnover_point},基准值为：{price_turnover_point}")
            return False
    def demandvalue_by_month(self ,month):
        '''
        根据月份获取最大需量值
        :param month:
        :return:
        '''

        json_data={
            'deviceCodes':['V1736496191424'], #写死目前 上海下面的虚拟设备
            # 'groupframe':'13',#设备维度
            'startTime':int(datetime.strptime(f"{month}-01 00:00:00", "%Y-%m-%d %H:%M:%S").timestamp()* 1000),
            'endTime':int(datetime.strptime(f"{month}-30 23:59:59", "%Y-%m-%d %H:%M:%S").timestamp()* 1000),
            'indicatorId':'198' #最大需量的指标id
        }

        IndicatorComputInfo=IndicatorComputeWay().indicatorcomepute(json_data=json_data)
        sum_value=0
        for IndicatorValueinfo in  IndicatorComputInfo:
            if IndicatorValueinfo.get('calpointCode') is None:
                sum_value+=IndicatorValueinfo.get('pointCode').get('sum')
            else:
                sum_value+=IndicatorValueinfo.get('calpointCode').get('sum')


        INFO.logger.info(f'月份:{month},最大需量值:{sum_value}')
        return sum_value

    def active_power_by_month(self,month):
        '''
        按月查询 正向有功电度
        :return:
        '''

        json_data={
            'deviceCodes':['V1736496191424'], #写死目前 上海下面的虚拟设备
            'startTime':int(datetime.strptime(f"{month}-01 00:00:00", "%Y-%m-%d %H:%M:%S").timestamp()* 1000),
            'endTime':int(datetime.strptime(f"{month}-20 23:59:59", "%Y-%m-%d %H:%M:%S").timestamp()* 1000),
            'indicatorId':'202' #正向有功电度的指标id
        }

        IndicatorComputInfo = IndicatorComputeWay().indicatorcomepute(json_data=json_data)
        sum_value = 0
        for IndicatorValueinfo in IndicatorComputInfo:
            sum_value += IndicatorValueinfo.get('pointCode').get('sum')
        INFO.logger.info(f'月份:{month},正向有功电度:{sum_value}')
        return sum_value


    def assert_electricityPricerule(self,date_range):

        Capacityvalue=10000# 容量

        # 时间范围
        # date_range='2024-12' #格式为 YYYY-MM

        # input('需要输入正向有功和最大需要的实际点位信息才可以！！！')
        #最大需量
        demandvalue=self.demandvalue_by_month(month=date_range)

        #本月正向有功累计值
        active_power=self.active_power_by_month(month=date_range)

        # 容需量电价表
        electricityPricerulelist=self.electricityPricelist().get('data').get('records')

        # 基本电费分析表
        json_data={    'startTime': '2024-11',
                             'endTime': '2025-01',
                             'energyId': '24',
                             'energyDimensionId': '2',
                             'menuId': '1863426873777778690',
                             'dimensionId': '1',
                             'groupId': '27',}
        BasicChargelist=self.getBasicCharge(json_data=json_data).get('data')
        echart_data = BasicChargelist.get('echart')

        # 按月获取容量电价计算规则数据
        electricityPricerule=self.electricityPrice_by_month(electricityPricerulelist, date_range)

        # 容量电价
        capacity_price = electricityPricerule.get('capacityPrice')
        # 需量电价
        demand_price = electricityPricerule.get('demandPrice')
        #折扣标准
        discountStandard=electricityPricerule.get('discountStandard')
        # 折扣比例
        discount_ratio = electricityPricerule.get('discountRatio')/100
        # 基准比例
        base_ratio = electricityPricerule.get('baseRatio')/100

        # 容量基本电费
        capacity_price_fee = Capacityvalue * capacity_price

        # 容需量成本转折点
        capacity_price_fee_turnover_point = f"{capacity_price_fee / demand_price :.2f}" #保留两位小数

        # 需量基本电费 计算结果
        demand_price_fee=self.calculate_demand_price_fee(demand=demandvalue, capacity=Capacityvalue,
                                       base_ratio=base_ratio,demand_price=demand_price,capacity_price=capacity_price,
                                       active_power=active_power, discount_ratio=discount_ratio,discountStandard=discountStandard)

        self.assert_feeinfo(date_range, echart_data, capacity_price_fee, demand_price_fee, capacity_price_fee_turnover_point)

    def run_assert_electricityPricerule_by_month(self):

        # for i in ['2024-10','2024-11','2024-12']:
        tslist = TimeWay().generate_date_or_timestamp_list(
            start_time_str="2024-11-01 00:00:00", end_time_str="2025-01-10 23:10:00",
            time_unit='month', output_format="data", if_nowtime=False)  # 获取时间列表 时间戳格式

        for i in tslist:
            i=str(i).split(" ")[0][0:7]
            time.sleep(0.5)

            self.assert_electricityPricerule(date_range=i)


if __name__ == '__main__':
    task=ElectricChargeWay()
    # task.assert_electricityPricerule()
    task.run_assert_electricityPricerule_by_month()

    # task.demandvalue_by_month('2024-12')
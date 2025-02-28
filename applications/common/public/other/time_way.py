#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/5/27 captchacode:08
# @Author  : carlos
# @Email   : carlos.w.0713@outlook.com
# @file_tool    : time_way.py
# @IDE     : PyCharm
# @REMARKS : 备注
import time
from datetime import datetime, timedelta
# import datetime


class TimeWay:


        def timestamp_to_date(self,timestamp):
            '''时间措转日期'''

            try: #可能出现日期出错

                if  len(str(timestamp))==13 :  # 检查毫秒部分是否为000
                    # 将毫秒时间戳转换为datetime对象
                    date = datetime.fromtimestamp(timestamp / 1000.0)
                    # 使用strftime()函数将datetime对象格式化为友好的日期字符串

                else:
                    date = datetime.fromtimestamp(timestamp)

                # 使用strftime()函数将datetime对象格式化为友好的日期字符串
                formatted_date = date.strftime('%Y-%m-%d %H:%M:%S')  # 格式：年-月-日 时:分:秒

                return formatted_date
            except:
                return f"日期转化错误：{timestamp}"



        def get_time_range(self,range_type,time_type="%Y-%m-%d %H:%M:%S",timestatus=False):
            """
            获取时间范围
            :param range_type: 时间范围类型，可选值为 "today", "this_week", "this_month", "three_months", "one_year"
            :return: 时间范围字符串
            """
            now = datetime.now()

            if isinstance(range_type, int):

                if not timestatus:
                    start_time = now - timedelta(days=range_type)
                    end_time = now
                elif timestatus=='before':
                    start_time = now - timedelta(days=range_type)
                    end_time = now - timedelta(days=1)
                elif timestatus=='after':
                    start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)  + timedelta(days=1)
                    end_time = now.replace(hour=23, minute=59, second=59, microsecond=29)  + timedelta(days=range_type)

                elif timestatus=='running':
                    start_time = now
                    end_time = now + timedelta(days=range_type)
                else:
                    Exception ("入参输入错误")

            elif range_type == "today":
                # start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
                start_time = now.replace()
                end_time = start_time + timedelta(days=1) - timedelta(microseconds=1)
            elif range_type == "this_week":
                start_time = now - timedelta(days=now.weekday())
                end_time = start_time + timedelta(days=7) - timedelta(microseconds=1)
            elif range_type == "this_month":
                start_time = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                end_time = start_time.replace(month=start_time.month+1, day=1) - timedelta(microseconds=1)
            elif range_type == "three_months":
                start_time = now - timedelta(days=90)
                end_time = start_time.replace(month=start_time.month+4, day=1) - timedelta(microseconds=1)
            elif range_type == "one_year":
                start_time = now - timedelta(days=366)
                end_time = start_time.replace(year=start_time.year+2) - timedelta(microseconds=1)
            else:
                raise ValueError("入参输入错误")

            start_str = start_time.strftime(time_type)
            end_str = end_time.strftime(time_type)

            # start_timestamp = int(start_time.timestamp())*1000
            start_timestamp = int(start_time.timestamp()*1000)
            end_timestamp = int(end_time.timestamp()*1000)

            return start_str, end_str, start_timestamp, end_timestamp

        from datetime import datetime, timedelta

        def getchangetime(self,time_value, time_type, change_amount, time_unit):
            '''
            获取时间转化后的时间
            :param time_value:
            :param time_type:
            :param change_amount:
            :param time_unit:
            :return:
            '''
            # 根据时间类型解析时间
            if time_type == 'timestamp':
                # 如果是时间戳，转换为datetime对象
                dt = datetime.fromtimestamp(time_value)
            elif time_type == 'normal':
                # 如果是正常时间，尝试解析为datetime对象
                dt = datetime.strptime(time_value, '%Y-%m-%d %H:%M:%S')
            else:
                raise ValueError("Invalid time_type. Expected 'timestamp' or 'normal'.")

            # 根据时间单位和变化量调整时间
            if time_unit == 'hours':
                dt += timedelta(hours=change_amount)
            elif time_unit == 'minutes':
                dt += timedelta(minutes=change_amount)
            elif time_unit == 'seconds':
                dt += timedelta(seconds=change_amount)
            elif time_unit == 'days':
                dt += timedelta(days=change_amount)
            else:
                raise ValueError("Invalid time_unit. Expected 'hours', 'minutes', 'seconds', or 'days'.")

            # 返回修改后的时间
            return dt

        def convert_str_to_timestamp(self, time_str, format='%Y-%m-%d %H:%M:%S'):
            """
            将时间字符串转换为时间戳

            :param time_str: 时间字符串
            :param format: 时间格式，默认为 '%Y-%m-%d %H:%M:%S'
            :return: 时间戳
            """
            time_object = time.strptime(time_str, format)
            timestamp = time.mktime(time_object)
            return timestamp


        def time_conversion(self,time_num: int):
            """
            时间戳转换成日期
            :param time_num:
            :return:
            """
            if isinstance(time_num, int):
                time_stamp= time_num
                if len(str(time_num))>11:
                    time_stamp = float(time_num / 1000)
                time_array = time.localtime(time_stamp)
                other_style_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
                return other_style_time


        def now_time(self, format="%Y-%m-%d %H:%M:%S", timetype='string'):
            """
            获取当前时间，支持返回日期字符串或时间戳格式。
            :param format: 日期字符串的格式，默认为 '%Y-%m-%d %H:%M:%S'
            :param timetype: 返回类型，'string' 返回日期字符串，'timestamp' 返回时间戳
            :return: 当前时间的字符串或时间戳
            """
            if timetype == 'string':
                # 返回日期字符串
                localtime = time.strftime(format, time.localtime())
                return localtime
            elif timetype == 'timestamp':
                # 返回时间戳
                timestamp = int(time.time()*1000)
                return timestamp
            else:
                raise ValueError("Invalid timetype. Use 'string' or 'timestamp'.")



        def now_time_day(self,after=0, before=0):
            """
            获取当前时间, 日期格式: 2021-12-captchacode
            :param after: 返回当前时间之后的天数
            :param before: 返回当前时间之前的天数
            :return: 日期字符串
            """
            current_time = time.time()
            seconds_per_day = 24 * 60 * 60  # 一天的秒数

            if after > 0:
                result_time = current_time + after * seconds_per_day
            elif before > 0:
                result_time = current_time - before * seconds_per_day
            else:
                result_time = current_time

            return time.strftime("%Y-%m-%d", time.localtime(result_time))

        def data_now_time(self):
            """
            获取当前时间, 日期格式: 2021-12-11_12-39-25
            :return: 主要用于文件名的获取
            """
            localtime = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            return localtime

        def compare_time(self,time_a, time_b, format='%Y-%m-%d %H:%M:%S'):
            """
            比较两个时间点大小
            :param time_a: 时间 a 字符串
            :param time_b: 时间 b 字符串
            :param format: 时间格式，默认为 '%Y-%m-%d %H:%M:%S'
            :return: True if a > b else False
            """
            time_a = time.strptime(time_a, format)
            time_b = time.strptime(time_b, format)

            time_a_stamp = time.mktime(time_a)
            time_b_stamp = time.mktime(time_b)

            if time_a_stamp > time_b_stamp:
                return True
            else:
                return False

        def generate_date_or_timestamp_list(self,start_time_str, end_time_str, time_unit, output_format,if_nowtime):
            """
            生成从开始时间到结束时间之间的时间段数据，根据指定的时间单位。

            :param start_time_str: 开始时间字符串，格式为 %Y-%m-%d %H:%M:%S
            :param end_time_str: 结束时间字符串，格式为 %Y-%m-%d %H:%M:%S
            :param time_unit: 时间单位，'month' 表示按月，'day' 表示按天，'hour' 表示按小时，'minute' 表示按分钟
            :return: 时间段数据列表
            """


            if if_nowtime:
                nowtime=datetime.now()
                timestamp = nowtime.timestamp()
                # 将时间戳转换为毫秒
                timestamp_ms = int(timestamp * 1000)
                return [timestamp_ms]


            # 解析开始时间和结束时间
            try:
                start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
                end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                raise ValueError("无效的时间格式，请使用 %Y-%m-%d %H:%M:%S")

            # 生成时间段数据列表
            result_list = []
            timestr_list = []
            current_time = start_time

            while current_time <= end_time:

                now = datetime.now()
                result_list.append(current_time.strftime('%Y-%m-%d %H:%M:%S'))

                timestr = current_time.timestamp()
                # 将时间戳转换回 datetime 对象
                combined_datetime = datetime.fromtimestamp(timestr).replace(microsecond=now.microsecond)  # 替换毫秒保证值不一样

                timestamp_ms = int(combined_datetime.timestamp() * 1000)
                timestr_list.append(timestamp_ms)

                #输入为正整数，则按秒级添加
                if isinstance(time_unit,int):
                    current_time += timedelta(seconds=time_unit)

                elif time_unit == 'month':
                    # 计算下一个月的第一天
                    if current_time.month == 12:
                        next_month = current_time.replace(year=current_time.year + 1, month=1, day=1)
                    else:
                        # print(current_time.month)
                        next_month = current_time.replace(month=current_time.month + 1, day=1)
                    # 计算下一个月的最后一天
                    # next_month_last_day = next_month - timedelta(days=1)
                    next_month_last_day = next_month
                    current_time = next_month_last_day
                    # print(current_time)
                elif time_unit == 'day':
                    current_time += timedelta(days=1)
                elif time_unit == 'hour':
                    current_time += timedelta(hours=1)

                elif time_unit == 'minute':
                    current_time += timedelta(minutes=1)
                else:
                    raise ValueError("无效的时间单位，请使用 'month', 'day', 'hour' 或 'minute'")

            if output_format == "timestamp":
                return timestr_list
            else:
                return result_list


if __name__ == '__main__':
    task=TimeWay()

    # 使用示例
    # start_time_str, end_time_str, start_timestamp, end_timestamp = task.get_time_range(range_type="this_month")
    # print(f"Start Time (str): {start_time_str}")
    # print(f"End Time (str): {end_time_str}")
    # print(f"Start Timestamp: {start_timestamp}")
    # print(f"End Timestamp: {end_timestamp}")

    # print(task.get_time_range(""))
    # print(task.get_time_range(range_type=2,timestatus='before'))

    A=task.generate_date_or_timestamp_list(
                "2024-11-14 07:27:24", end_time_str="2024-11-14 09:27:24",
                time_unit="minute",output_format="timestamp1",if_nowtime=True)
    print(len(A),A)





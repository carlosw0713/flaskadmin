#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/5/29 17:04
# @Author  : carlos
# @Email   : carlos.w.0713@outlook.com
# @file_tool    : exl_way.py
# @IDE     : PyCharm
# @REMARKS : 备注
import csv
import os

import openpyxl
# import numpy
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.utils.exceptions import InvalidFileException

# from settings.path import BASE_DIR
# from openpyxl.worksheet.dimensions import DimensionHolder, ColumnDimension

def create_excel_file(file_name, sheet_name):
    """创建一个新的Excel文件并添加指定的工作表"""
    wb = Workbook()
    ws = wb.active
    ws.title = sheet_name
    wb.save(file_name)
    wb.close()
def read_excel_dict(file_name, sheet_name):
    """按行读取Excel文件中的数据并返回列表"""
    try:
        wb = openpyxl.load_workbook(file_name)
        ws = wb[sheet_name]
        data = []
        for row in ws.iter_rows(min_row=1, values_only=True):
            data.append(row)
        wb.close()
        return data
    except FileNotFoundError:
        print(f"The file '{file_name}' does not exist.")
        return None
    except KeyError:
        print(f"No sheet named '{sheet_name}' found in the file.")
        return None
def append_excel_dict(file_name, sheet_name, exl_data):
    """向Excel文件的最后一行添加数据，数据应为字典格式"""
    try:
        wb = openpyxl.load_workbook(file_name)
        ws = wb[sheet_name]

        # 检查数据的列是否与工作表的列匹配
        if set(exl_data.keys()) != set(ws.column_dimensions.keys()):
            raise ValueError("Data keys do not match with the sheet's column names.")

        # 将数据转换为列表，以便可以添加到工作表中
        data_list = [exl_data.get(key) for key in ws.column_dimensions.keys()]

        # 找到最后一行并添加新数据
        last_row = max(ws.max_row, 1)
        ws.cell(row=last_row + 1, column=1).value = data_list[0]
        for col, val in zip(ws.column_dimensions.keys(), data_list[1:]):
            ws.cell(row=last_row + 1, column=ws[col].column, value=val)

        wb.save(file_name)
        wb.close()
    except FileNotFoundError:
        print(f"The file '{file_name}' does not exist.")
    except KeyError:
        print(f"No sheet named '{sheet_name}' found in the file.")
    except ValueError as e:
        print(str(e))



def read_excel_data(file_name, sheet_name, datatype='list', loc=None):
    """按行读取Excel文件中的数据并返回列表或字典"""
    try:
        wb = openpyxl.load_workbook(file_name)
        ws = wb[sheet_name]
        data = []

        start_row, start_col = 1, 1
        if loc:
            start_row, start_col = loc[0], loc[1]

        if datatype == 'list':
            for row in ws.iter_rows(min_row=start_row, min_col=start_col, values_only=True):
                data.append(list(row))
        elif datatype == 'dict':
            for row in ws.iter_rows(min_row=start_row, min_col=start_col, values_only=True):
                data.append({ws.cell(row=start_row, column=col).value: row[col - start_col] for col in range(start_col, ws.max_column + 1)})

        wb.close()
        return data
    except FileNotFoundError:
        print(f"The file '{file_name}' does not exist.")
        return None
    except KeyError:
        print(f"No sheet named '{sheet_name}' found in the file.")
        return None


def append_excel_data(file_name, sheet_name, exl_data, loc=None, savecopy=False):
    """向Excel文件的指定位置添加数据，数据应为字典/列表格式"""
    try:
        wb = openpyxl.load_workbook(file_name)

        # 尝试获取工作表
        try:
            ws = wb[sheet_name]
        except KeyError:
            # 如果工作表不存在，则创建新的工作表
            ws = wb.create_sheet(sheet_name,index=0)

        # 确定插入位置
        if loc:
            row, col = loc[0], loc[1]
        else:
            row = max(ws.max_row, 1) + 1
            col = 1

        # 判断数据类型并处理
        if isinstance(exl_data[0], dict):
            # 处理字典数据类型

            # 获取所有的keys
            first_row_values = [cell.value for cell in ws[1]]
            keys = list(exl_data[0].keys()) if exl_data else []

            # 检查列表中的值是否在第一行中，如果不在则插入
            for value in keys:
                if value not in first_row_values:
                    first_row_values.append(value)

            # 更新 Excel 表格的第一行数据
            for index, value in enumerate(first_row_values, start=1):
                ws.cell(row=1, column=index, value=value)

            # 写入数据
            for row_data in exl_data:
                for col_idx, key in enumerate(first_row_values, start=1):
                    ws.cell(row=row, column=col_idx, value=row_data.get(key, ''))
                row += 1

        elif isinstance(exl_data[0], list):
            # 处理列表数据类型
            for data_list in exl_data:
                for idx, value in enumerate(data_list, start=col):
                    ws.cell(row=row, column=idx, value=value)
                row += 1

        else:
            raise ValueError("Invalid data type. Data must be a dictionary or a list.")


        # 另存为副本，如果需要
        if savecopy:
            save_name = savecopy if isinstance(savecopy, str) else f"{file_name.split('.')[0]}_copy.xlsx"
            wb.save(save_name)
            print(f"写入exl文件{save_name}")
        else:
            wb.save(file_name)
            print(f"写入exl文件{file_name}")

        wb.close()

    except FileNotFoundError:
        print(f"The file '{file_name}' does not exist")
        directory = os.path.dirname(file_name)
        filename = os.path.basename(file_name)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # 完整的文件路径
        file_path = os.path.join(directory, filename)
        # 创建一个新的工作簿
        wb = Workbook()
        # 保存工作簿
        wb.save(file_path)
        print(f"创建文件{file_path}")
        append_excel_data(file_path, sheet_name, exl_data, loc, savecopy)
    except KeyError:
        print(f"No sheet named '{sheet_name}' found in the file.")
    except ValueError as e:
        print(str(e))



def read_csv_data(file_name, datatype='list', loc=None):
    """按行读取CSV文件中的数据并返回列表或字典"""
    data = []
    try:
        with open(file_name, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            if loc:
                start_row, start_col = loc[0], loc[1]
                for i, row in enumerate(reader):
                    if i >= start_row - 1:
                        data.append(row[start_col - 1:])
            else:
                data = list(reader)

        if datatype == 'dict' and data:
            headers = data[0]
            data = [dict(zip(headers, row)) for row in data[1:]]

        return data
    except FileNotFoundError:
        print(f"The file '{file_name}' does not exist.")
        return None


def append_csv_data(file_name, csv_data, loc=None, savecopy=False):
    """向CSV文件的指定位置添加数据，数据应为列表格式"""
    try:
        mode = 'a' if loc is None else 'w'
        with open(file_name, mode=mode, newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if loc is None:
                writer.writerows(csv_data)
            else:
                # Read existing data
                with open(file_name, mode='r', newline='', encoding='utf-8') as read_file:
                    existing_data = list(csv.reader(read_file))

                # Insert new data
                start_row, start_col = loc[0], loc[1]
                for i, row in enumerate(csv_data):
                    if i + start_row - 1 < len(existing_data):
                        existing_data[i + start_row - 1][start_col - 1:start_col - 1 + len(row)] = row
                    else:
                        existing_data.append([None] * (start_col - 1) + row)

                # Write updated data
                with open(file_name, mode='w', newline='', encoding='utf-8') as write_file:
                    writer = csv.writer(write_file)
                    writer.writerows(existing_data)

        if savecopy:
            import shutil
            copy_name = savecopy if isinstance(savecopy, str) else f"{file_name.split('.')[0]}_copy.csv"
            shutil.copy(file_name, copy_name)
            print(f"写入csv文件{copy_name}")
        else:
            print(f"写入csv文件{file_name}")

    except ValueError as e:
        print(str(e))


if __name__ == '__main__':


    a = [[None, 13142394049, 'succeed-没有填写成长值', 13142393949, None, 'VIP3', None], [None, 13142394050, 'succeed-正常在范围内', 13142393950, None, 'VIP2', 132], [None, 13142394051, 'succeed-没有成长值和会员等级', 13142393951, None, None, None], [None, 13142394052, 'fail-没有填写会员等级', 13142393952, None, None, 346], [None, 13142394053, 'fail-成长值大于当前会员等级', 13142393953, None, 'VIP2', 150], [None, 13142394054, 'fail-成长值小于当前会员等级', 13142393954, None, 'VIP5', 173], [None, 13142394055, 'fail-会员等级大于5', 13142393955, None, 'VIP6', 289], [None, 13142394056, 'fail-成长值不规范', 13142393956, None, 'VIP1', -666], [None, 13142394057, 'fail-会员已经创建', 13142392973, None, 'VIP1', 58]]

    csvfile_name = os.path.join(BASE_DIR, 'static', 'exl', 'login', 'TEST', '管理员账户信息测试.csv')
    csv_data=read_csv_data(file_name=csvfile_name,  loc=[1, 1])
    print(csv_data)





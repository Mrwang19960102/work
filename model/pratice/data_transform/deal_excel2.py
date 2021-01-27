# -*- coding: utf-8 -*-
# @File:       |   deal_excel.py 
# @Date:       |   2021/1/13 21:47
# @Author:     |   ThinkPad
# @Desc:       |  
import os
import xlrd
import openpyxl
import pandas as pd
import xlsxwriter
from deal_pdf import PDFConverter

f_excel_path = './excel文件夹'
f_pdf_path = './pdf文件夹'

if not os.path.exists(f_excel_path):
    print('创建excel文件夹')
    os.mkdir(f_excel_path)

if not os.path.exists(f_pdf_path):
    print('创建pdf文件夹')
    os.mkdir(f_pdf_path)


def trans_data():
    df = pd.read_excel('./原始信息.xlsx')
    for index, info in df.iterrows():
        em_num = info['员工编号']
        name = info['姓名']
        sex = info['性别']
        age = info['年龄']
        birth_date = info['出生日期']
        phone = info['联系电话']
        id = info['身份证号']
        p_landscape = info['政治面貌']
        department = info['所在部门']
        position = info['职务']
        induction_date = info['入职时间']
        address = info['家庭住址']
        community = info['所属社区']

        # 创建文件
        file_name = './{}/{}{}.xlsx'.format(f_excel_path, em_num, name)
        workbook = xlsxwriter.Workbook(file_name)
        merge_format = workbook.add_format({
            'bold': True,
            'font_size': 20,
            'align': 'center',  # 水平居中
            'valign': 'vcenter',  # 垂直居中
        })
        worksheet = workbook.add_worksheet()
        # 写入标题数据
        worksheet.merge_range('A6:I6', '疫情防控承诺函', merge_format)
        workbook.close()
        value_dict = {
            '所在部门：': {'col': '', 'columns': '', 'value': ''},
            '姓    名：': {'col': '', 'columns': '', 'value': ''},
            '性    别：': {'col': '', 'columns': '', 'value': ''},
            '身份证号：': {'col': '', 'columns': '', 'value': ''},
            '联系电话：': {'col': '', 'columns': '', 'value': ''},
            '入职时间：': {'col': '', 'columns': '', 'value': ''},
            '家庭住址：': {'col': '', 'columns': '', 'value': ''},
            '年    龄：': {'col': '', 'columns': '', 'value': ''},
            '职    务：': {'col': '', 'columns': '', 'value': ''},
            '员工编号：': {'col': '', 'columns': '', 'value': ''},
            '出生日期：': {'col': '', 'columns': '', 'value': ''},
            '政治面貌：': {'col': '', 'columns': '', 'value': ''},
            '所属社区：': {'col': '', 'columns': '', 'value': ''},
        }

        wb = openpyxl.load_workbook(file_name)
        sheet = wb.active
        sheet.title = str(em_num) + str(name)
        sheet['A9'] = '所在部门：'
        sheet['B9'] = department
        sheet['A11'] = '姓    名：'
        sheet['B11'] = name
        sheet['A13'] = '性    别：'
        sheet['B13'] = sex
        sheet['A15'] = '身份证号：'
        sheet['B15'] = str(id)
        sheet['A17'] = '联系电话：'
        sheet['B17'] = phone
        sheet['A19'] = '入职时间：'
        sheet['B19'] = induction_date
        sheet['A21'] = '家庭住址：'
        sheet['B21'] = address
        sheet['D13'] = '年    龄：'
        sheet['E13'] = str(age)
        sheet['F9'] = '职    务：'
        sheet['G9'] = position
        sheet['F11'] = '员工编号：'
        sheet['G11'] = str(em_num)
        sheet['F13'] = '出生日期：'
        sheet['G13'] = birth_date
        sheet['F15'] = '政治面貌：'
        sheet['G15'] = p_landscape
        sheet['F21'] = '所属社区：'
        sheet['G21'] = community
        sheet['A24'] = '本人承诺：xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

        wb.save(file_name)
        print('name={}数据存储完成'.format(name))
        # 获取到文件的sheet数
        b = xlrd.open_workbook(file_name)
        sheetnum = len(b.sheets())
        pdfConverter = PDFConverter(file_name, sheetnum)
        pdfConverter.run_conver()


if __name__ == '__main__':
    trans_data()

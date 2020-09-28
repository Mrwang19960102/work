# -*- coding: utf-8 -*-
# @File:       |   deal_data.py 
# @Date:       |   2020/9/3 10:46
# @Author:     |   ThinkPad
# @Desc:       |
import warnings
import pandas as pd
from datetime import datetime
from openpyxl import load_workbook

warnings.filterwarnings('ignore')


def saveExcel(df_list, pth, sheet_name, save_type=0):
    '''
    excel存储：存储多个df数据到excel文件中
    @param df_list:df列表
    @param pth:生成地址
    @param sheet_name:表名称
    @param save_type:存储类型
    @return:
    '''
    writer = pd.ExcelWriter(pth, engine='openpyxl')
    book = load_workbook(pth)
    writer.book = book
    cnt = 0
    for df in df_list:
        if 0 == save_type:
            df.to_excel(writer, startrow=cnt, sheet_name=sheet_name, header=None)
        elif 1 == save_type:
            df.to_excel(writer, startrow=cnt, sheet_name=sheet_name, index=False)
        cnt = cnt + df.shape[0] + 2
    writer.save()


def deal_data():
    '''
    处理数据文件
    @return:
    '''
    source_file_list = ['8月搞笑&网红达人拉新', '8月搞笑拉新', '9月时尚拉新进度表',
                        '9月汽车拉新进度表', '9月游戏拉新进度表', '9月音乐拉新进度表',
                        'VLOG拉新', '拉新一号分部', '拉新二号分部', '拉新三号分部']
    df_list = []
    name_list = []
    sheet_name_list_t = []
    for source_file in source_file_list:
        df = pd.ExcelFile('./data_source/{}.xlsx'.format(source_file))
        sheet_name_list = df.sheet_names
        name_list.extend(sheet_name_list)
        sheet_name_list_t = []
        for name in name_list:
            if name not in sheet_name_list_t:
                if '数据监控' not in name and '入驻' not in name and '线索' not in name and '发文' not in name and '未断更老作者' not in name:
                    sheet_name_list_t.append(name)
    for source_file in source_file_list:
        data_df = pd.ExcelFile('./data_source/{}.xlsx'.format(source_file))
        every_df_sheet = data_df.sheet_names
        for sheet in every_df_sheet:
            if sheet in sheet_name_list_t:
                data_df = pd.read_excel('./data_source/{}.xlsx'.format(source_file), sheet_name=sheet, index_col=0)
                if not data_df.empty:
                    check_df = data_df[data_df['作者拉新状态'].isin(['已发文', '已激活', '已入驻'])]
                    if not check_df.empty:
                        print('文件={}，sheet={}数据提取完成'.format(source_file, sheet))
                        check_df['Name'] = sheet
                        check_df['文件名'] = source_file
                        check_df.columns = [str(x) for x in check_df.columns.tolist()]
                        check_df = check_df.loc[:, ~check_df.columns.str.contains('^Unnamed')]
                        df_list.append(check_df)
                    else:
                        print('文件={}，sheet={}中没有筛选出符合数据'.format(source_file, sheet))
    if df_list:
        time = datetime.strftime(datetime.now(), '%Y-%m-%d%H%M%S')
        file_name = './export_data/resultsDdf' + time + '.xlsx'
        print(file_name)
        # 生成空文件
        pd.DataFrame().to_excel(file_name, index=False, encoding='utf-8-sig', sheet_name='结果')
        saveExcel(df_list, file_name, '结果', 1)


if __name__ == '__main__':
    deal_data()

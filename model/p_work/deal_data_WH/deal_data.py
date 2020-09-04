# -*- coding: utf-8 -*-
# @File:       |   deal_data.py 
# @Date:       |   2020/9/3 10:46
# @Author:     |   ThinkPad
# @Desc:       |
import warnings
import pandas as pd
from datetime import datetime

warnings.filterwarnings('ignore')


def deal_data():
    '''
    处理数据文件
    @return:
    '''
    source_file = '8月搞笑&网红达人拉新'
    df = pd.ExcelFile('./data_source/{}.xlsx'.format(source_file))
    sheet_name_list = df.sheet_names
    input_names = input('请输入对应的sheet名称，多个sheet请用，隔开：')
    need_sheets = input_names.split(',')
    print('输入的参数为：{}'.format(need_sheets))
    if need_sheets:
        pass
    else:
        need_sheets = input_names.split('，')
    if need_sheets:
        df_list = []
        for sheet in need_sheets:
            if sheet in sheet_name_list:

                data_df = pd.read_excel('./data_source/{}.xlsx'.format(source_file), sheet_name=sheet)
                check_df = data_df[data_df['作者拉新状态'].isin(['已发文', '已激活', '已入驻'])]
                if not check_df.empty:
                    print('sheet={}数据提取完成'.format(sheet))
                    check_df['Name'] = sheet
                    df_list.append(check_df)
                else:
                    print('sheet={}中没有筛选出符合数据'.format(sheet))
            else:
                print('sheet={}没有在该excel文件中'.format(sheet))
        if df_list:
            results_df = pd.concat(df_list, axis=0)

            time = datetime.strftime(datetime.now(), '%Y-%m-%d%H%M%S')
            file_name = './export_data/resultsDdf' + time+'.xlsx'
            print(file_name)
            results_df.to_excel(file_name, index=False,encoding='utf-8-sig')
    else:
        print('输入逗号统一用英文格式或者中文格式')


if __name__ == '__main__':
    deal_data()

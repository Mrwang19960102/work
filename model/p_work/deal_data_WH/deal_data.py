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
    for source_file in source_file_list:
        df = pd.ExcelFile('./data_source/{}.xlsx'.format(source_file))
        sheet_name_list = df.sheet_names
        for sheet in sheet_name_list:
            if sheet in all_name_sheet:
                data_df = pd.read_excel('./data_source/{}.xlsx'.format(source_file), sheet_name=sheet, index_col=0)
                check_df = data_df[data_df['作者拉新状态'].isin(['已发文', '已激活', '已入驻'])]
                if not check_df.empty:
                    print('文件={}，sheet={}数据提取完成'.format(source_file, sheet))
                    check_df['Name'] = sheet
                    check_df['文件名'] = source_file
                    check_df.columns = [str(x) for x in check_df.columns.tolist()]
                    print(check_df.columns)
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
    all_name_sheet = ['谢普庆', '韦彩花', '魏鹭饶', '笑笑', '邹佳益', '黄潇逸', '韩清华', '朱晨婧', '张清倪', '徐安琪', '宋雨欣', '齐聪艺', '徐庆洛', '苏欢',
                      '金梦暄', '高洁', '王欣雨', '陈珊', '张晓菁', '许安然', '聂云', '宋泽矩', '刘研', '李雨忻', '乌云其木格', '汪欣', '刘婷', '徐雅芳',
                      '林依玫', '黄诗雨', '洪惠琪', '徐鑫', '刘欣', '刘俏', '李梓萌', '林湘凝', '刘倩', '胡雨涵', '张锦娉', '郑淇丹', '祝琦', '岳璐', '沈泽轩',
                      '邓钥衡', '刘超', '周小洲', '陈洁', '黄成妍', '俞佳琦', '郑鑫']
    deal_data()

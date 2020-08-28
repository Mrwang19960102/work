# -*- coding: utf-8 -*-
# @File:       |   tools.py 
# @Date:       |   2020/8/28 14:33
# @Author:     |   ThinkPad
# @Desc:       |  爬虫工具软件
import base64
import re
import pandas as pd
from io import BytesIO
from fontTools.ttLib import TTFont


def get_page_show_ret(mystr, bs64_str):
    '''
    :param mystr: 要转码的字符串
    :param bs64_str:  转码格式
    :return: 转码后的字符串
    '''
    font = TTFont(BytesIO(base64.decodebytes(bs64_str.encode())))
    c = font['cmap'].tables[0].ttFont.tables['cmap'].tables[0].cmap
    ret_list = []
    for char in mystr:
        decode_num = ord(char)
        if decode_num in c:
            num = c[decode_num]
            num = int(num[-2:]) - 1
            ret_list.append(num)
        else:
            ret_list.append(char)
    ret_str_show = ''
    for num in ret_list:
        ret_str_show += str(num)
    return ret_str_show


def deal_data():
    '''
    处理数据文件
    :return:
    '''
    df_list = []
    for i in range(1, 51):
        df = pd.read_excel('./data_source/第{}页.xlsx'.format(i))
        df_list.append(df)
    data_df = pd.concat(df_list, axis=0)
    data_df.to_excel('./武汉市租房部分数据.xlsx',index=False)
    print(data_df)



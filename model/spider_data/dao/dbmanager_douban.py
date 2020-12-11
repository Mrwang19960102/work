# -*- coding: utf-8 -*-
# @File:       |   dbmanager_douban.py 
# @Date:       |   2020/12/10 13:03
# @Author:     |   ThinkPad
# @Desc:       |  
import pandas as pd
import numpy as np
from datetime import datetime
from model.spider_data import conf
from model.spider_data.dao import dbhandler


def get_book_already():
    '''
    获取已经爬取过的数据url
    @return:
    '''
    df = pd.DataFrame()
    table_name = conf.douban_book_table
    sql = '''SELECT DISTINCT url FROM {}'''.format(table_name)
    res = dbhandler.get_date(sql, table_name)
    if res:
        df = pd.DataFrame(list(res), columns=['url'])
    return df


def save_douban_book(data_df):
    '''
    数据存储
    @param save_df:
    @return:
    '''

    if data_df.empty:
        print('plz check data')
        return False
    table_name = conf.douban_book_table
    data_df = data_df.where(data_df.notnull(), None)
    data_df['cal_time'] = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    all_data = np.array(data_df).tolist()
    sql = dbhandler.con_insert_sql(data_df, table_name)
    in_bo = dbhandler.inser_many_date(sql, table_name, all_data)
    return in_bo


def get_data():
    '''

    @return:
    '''
    sql = '''SELECT url,book_name,book_author,book_isdn,score,com_num from douban_book;'''
    res = dbhandler.get_date(sql, conf.douban_book_table)
    pd.DataFrame(list(res), columns=['url', 'book_name', 'book_author', 'book_isdn', 'score', 'com_num']).to_excel(
        './豆瓣书籍数据.xlsx', index=False)




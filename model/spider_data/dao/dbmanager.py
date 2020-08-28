# -*- coding: utf-8 -*-
# @File:       |   dbmanager.py 
# @Date:       |   2020/7/20 10:04
# @Author:     |   ThinkPad
# @Desc:       |

import pandas as pd
import numpy as np
from datetime import datetime
from model.spider_data import conf
from model.spider_data.dao import dbhandler


def con_insert_sql(df, table_name):
    '''

    :param df:
    :param table_name:
    :return:
    '''
    columns = list(df.columns)
    columns_param = ','.join(columns)
    values_param = ','.join(['%s'] * len(columns))
    sql = '''insert into {} ({}) values ({})'''.format(table_name, columns_param, values_param)
    return sql


def save_qiye_info(data_df):
    table_name = conf.qiye_info_table
    data_df = data_df.where(data_df.notnull(), None)
    all_data = np.array(data_df).tolist()
    sql = con_insert_sql(data_df, table_name)
    in_bo = dbhandler.inser_many_date(sql, table_name, all_data)
    print(in_bo)


def check_data():
    '''
    数据检查
    :return:
    '''
    data_df = pd.DataFrame()
    info_df = pd.DataFrame()
    table_info = conf.qiye_info_table
    table_data = conf.qiye_data_table
    need_url = []
    sql_info = '''SELECT DISTINCT url FROM {} '''.format(table_info)
    sql_data = '''SELECT DISTINCT url FROM {}  where url is not null '''.format(table_data)
    res_info = dbhandler.get_date(sql_info, table_info)
    res_data = dbhandler.get_date(sql_data, table_data)
    if res_info:
        info_df = pd.DataFrame(list(res_info), columns=['url'])
        info_df['url'] = info_df['url'].apply(str)
    if res_data:
        data_df = pd.DataFrame(list(res_data), columns=['url'])
        data_df['url'] = data_df['url'].apply(str)
    print(len(list(data_df['url'])))
    for url in list(data_df['url']):
        if url not in list(info_df['url']):
            need_url.append(url)
    print(need_url)
    print(len(need_url))
    sql = '''update {} set status=0 where url in {}'''.format(table_data, tuple(need_url))
    up_bo = dbhandler.exec_sql(sql, table_data)
    print(up_bo)


def update_data(save_df):
    table_name = conf.qiye_data_table

    if not save_df.empty:
        url_list = list(save_df['url'])
        if len(url_list) == 1:
            print(url_list)
            sql = '''update {} set status=1 where url ='{}' '''.format(table_name, url_list[0])
            print(sql)
        else:
            sql = '''update {} set status=1 where url in {}'''.format(table_name, tuple(url_list))
        up_bo = dbhandler.exec_sql(sql, table_name)
        print(up_bo)


def need_parsing_url():
    table_name = conf.qiye_data_table
    sql = 'select url from {} where status=0 limit 50 '.format(table_name)
    res = dbhandler.get_date(sql, table_name)
    if res:
        data_df = pd.DataFrame(list(res), columns=['url'])
        data_df['url'] = data_df['url'].apply(str)
    return data_df


def save_film_rebiews(data_df):
    '''
    存储影视评论数据
    :param data_df:
    :return:
    '''
    table_name = conf.film_reviews_table
    if data_df is None or data_df.empty:
        print('plc check data')
    data_df = data_df.where(data_df.notnull(), None)
    data_df['cal_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    all_data = np.array(data_df).tolist()
    sql = con_insert_sql(data_df, table_name)
    in_bo = dbhandler.inser_many_date(sql, table_name, all_data)
    return in_bo

# def check_data():
#     need_url = []
#     data_df = pd.DataFrame()
#     df = pd.read_excel('./df.xlsx')
#     table_data = conf.qiye_data_table
#     df['url'] = df['url'].astype(str)
#     print(len(set(df['url'])))
#     sql_data = '''SELECT DISTINCT url FROM {} '''.format(table_data)
#     res_data = dbhandler.get_date(sql_data, table_data)
#     if res_data:
#         data_df = pd.DataFrame(list(res_data), columns=['url'])
#         data_df['url'] = data_df['url'].apply(str)
#     for url in list(df['url']):
#         if url not in list(data_df['url']):
#             print(type(url), url)
#             need_url.append(url)
#     print(need_url)
#     print(len(need_url))
#     print(list(data_df['url']))


# check_data()

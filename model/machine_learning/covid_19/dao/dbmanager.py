# -*- coding: utf-8 -*-
# @File:       |   dbmanager.py 
# @Date:       |   2020/7/20 10:04
# @Author:     |   ThinkPad
# @Desc:       |

import pandas as pd
import numpy as np
from model.machine_learning.covid_19 import conf
from model.machine_learning.covid_19.dao import dbhandler


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


def get_data_all(countryCode):
    '''
    获取countryCode国家疫情的全部数据
    :param countryCode:国家代码
    :return:
    '''
    data_df = pd.DataFrame()
    table = conf.covid_19_table
    sql = '''SELECT date,sum(cured),sum(dead),sum(suspected),sum(confirmed) FROM {} 
    where countryCode='{}' GROUP BY date ORDER BY date;'''.format(table, countryCode)
    results = dbhandler.get_date(sql, table)
    if results:
        data_df = pd.DataFrame(list(results), columns=['date', 'cured', 'dead', 'suspected', 'confirmed'])
    return data_df


def need_parsing_url():
    table_name = conf.qiye_data_table
    sql = 'select url from {} where status=0 limit 50 '.format(table_name)
    res = dbhandler.get_date(sql, table_name)
    if res:
        data_df = pd.DataFrame(list(res), columns=['url'])
        data_df['url'] = data_df['url'].apply(str)
    return data_df


def save_data():
    table_name = conf.qiye_data_table
    df = pd.read_excel('./df.xlsx')
    df['url'] = df['url'].apply(str)
    print(df)
    all_data = np.array(df).tolist()
    sql = con_insert_sql(df, table_name)
    in_bo = dbhandler.inser_many_date(sql, table_name, all_data)
    print(in_bo)


def save_qiye_info(data_df):
    table_name = conf.qiye_info_table
    all_data = np.array(data_df).tolist()
    sql = con_insert_sql(data_df, table_name)
    in_bo = dbhandler.inser_many_date(sql, table_name, all_data)
    print(in_bo)




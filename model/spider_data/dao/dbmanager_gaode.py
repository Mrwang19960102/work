# -*- coding: utf-8 -*-
# @File:       |   dbmanager_gaode.py
# @Date:       |   2020/10/26 16:29
# @Author:     |   ThinkPad
# @Desc:       |  
import pandas as pd
import numpy as np
from datetime import datetime
from model.spider_data import conf
from model.spider_data.dao import dbhandler


def get_need_city():
    '''
    获取需要的城市
    @return:
    '''
    df = pd.DataFrame()
    table_name = conf.area_division_table
    sql = '''SELECT DISTINCT prov_name,coun_name FROM {} where prov_name in ('福建省','广西壮族自治区') order by prov_name'''.format(
        table_name)
    res = dbhandler.get_date(sql, table_name)
    print(res)
    if res:
        df = pd.DataFrame(list(res), columns=['prov_name', 'city_name'])
    return df


def al_prov_city():
    '''
    获取数据库中已经计算过的城市
    @return:
    '''
    city_list = []
    table_name = conf.gaodemap_baidu_data_table
    sql = '''SELECT DISTINCT city_name FROM {} '''.format(
        table_name)
    res = dbhandler.get_date(sql, table_name)
    print(res)
    if res:
        df = pd.DataFrame(list(res), columns=['city_name'])
        city_list = df['city_name'].tolist()
    return city_list


def save_gaode_phone_data(data_df):
    '''
    存储高德手机号数据
    @return:
    '''
    if data_df.empty:
        print('plz check data')
        return False
    table_name = conf.gaodemap_baidu_data_table
    # 删除旧数据
    data_df = data_df.where(data_df.notnull(), None)
    data_df['cal_time'] = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    all_data = np.array(data_df).tolist()
    sql = dbhandler.con_insert_sql(data_df, table_name)
    in_bo = dbhandler.inser_many_date(sql, table_name, all_data)
    return in_bo

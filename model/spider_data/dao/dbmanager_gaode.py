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


def get_need_city(pro_list):
    '''
    获取需要的城市
    @return:
    '''
    df = pd.DataFrame()
    table_name = conf.area_division_table
    if 1 == len(pro_list):
        sql = '''SELECT DISTINCT prov_code,prov_name,city_code,city_name,coun_code,coun_name FROM {} 
        where prov_name in {} order by prov_name'''.format(table_name, pro_list[0])
    else:
        sql = '''SELECT DISTINCT prov_code,prov_name,city_code,city_name,coun_code,coun_name FROM {} 
        where prov_name in {} order by prov_name'''.format(table_name, tuple(pro_list))
    res = dbhandler.get_date(sql, table_name)
    if res:
        df = pd.DataFrame(list(res), columns=['prov_code', 'prov_name', 'city_code',
                                              'city_name', 'coun_code', 'coun_name'])
    return df


def al_prov_city(s_type, pw):
    '''
    获取数据库中已经计算过的城市
    @return:
    '''
    df = pd.DataFrame()
    table_name = conf.gaodemap_baidu_data_table
    sql = '''SELECT DISTINCT coun_code,coun_name FROM {} where s_type={} and shop_type='{}' '''.format(
        table_name, s_type, pw)
    res = dbhandler.get_date(sql, table_name)
    if res:
        df = pd.DataFrame(list(res), columns=['coun_code', 'coun_name'])
    return df


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

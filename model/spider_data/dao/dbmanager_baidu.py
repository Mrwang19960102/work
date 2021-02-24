# -*- coding: utf-8 -*-
# @File:       |   dbmanager_baidu.py 
# @Date:       |   2020/10/26 16:29
# @Author:     |   ThinkPad
# @Desc:       |  
import pandas as pd
import numpy as np
from datetime import datetime
from model.spider_data import conf
from model.spider_data.dao import dbhandler


def get_info():
    '''

    @return:
    '''
    table_name = conf.dianping_new_shaosong_table
    sql = """SELECT shop_url,shop_name,city,phone,phone2 FROM {} WHERE shop_id is not null""".format(table_name)
    res = dbhandler.get_date(sql, table_name)
    if res:
        df = pd.DataFrame(list(res), columns=['url', 'shao_name', 'city', 'phone', 'phone2'])
        print(df)


def save_baidu_phone(data_df, pw, s_type):
    '''
    存储百度手机号数据
    @return:
    '''
    in_bo = False
    if data_df.empty:
        print('plz check data')
        return False
    table_name = conf.gaodemap_baidu_data_table
    city_code = data_df['city_code'].tolist()[0]
    town_code = data_df['coun_code'].tolist()[0]
    # 删除旧数据
    sql = '''delete from {} where city_code='{}' and 
    coun_code='{}' and shop_type='{}' and s_type={} '''.format(table_name, city_code, town_code, pw, s_type)
    del_bo = dbhandler.exec_sql(sql, table_name)
    if del_bo:
        data_df = data_df.where(data_df.notnull(), None)
        data_df['cal_time'] = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        all_data = np.array(data_df).tolist()
        sql = dbhandler.con_insert_sql(data_df, table_name)
        in_bo = dbhandler.inser_many_date(sql, table_name, all_data)
    return in_bo


def already_area(pw):
    '''
    获取结果表中已经计算过的区域
    @return:
    '''
    data_df = pd.DataFrame()
    table_name = conf.map_baidu_data_table
    sql = '''SELECT DISTINCT coun_code,coun_name FROM {} where shop_type='{}' '''.format(table_name, pw)
    results = dbhandler.get_date(sql, table_name)
    if results:
        data_df = pd.DataFrame(list(results), columns=['coun_code', 'coun_name'])

    return data_df


def get_map_data():
    '''
    获取百度地图中的数据
    @return:
    '''
    data_df = pd.DataFrame()
    table_name = conf.map_baidu_data_table
    sql = '''
    SELECT DISTINCT shop_name,address,prov_name,city_name,phone
    FROM {}
    WHERE LENGTH(phone) IN (11, 23, 25,26,34,35,36,37,38,39,41,47,50,51,53,56,68,87)
    ORDER BY city_name'''.format(table_name)
    results = dbhandler.get_date(sql, table_name)
    if results:
        columns = ['shopName', 'address', 'provName', 'cityName', 'phone']
        data_df = pd.DataFrame(list(results), columns=columns)
    return data_df


def save_dzdp_phone_data(data_df):
    '''
    存储百度手机号数据
    @return:
    '''
    in_bo = False
    if data_df.empty:
        print('plz check data')
        return False
    table_name = conf.dzdp_shop_phone_table
    # 删除旧数据
    data_df = data_df.where(data_df.notnull(), None)
    data_df['cal_time'] = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    all_data = np.array(data_df).tolist()
    sql = dbhandler.con_insert_sql(data_df, table_name)
    in_bo = dbhandler.inser_many_date(sql, table_name, all_data)
    return in_bo

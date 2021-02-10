# -*- coding: utf-8 -*-
# @File:       |   dbmanager_dzdp.py 
# @Date:       |   2020/11/2 11:31
# @Author:     |   ThinkPad
# @Desc:       |  
import pandas as pd
import numpy as np
from datetime import datetime
from model.spider_data import conf
from model.spider_data.dao import dbhandler


def already_shop_phone(pw):
    '''
    获取以及计算获取过手机号的店铺
    @return:
    '''
    url_list = []
    table_name = conf.dzdp_shop_phone_table
    sql = '''
        SELECT DISTINCT(url) from {} where shop_type='{}' '''.format(table_name, pw)
    res = dbhandler.get_date(sql, table_name)
    if res:
        url_df = pd.DataFrame(list(res), columns=['url'])
        url_list = url_df['url'].tolist()
    return url_list


def all_shop_phone(pw):
    '''
    获取全部店铺的url
    @return:
    '''
    df = pd.DataFrame()
    table_name = conf.dzdp_shop_table
    sql = '''SELECT DISTINCT shop_name,url,city from {} where shop_type='{}' '''.format(table_name, pw)
    res = dbhandler.get_date(sql, table_name)
    if res:
        df = pd.DataFrame(list(res), columns=['shop_name', 'url', 'city'])
    return df


def save_dzdp_phone_data(data_df):
    '''
    存储百度手机号数据
    @return:
    '''
    in_bo = False
    if data_df.empty:
        print('plz check data')
        return in_bo
    table_name = conf.dzdp_shop_phone_table
    # 删除旧数据
    data_df = data_df.where(data_df.notnull(), None)
    data_df['cal_time'] = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    all_data = np.array(data_df).tolist()
    sql = dbhandler.con_insert_sql(data_df, table_name)
    in_bo = dbhandler.inser_many_date(sql, table_name, all_data)
    return in_bo


def save_dzdp_shoplist(data_df, select_method):
    '''
    存储大众点评店铺列表数据
    @return:
    '''
    in_bo = False
    if data_df.empty:
        print('plz check data')
        return False
    table_name = conf.dzdp_shop_table
    # 删除旧数据
    # if 1 == select_method:
    #     region = data_df['region'].tolist()[0]
    #     if 1 < len(data_df):
    #         del_sql = '''delete from {}
    #         where url in {} and region='{}' '''.format(table_name,
    #                                                    tuple(data_df['url'].tolist()),
    #                                                    region)
    #     else:
    #         del_sql = '''delete from {}
    #         where url = '{}' and region='{}' '''.format(table_name,
    #                                                     data_df['url'].tolist()[0],
    #                                                     region)
    # elif 0 == select_method:
    #     small_type = data_df['small_type'].tolist()[0]
    #     if 1 < len(data_df):
    #         del_sql = '''delete from {}
    #         where url in {} and small_type='{}' '''.format(table_name,
    #                                                        tuple(data_df['url'].tolist()),
    #                                                        small_type)
    #     else:
    #         del_sql = '''delete from {}
    #         where url = '{}' and small_type='{}' '''.format(table_name,
    #                                                         tuple(data_df['url'].tolist()),
    #                                                         small_type)
    # else:
    #     pass
    shop_id_list = data_df['shop_id'].tolist()
    del_sql = '''delete from {} where shop_id in {} '''.format(table_name, tuple(shop_id_list))
    del_bo = dbhandler.exec_sql(del_sql, table_name)
    if del_bo:
        data_df = data_df.where(data_df.notnull(), None)
        data_df['cal_time'] = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        all_data = np.array(data_df).tolist()
        sql = dbhandler.con_insert_sql(data_df, table_name)
        in_bo = dbhandler.inser_many_date(sql, table_name, all_data)
    return in_bo


def get_cities():
    '''
    获取数据库中所有的城市
    @return:
    '''
    city_list = []
    table_name = conf.area_division_table
    sql = '''select distinct city_name from {}'''.format(table_name)
    res = dbhandler.get_date(sql, conf.area_division_table)
    if res:
        df = pd.DataFrame(list(res), columns=['city_name'])
        city_list = df['city_name'].tolist()
    return city_list


def already_cityArea(city_name):
    '''
    获取该城市已经采集过数据的行政区
    @param city_name: 城市名称
    @return:
    '''
    city_area_df = pd.DataFrame()
    tableName = conf.dzdp_shop_table
    sql = '''select distinct city,region from {} where city ='{}' '''.format(tableName, city_name)
    res = dbhandler.get_date(sql, tableName)
    if res:
        city_area_df = pd.DataFrame(list(res), columns=['city_name', 'area_name'])

    return city_area_df


def get_needshop_info():
    '''
    获取已经采集过的商铺手机号信息
    @return:
    '''
    dataDf = pd.DataFrame()
    tableName = conf.dzdp_shop_phone_table
    sql = '''select DISTINCT a.shop_name,a.shop_id,a.url from {} a where a.shop_id not in (SELECT DISTINCT shop_id from {})'''.format(
        conf.dzdp_shop_table, tableName)
    print(sql)
    res = dbhandler.get_date(sql, tableName)
    if res:
        dataDf = pd.DataFrame(list(res), columns=['shop_name', 'shop_id', 'url'])
        dataDf['shop_id'] = dataDf['shop_id'].astype(str)
    return dataDf


def get_needshop_info2():
    '''
    获取已经采集过的商铺手机号信息
    @return:
    '''
    dataDf = pd.DataFrame()
    tableName = conf.dzdp_shop_phone_table
    sql = '''select DISTINCT a.shop_name,a.city,a.region,a.shop_id,a.url from {} a where a.shop_id not in (SELECT DISTINCT shop_id from {})'''.format(
        conf.dzdp_shop_table, tableName)
    print(sql)
    res = dbhandler.get_date(sql, tableName)
    if res:
        dataDf = pd.DataFrame(list(res), columns=['shop_name', 'city', 'region', 'shop_id', 'url'])
        dataDf['shop_id'] = dataDf['shop_id'].astype(str)
    return dataDf


def get_all_shop():
    '''
    获取商铺列表中的所有商铺
    @return:
    '''
    dataDf = pd.DataFrame()
    tablaName = conf.dzdp_shop_table
    sql = '''select DISTINCT shop_name,shop_id,url from {} '''.format(tablaName)
    res = dbhandler.get_date(sql, tablaName)
    if res:
        dataDf = pd.DataFrame(list(res), columns=['shop_name', 'shop_id', 'url'])
        dataDf['shop_id'] = dataDf['shop_id'].astype(str)
    return dataDf


def get_pro_city(pro_name):
    '''
    获取省份的城市信息
    @param pro_name: 省份名称
    @return:
    '''
    dataDf = pd.DataFrame()
    table_name = conf.area_division_table
    sql = '''SELECT DISTINCT prov_name,city_name from {} WHERE prov_name='{}' '''.format(table_name, pro_name)
    res = dbhandler.get_date(sql, table_name)
    if res:
        dataDf = pd.DataFrame(list(res), columns=['pro_name', 'city_name'])
        dataDf['city_name'] = dataDf['city_name'].apply(lambda x: x.replace('市', ''))
    return dataDf

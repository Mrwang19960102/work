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
        return False
    table_name = conf.dzdp_shop_phone_table
    # 删除旧数据
    data_df = data_df.where(data_df.notnull(), None)
    data_df['cal_time'] = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    all_data = np.array(data_df).tolist()
    sql = dbhandler.con_insert_sql(data_df, table_name)
    in_bo = dbhandler.inser_many_date(sql, table_name, all_data)
    return in_bo

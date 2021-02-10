# -*- coding: utf-8 -*-
# @File:       |   dbmanager.py 
# @Date:       |   2021/1/22 23:58
# @Author:     |   ThinkPad
# @Desc:       |  数据库操作


import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from model.pratice.warehouse import conf
from model.pratice.warehouse.dao import dbhandler


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


def get_return_data_day(cal_date):
    '''
    获取数据库中当天的退货数量
    @param cal_date: 计算时间
    @return:
    '''
    df = pd.DataFrame()
    table_name = conf.return_data_table
    sql = '''SELECT date,SKU,bin_no,qty from {} where date='{}' '''.format(table_name, cal_date)
    res = dbhandler.get_date(sql, table_name)
    if res:
        df = pd.DataFrame(list(res), columns=['date', 'sku', 'bin_no', 'qty'])
    return df


def get_inventory_data(cal_data):
    '''
    获取计算时间前一天的库存数据
    @param cal_data:
    @return:
    '''
    df = pd.DataFrame()
    table_name = conf.inventory_data_table
    # 计算时间的上一天
    cal_date_l = datetime.strftime(datetime.strptime(cal_data, '%Y-%m-%d') + timedelta(days=-1), '%Y-%m-%d')
    print(cal_date_l)
    sql = '''SELECT date,sku,bin_no,qty FROM {} where date ='{}' '''.format(table_name, cal_date_l)
    res = dbhandler.get_date(sql, table_name)
    if res:
        df = pd.DataFrame(list(res), columns=['date', 'sku', 'bin_no', 'qty'])
        df['date'] = df['date'].apply(lambda x: datetime.strftime(x, '%Y-%m-%d'))
    return df


def get_sale_data_day(cal_date):
    '''
    获取计算时间当天要发出去的商品数据
    @param cal_date: 计算时间
    @return:
    '''
    dataDf = pd.DataFrame()
    table_name = conf.sale_data_table
    sql = '''SELECT date,order_num,sku,qty,order_type from {} where date ='{}' '''.format(table_name, cal_date)
    res = dbhandler.get_date(sql, table_name)
    if res:
        dataDf = pd.DataFrame(list(res), columns=['date', 'order_num', 'sku', 'qty', 'order_type'])

    return dataDf


def save_inventory_data(data_df):
    '''
    存储库存数据
    @param data_df: 要存储的数据
    @return:
    '''
    table_name = conf.inventory_data_table
    if data_df is None or data_df.empty:
        print('plc check data')
    data_df = data_df.where(data_df.notnull(), None)
    all_data = np.array(data_df).tolist()
    sql = con_insert_sql(data_df, table_name)
    in_bo = dbhandler.inser_many_date(sql, table_name, all_data)
    return in_bo


def save_defore_sale_data(save_df):
    '''
    存储没有计算时间没有发货前的库存
    @param save_df:
    @return:
    '''
    table_name = conf.before_sale_data_table
    if save_df is None or save_df.empty:
        print('plc check data')
    del_sql = '''delete from {} where date ='{}' '''.format(table_name, save_df['date'].tolist()[0])
    del_bo = dbhandler.exec_sql(del_sql, table_name)
    data_df = save_df.where(save_df.notnull(), None)
    all_data = np.array(data_df).tolist()
    sql = con_insert_sql(data_df, table_name)
    in_bo = dbhandler.inser_many_date(sql, table_name, all_data)
    return in_bo


def sale_data(cal_date, inventoryDf_before_sale):
    '''
    根据当天要发出去的商品 然后更新库存数据
    @param cal_date: 计算时间
    @param inventoryDf_before_sale:
    @return:
    '''
    table_name = conf.before_sale_data_table
    # 获取计算时间当天要发出去的数据
    saleDf = get_sale_data_day(cal_date)
    if not saleDf.empty:
        # 遍历每一个要卖出去的商品  在inventoryDf_before_sale寻找，然后做减法
        for index, info in saleDf.iterrows():
            order_num = info['order_num']
            sku = info['sku']
            qty = info['qty']
            order_type = info['order_type']
            print(sku)
            if sku in inventoryDf_before_sale['sku'].tolist():
                select_sql = '''select qty,bin_no from {} where date ='{}' and sku='{}' limit 1 '''.format(table_name,
                                                                                                           cal_date,
                                                                                                           sku)
                res = dbhandler.get_date(select_sql, table_name)
                if res:
                    value = res[0][0]
                    bin = res[0][1]
                    # 如果数据库的库存小于要发货的数量
                    while value < qty:
                        update_sql = '''update {} set qty='{}' where date ='{}' and sku='{}' and bin_no='{}' '''.format(
                            table_name, 0, cal_date, sku, bin)
                        update_bo = dbhandler.exec_sql(update_sql, table_name)
                        # 还需要从别的箱子中去发货
                        value = qty - value



            else:
                # 说明不存在
                print('sku={}没有库存'.format(sku))

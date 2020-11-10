# -*- coding: utf-8 -*-
# @File:       |   dbmanger_maoyan.py 
# @Date:       |   2020/11/10 16:08
# @Author:     |   ThinkPad
# @Desc:       |  
import pandas as pd
import numpy as np
from datetime import datetime
from model.spider_data import conf
from model.spider_data.dao import dbhandler


def save_maoyan_movie(data_df):
    '''
    存储猫眼电影数据  名称 url 评分
    @param data_df: 要存储的数据
    @return:
    '''
    if data_df.empty:
        print('plz check data')
        return False
    table_name = conf.maoyan_movie_table
    del_sql = '''delete from {} where url in {}'''.format(table_name, tuple(data_df['url'].tolist()))
    del_bo = dbhandler.exec_sql(del_sql, table_name)
    if del_bo:
        data_df = data_df.where(data_df.notnull(), None)
        data_df['cal_time'] = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        all_data = np.array(data_df).tolist()
        sql = dbhandler.con_insert_sql(data_df, table_name)
        in_bo = dbhandler.inser_many_date(sql, table_name, all_data)
        return in_bo

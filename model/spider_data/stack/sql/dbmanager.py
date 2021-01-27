# -*- coding: utf-8 -*-
# @File:       |   dbmanager.py 
# @Date:       |   2020/7/20 10:04
# @Author:     |   ThinkPad
# @Desc:       |

import pandas as pd
import numpy as np
from datetime import datetime
from model.spider_data.stack import conf
from model.spider_data.stack.sql import dbhandler


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


def save_stack(data_df):
    inbo = False
    if data_df.empty:
        print('plz check data')
        return inbo
    table_name = conf.stack_overflow_table
    del_sql = '''delete from {} where url in {}'''.format(table_name, tuple(data_df['url'].tolist()))
    del_bo = dbhandler.exec_sql(del_sql, table_name)
    if del_bo:
        data_df = data_df.where(data_df.notnull(), None)
        data_df['cal_time'] = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        all_data = np.array(data_df).tolist()
        sql = con_insert_sql(data_df, table_name)
        inbo = dbhandler.inser_many_date(sql, table_name, all_data)
    return inbo


def save_stack_answer(data_df):
    print(data_df)
    inbo = False
    if data_df.empty:
        print('plz check data')
        return inbo
    table_name = conf.stack_answer_table
    del_sql = '''delete from {} where url in {}'''.format(table_name, tuple(data_df['url'].tolist()))
    del_bo = dbhandler.exec_sql(del_sql, table_name)
    if del_bo:
        data_df = data_df.where(data_df.notnull(), None)
        data_df['cal_time'] = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        all_data = np.array(data_df).tolist()
        sql = con_insert_sql(data_df, table_name)
        inbo = dbhandler.inser_many_date(sql, table_name, all_data)
    return inbo


def check_already(pw, page):
    '''
    检查有没有怕去过
    @return:
    '''
    table_name = conf.stack_overflow_table
    sql = '''select count(*) from {} where pw='{}' and page={} '''.format(table_name, pw, page)
    res = dbhandler.get_date(sql, table_name)
    if res:
        return True
    else:
        return False


def get_need_url(pw):
    '''
    获取需要采集的数据信息
    @return:
    '''
    dataDf = pd.DataFrame()
    table_name1 = conf.stack_overflow_table
    table_name2 = conf.stack_answer_table
    sql = '''SELECT DISTINCT a.url,a.author 
    from {} a where a.url not in (select DISTINCT url from {}) and a.answer!='0' '''.format(table_name1, table_name2)
    res = dbhandler.get_date(sql, table_name1)

    if res:
        dataDf = pd.DataFrame(list(res), columns=['url', 'author'])
    return dataDf


def get_already_pw_page(pw):
    '''
    开源中国中获取已经
    @param pw:
    @return:
    '''
    page_list = []
    table_name = conf.kaiyuan_table
    sql = '''SELECT DISTINCT pw,page FROM {} where pw='{}' '''.format(table_name, pw)
    res = dbhandler.get_date(sql, table_name)
    if res:
        df = pd.DataFrame(list(res), columns=['pw', 'page'])
        df['page'] = df['page'].astype(int)
        page_list = df['page'].tolist()

    return page_list


def get_need_url_kaiyuan(pw):
    '''
    获取需要采集的url
    @return:
    '''
    data_Df = pd.DataFrame()
    table_name1 = conf.kaiyuan_table
    table_name2 = conf.kaiyuan_info_table
    sql = '''SELECT DISTINCT a.url FROM {} a 
    where a.url not in (select DISTINCT url from {} where pw='{}') and a.pw='{}' '''.format(table_name1,
                                                                                            table_name2,
                                                                                            pw, pw)
    res = dbhandler.get_date(sql, table_name1)
    if res:
        data_Df = pd.DataFrame(list(res), columns=['url'])
    return data_Df


def save_kaiyuan(data_df, table_name=conf.kaiyuan_table):
    inbo = False
    if data_df.empty:
        print('plz check data')
        return inbo

    if len(data_df) > 1:
        del_sql = '''delete from {} where url in {}'''.format(table_name, tuple(data_df['url'].tolist()))
    else:
        del_sql = '''delete from {} where url = '{}' '''.format(table_name, data_df['url'].tolist()[0])
    del_bo = dbhandler.exec_sql(del_sql, table_name)
    if del_bo:
        data_df = data_df.where(data_df.notnull(), None)
        data_df['cal_time'] = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        all_data = np.array(data_df).tolist()
        sql = con_insert_sql(data_df, table_name)
        inbo = dbhandler.inser_many_date(sql, table_name, all_data)
    return inbo


if __name__ == '__main__':
    pw_list = ['android-os', 'php', 'mysql', 'spring',
               'jfinal', 'python', 'eclipse', 'linux', 'jquery',
               'tomcat', 'ubuntu', 'centos', 'android', 'echarts']
    for pw in pw_list:

        sql = '''select aa.url,aa.pw,aa.title,aa.author,aa.pub_date,aa.read_count,aa.col_count,aa.answer_count,bb.com_author,bb.pub_date as com_pub_date from (SELECT a.url,a.pw,a.title,b.author,b.pub_date,b.read_count,b.col_count,b.answer_count FROM `kaiyuan` a LEFT JOIN kaiyuan_info b on a.url=b.url where a.pw='{}' ORDER BY pub_date) aa left join kaiyuan_comment bb on aa.url =bb.url'''.format(
            pw)
        res = dbhandler.get_date(sql, conf.kaiyuan_table)
        if res:
            df = pd.DataFrame(list(res), columns=['url',
                                                  'pw',
                                                  'title',
                                                  'author',
                                                  'pub_date',
                                                  'read_count',
                                                  'col_count',
                                                  'answer_count',
                                                  'com_author',
                                                  'com_pub_date'])
            df.to_excel('../data/{}.xlsx'.format(pw), index=False)
            print('pw={}数据生成完毕'.format(pw))

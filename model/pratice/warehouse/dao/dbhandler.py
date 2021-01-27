# -*- coding: utf-8 -*-
# @File:       |   dbhandler.py 
# @Date:       |   2020/7/20 10:04
# @Author:     |   ThinkPad
# @Desc:       |  数据库连接等操作
import time
import pymysql
from model.spider_data.conf import *

conn_src = None
conn_dest = None
table_conn = {}


def get_conn_db(db_conf):
    '''
    数据库连接
    :param db_conf:数据库参数
    :return: 数据库连接
    '''
    try:
        conn = pymysql.connect(
            host=db_conf['host'],
            port=int(db_conf['port']),
            user=db_conf['user'],
            passwd=db_conf['passwd'],
            db=db_conf['database'],
            charset=db_conf['dbchar']
        )
        print('数据库连接成功')
        return conn
    except Exception as e:
        print(e)


def close_conn():
    '''
    关闭数据库连接
    '''

    table_conn.clear()
    if conn_src != None:
        try:
            conn_src.close()
        except Exception as e:
            print(e)

    if conn_dest != None:
        try:
            conn_dest.close()
        except Exception as e:
            print(e)


def init_conn_local(db_table_conf):
    '''
    连接数据库
    :param db_table_conf:
    :return:
    '''
    a = 1
    if max_con_number >= a:
        try:
            conn = get_conn_db(db_table_conf['db_conf'])
            return conn
        except Exception as e:
            print(e)
            time.sleep(0.5)
        a += 1
    else:
        print('{} connection over upper linit,falied to get connection'.format(db_table_conf['db_type']))
        return False


def get_conn(table_name):
    '''
    根据表名获取对应的数据库连接对象
    '''
    db_conf_info = [{'db_type': 'conn_src', 'db_conf': db_src_conf, 'db_name': db_src_conf['database']},
                    {'db_type': 'conn_dest', 'db_conf': db_dest_conf, 'db_name': db_dest_conf['database']}]
    for db_conf in db_conf_info:
        conn = init_conn_local(db_conf)
        cursor = conn.cursor()
        table_sql = f"show tables from {db_conf['db_name']}"
        tableNum = cursor.execute(table_sql)
        tableList = [x[0] for x in cursor.fetchall()]
        tableList1 = [i.upper() for i in tableList]
        tableList2 = [i.lower() for i in tableList]
        if table_name in tableList1 + tableList2:
            return conn
        try:
            conn.close()
        except Exception as e:
            print(e)


def get_date(sql, table):
    '''
    sql语句查询数据
    :param sql: sql语句
    :param table: 表名
    :return:
    '''
    res = None
    conn = get_conn(table)
    try:
        if conn != None:
            cursor = conn.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            return list(results)
    except Exception as e:
        print("获取数据失败")
    return res


def inser_many_date(sql, table, vals):
    '''
    数据库中批量插入数据
    '''
    in_bo = False
    conn = get_conn(table)
    try:
        if conn != None:
            cursor = conn.cursor()
            cursor.executemany(sql, vals)
            conn.commit()
            cursor.close()
            in_bo = True
    except Exception as e:
        print("Failed:{}".format(e))
    return in_bo


def exec_sql(sql, table_name):
    '''
    执行sql语句
    :param sql:
    :param table_name:
    :return:
    '''
    bo = False
    conn = get_conn(table_name)
    try:
        if conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            bo = True
            print('更新完成')
    except Exception as e:
        print(e)
    return bo


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

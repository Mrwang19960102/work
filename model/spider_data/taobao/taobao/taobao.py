# -*- coding: utf-8 -*-
# @File:       |   taobao2.py
# @Date:       |   2020/12/26 00:11
# @Author:     |   ThinkPad
# @Desc:       |  
import re
import requests
import json
import pandas as pd
import numpy as np
from model.taobao import dbhandler, conf


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


def spider_goods(url):
    '''
    爬取淘宝页面上商品列表信息
    :param url:请求的链接
    :return:
    '''
    all_data = []
    res = requests.get(url, headers=headers)
    if 200 == res.status_code:
        res = res.content.decode()
        result = re.findall('g_page_config = (.*)}};', res)[0] + "}}"
        result_info = json.loads(result)
        if 'mods' in list(result_info.keys()):
            result_info = result_info['mods']
            if 'itemlist' in list(result_info.keys()):
                result_info = result_info['itemlist']
                if 'data' in list(result_info.keys()):
                    result_info = result_info['data']
                    if 'auctions' in list(result_info.keys()):
                        result_info = result_info['auctions']
                        for shop_info in result_info:
                            every_data = []
                            pic_url = shop_info['pic_url']
                            view_price = shop_info['view_price']
                            view_sales = shop_info['view_sales']
                            good_title = shop_info['raw_title']
                            nick = shop_info['nick']
                            item_loc = shop_info['item_loc']
                            every_data.append(pic_url)
                            every_data.append(view_price)
                            every_data.append(view_sales)
                            every_data.append(good_title)
                            every_data.append(nick)
                            every_data.append(item_loc)
                            all_data.append(every_data)
    if all_data:
        savedf = pd.DataFrame(all_data, columns=['pic_url', 'view_price', 'view_sales',
                                                 'raw_title', 'nick', 'item_loc'])
        print(savedf)

        in_bo = save_taobao_data(savedf)
        print('数据存储至：{}，状态：{}'.format(conf.taobao_data_table, in_bo))
    else:
        print('获取数据失败')


def save_taobao_data(data_df):
    '''
    存储淘宝数据
    @return:
    '''
    in_bo = False
    if data_df.empty:
        print('plz check data')
        return in_bo
    table_name = conf.taobao_data_table

    data_df = data_df.where(data_df.notnull(), None)
    all_data = np.array(data_df).tolist()
    sql = con_insert_sql(data_df, table_name)
    in_bo = dbhandler.inser_many_date(sql, table_name, all_data)
    return in_bo


if __name__ == '__main__':
    pw = '美食'
    print('开始采集淘宝网站关于{}数据'.format(pw))
    url = 'https://s.taobao.com/search?q={}&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306'.format(
        pw)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'cookie': 'tracknick=stronger%5Cu677E%5Cu677E; enc=GuMQY%2BBrRFa2uRcgjctAjguZj0Ou6D4MmRIY9JRHd%2B34ADja6QPdmokveN%2BNZwkOoeoXiLPdZO54iYSPkIWiyw%3D%3D; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; miid=424830181899844559; cna=FssiGII9L0UCAXAC862tpBHt; t=0aca7135461c1fb74bf5997d3cceed20; sgcookie=E100c%2FLb%2FqM6ke5eKA6P3BaQC0HlmLWS9Tc%2BJU5%2Fdq4I6sVKaK1MIXbgcJjua5EV%2BKdOIZJt9rXZNfhnQnc4%2F8fzjQ%3D%3D; _cc_=VT5L2FSpdA%3D%3D; _m_h5_tk=fdf6f2febac3a2eb9a8c4ad413793ccb_1608954512606; _m_h5_tk_enc=89ad9d6ebf05a6a2697878d61ae679c3; cookie2=1bb99e46a065498cc85b648b76a10813; v=0; _tb_token_=583673ae40e7b; xlly_s=1; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; JSESSIONID=E981746DD89BEE8F751DB88B3877024A; tfstk=cwVFBVttU6CFrCl5HXGyFsWa47HdaDVuG93-K8tcsCVykwHn0sAW2VDRukErD1Dh.; l=eBxb7nznOuO2otkhBO5Zlurza77TzIOf1sPzaNbMiInca6hltFNovNQ24lgpSdtjgt5AeeKPmtmRRRnw-5aLRxgKqelrgnspBL968e1..; isg=BBcXNaJWBIg60YC-yQqm7QD2pothXOu-GwB8qGlFXuZNmDPaeS0uDnr--jiGcMM2',
        'referer': 'https://www.taobao.com/'
    }
    spider_goods(url)

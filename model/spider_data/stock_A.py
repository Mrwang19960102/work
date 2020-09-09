# -*- coding: utf-8 -*-
# @File:       |   stock_A.py 
# @Date:       |   2020/9/7 9:29
# @Author:     |   ThinkPad
# @Desc:       |  爬取东方财富网站沪深A股的数据信息
import re
import time
import json
import requests
import pandas as pd
import numpy as np
from lxml import etree

headers = {
    'Referer': 'http://quote.eastmoney.com/center/gridlist.html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}


def spiderstock_A(url):
    '''
    爬取沪深A股的数据信息
    @param url: 请求链接
    @return:
    '''
    res = requests.get(url, headers=headers).content.decode()
    p1 = re.compile(r'[(](.*?)[)]', re.S)
    all_data = re.findall(p1, res)
    all_data = [eval(i) for i in all_data][0]
    stock_data = all_data['data']['diff']
    print(stock_data)
    allInsert_data = []
    for everyData in stock_data:
        everyInsert = []
        stock_code = everyData['f12']
        stock_name = everyData['f14']
        latest_price = everyData['f2']
        applies = everyData['f3']
        change_amount = everyData['f4']
        # 成交量
        volume = everyData['f5']
        # 成交额
        deal_amount = everyData['f6']
        # 振幅
        amplitude = everyData['f7']
        # 最高
        highest = everyData['f15']
        # 最低
        lowest = everyData['f16']
        # 今开
        open_today = everyData['f17']
        # 昨收
        yes_close = everyData['f18']
        everyInsert.append(stock_code)
        everyInsert.append(stock_name)
        everyInsert.append(latest_price)
        everyInsert.append(applies)
        everyInsert.append(change_amount)
        everyInsert.append(volume)
        everyInsert.append(deal_amount)
        everyInsert.append(amplitude)
        everyInsert.append(highest)
        everyInsert.append(lowest)
        everyInsert.append(open_today)
        everyInsert.append(yes_close)
        allInsert_data.append(everyInsert)
        print(stock_code)
    export_data = pd.DataFrame(allInsert_data, columns=['stock_code', 'stock_name', '最新价', '涨跌幅',
                                                        '涨跌额', '成交量（手）', '成交额', '振幅',
                                                        '最高', '最低', '今开', '昨收'])
    export_data.to_excel('./data_export/沪深A股数据.xlsx', index=False, encoding='utf-8-sig')


if __name__ == '__main__':
    # url = 'http://11.push2.eastmoney.com/api/qt/clist/get?cb=jQuery11240058798207130140945_1599442261887&pn=1&pz=4500&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1599442261904'
    # spiderstock_A(url)
    a = "a"
    print(a > 'b' or 'c')

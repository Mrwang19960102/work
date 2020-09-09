# -*- coding: utf-8 -*-
# @File:       |   piluyi.py 
# @Date:       |   2020/9/7 13:16
# @Author:     |   ThinkPad
# @Desc:       |  披露易爬虫借口
import re
import os
import json
import time
import requests
from lxml import etree
import pandas as pd

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'content-length': '394',
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': 'WT_FPC=id=23.1.96.76-3007895424.30831681:lv=1599456340967:ss=1599455142650;TS016e7565=015e7ee6038106e315b577c6032a7bef79586f626e8cf9e1986852f96daca61234d94dd062935283bcbdd1d2c8cae037a18caff270',
    'origin': 'https://www.hkexnews.hk',
    'referer': 'https://www.hkexnews.hk/sdw/search/searchsdw.aspx',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}


def spider_data(need_df, trading_dt):
    '''
    爬取披露易数据
    @param url:请求链接
    @param trading_dt:交易日
    @return:
    '''
    shareholding = None
    wight = None
    # 获取数据失败的股票代码list
    stock_no = []
    url = 'https://www.hkexnews.hk/sdw/search/searchsdw.aspx'
    for index, info in need_df.iterrows():
        stock_code = info['StockCode']
        stockName = info['StockName']
        print(stock_code)
        params = {
            'txtStockCode': stock_code,
            'txtShareholdingDate': trading_dt,
            # 'txtParticipantID': 'C00100',
            '__EVENTTARGET': 'btnSearch',
        }
        try:
            res = requests.post(url, headers=headers, data=params).content.decode()
            if res:
                html = etree.HTML(res)
                # participant_ID = html.xpath('.//div[@class="table-scroller"]//table//tbody//tr//td[@class="col-participant-id"]//div[@class="mobile-list-body"]//text()')
                participant_ID = html.xpath('.//td[@class="col-participant-id"]//div[@class="mobile-list-body"]//text()')
                if participant_ID:
                    participant_ID = [x.replace('\n', '').replace('\r', '').replace(' ', '') for x in participant_ID]
                participant_name = html.xpath(
                    './/td[@class="col-participant-name"]//div[@class="mobile-list-body"]//text()')
                if participant_name:
                    participant_name = [x.replace('\n', '').replace('\r', '').replace(' ', '') for x in participant_name]
                shareholding = html.xpath(
                    './/td[@class="col-shareholding text-right"]//div[@class="mobile-list-body"]//text()')
                if shareholding:
                    shareholding = [x.replace('\n', '').replace('\r', '').replace(' ', '') for x in shareholding]
                weight = html.xpath(
                    './/td[@class="col-shareholding-percent text-right"]//div[@class="mobile-list-body"]//text()')
                if weight:
                    weight = [x.replace('\n', '').replace('\r', '').replace(' ', '') for x in weight]
                print('length={},participant_ID：{}'.format(len(participant_ID), participant_ID))
                print('length={},participant_name：{}'.format(len(participant_name), participant_name))
                print('length={},shareholding：{}'.format(len(shareholding), shareholding))
                print('length={},weight：{}'.format(len(weight), weight))
                data_df = pd.DataFrame({
                    'participant_ID': participant_ID,
                    'participant_name': participant_name[:len(participant_ID)],
                    'shareholding': shareholding[:len(participant_ID)],
                    'weight': weight[:len(participant_ID)],
                })
                data_df['stock_code'] = stock_code
                stock_code_A = re.findall(re.compile(r'[#](.*?)[)]', re.S), stockName)
                if stock_code_A:
                    stock_code_A = stock_code_A[0]
                else:
                    stock_code_A = None
                data_df['A_stock_code'] = stock_code_A
                dt = trading_dt.replace('/', '')
                data_df['trading_dt'] = dt
                data_df.to_excel('./data_export/{}股票数据_{}.xlsx'.format(stock_code, dt), index=False)
                print('*' * 50)
            else:
                stock_no.append(stock_code)
                print('The stock_code={} ,no response obtained'.format(stock_code))
            time.sleep(0.5)
        except Exception as e:
            print('The stock_code={} get data error,{}'.format(stock_code, e))
            stock_no.append(stock_code)
    if stock_no:
        stock_data_no = pd.DataFrame({
            'stock_code': stock_no
        })
        stock_data_no.to_excel('./data_export/stock_data_no.xlsx', index=False)


def check_data():
    '''
    筛选数据：筛选出需要的股票信息
    @return:
    '''
    data_df = pd.read_excel('./data_source/stock.xlsx', sheet_name='company')
    data_df = data_df[2734:]
    # data_df = data_df[2739:]
    StockName_list = list(data_df['StockName'])
    # 筛选出A股
    stockName_list = [x for x in StockName_list if '#' in x]
    need_df = data_df[data_df['StockName'].isin(stockName_list)]
    df_no = pd.read_excel('./data_export/stock_data_no.xlsx')
    need_df = need_df[need_df['StockCode'].isin(list(df_no['stock_code']))]
    # print(need_df)
    return need_df

def integration_excel_data(trading_dt):
    '''
    整合excel文件数据
    @return:
    '''
    dt = trading_dt.replace('/', '')
    path = r'D:\master\work\model\spider_data\data_export'
    file_list = []
    df_list = []
    for filename in os.listdir(path):
        if dt in filename:
            file_list.append(filename)
    print(file_list)
    for excel in file_list:
        df = pd.read_excel('./data_export/{}'.format(excel))
        df_list.append(df)
    data_df = pd.concat(df_list,axis=0)
    print(data_df)
    data_df.to_excel('./data_export/所有股票数据_{}.xlsx'.format(dt),index=False)



if __name__ == '__main__':
    # 交易日
    trading_dt = '2020/09/02'
    integration_excel_data(trading_dt)
    # need_df = check_data()
    # spider_data(need_df, trading_dt)

# -*- coding: utf-8 -*-
# @File:       |   stock_data.py 
# @Date:       |   2021/2/2 9:10
# @Author:     |   ThinkPad
# @Desc:       |  
import re
import time
import json
import requests
import pandas as pd


def get_data(year, totpage):
    '''
    数据采集
    @return:
    '''
    headers = {
        'Host': 'stockdata.stock.hexun.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    all_data = []
    for page in range(1, int(totpage) + 1):
        url = 'http://stockdata.stock.hexun.com/zrbg/data/zrbList.aspx?date={}-12-31&count=20&pname=20&titType=null&page={}&callback=hxbase_json11612227971462'.format(
            year, str(page))
        print('year={},page={},url={}'.format(year,page,url))
        try:
            res = requests.get(url, headers=headers)
            if 200 == res.status_code:
                res = res.content.decode('gbk')
                res = res.replace('hxbase_json1(', '')[:-1]
                res = res.replace('<', '').replace('>', '').replace('{Number', "{'Number'") \
                    .replace('StockNameLink', "'StockNameLink'").replace('industry:', "'industry':") \
                    .replace('stockNumber:', "'stockNumber':").replace('industryrate:', "'industryrate':") \
                    .replace('Pricelimit:', "'Pricelimit':").replace('lootingchips:', "'lootingchips':") \
                    .replace('Scramble:', "'Scramble':").replace('rscramble:', "'rscramble':") \
                    .replace('Strongstock:', "'Strongstock':").replace('Hstock:', "'Hstock':") \
                    .replace('Wstock:', "'Wstock':").replace('Tstock:', "'Tstock':").replace('Wstock:', "'Wstock':")
                info_json = eval(res)
                for k, v in info_json.items():
                    if len(str(v)) > 10:
                        stockData_list = v
                        for stock_data in stockData_list:
                            every_data = []
                            industry = stock_data['industry']
                            stockNumber = stock_data['stockNumber']
                            industryrate = stock_data['industryrate']
                            Pricelimit = stock_data['Pricelimit']
                            lootingchips = stock_data['lootingchips']
                            Scramble = stock_data['Scramble']
                            rscramble = stock_data['rscramble']
                            Strongstock = stock_data['Strongstock']
                            every_data.append(industry)
                            every_data.append(stockNumber)
                            every_data.append(industryrate)
                            every_data.append(Pricelimit)
                            every_data.append(lootingchips)
                            every_data.append(Scramble)
                            every_data.append(rscramble)
                            every_data.append(Strongstock)
                            all_data.append(every_data)
                            # print(every_data)
        except Exception as e:
            print(e)
        # time.sleep(1)
    if all_data:
        allDf = pd.DataFrame(all_data, columns=['industry', 'stockNumber', 'industryrate', 'Pricelimit', 'lootingchips',
                                                'Scramble', 'rscramble', 'Strongstock'])
        allDf.to_excel('{}数据.xlsx'.format(year), index=False)


if __name__ == '__main__':
    get_data('2019', '206')

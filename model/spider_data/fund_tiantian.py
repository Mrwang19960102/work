# -*- coding: utf-8 -*-
# @File:       |   fund_tiantian.py 
# @Date:       |   2021/1/6 13:15
# @Author:     |   ThinkPad
# @Desc:       |  天天基金数据采集
import os
import re
import time
import math
import copy
import math
import random
import requests
import pandas as pd
from lxml import etree
from snownlp import SnowNLP
from datetime import datetime
from multiprocessing import Pool
from model.spider_data import tools, conf
from model.spider_data.dao import dbmanager_dzdp


def fund_com(fund_code):
    '''
    根据基金代码 获取天天基金中有关该基金的评论
    @param fund_code:基金代码
    @return:
    '''
    url = 'http://guba.eastmoney.com/list,of{}.html'.format(fund_code)
    headers = {
        'Host': 'guba.eastmoney.com',
        'Referer': 'http://fund.eastmoney.com/161725.html?spm=search',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    print(url)
    if 200 == res.status_code:
        res = res.content.decode()
        html = etree.HTML(res)
        # 采集一共有多少条帖子
        tot_com = html.xpath('.//div[@id="articlelistnew"]/div[@class="pager"]//text()')
        tot_com = [x.replace('共有帖子数', '').replace('篇', '').replace('\r', '').replace('\n', '').replace(' ', '') for x in
                   tot_com]
        tot_com = list(filter(None, tot_com))
        if 2 == len(tot_com):
            tot_com = tot_com[1]
        elif 1 == len(tot_com):
            tot_com = tot_com[0]
        print(tot_com)
        # 根据总条数获取一共多少页数
        page_num = math.ceil(int(tot_com) / 80)
        df_list = []
        for i in range(1, 30):
            # for i in range(1, page_num + 1):
            print('一共{}页，开始采集fund_code={},第{}页数据'.format(page_num, fund_code, str(i)))
            fundCom_url = 'http://guba.eastmoney.com/list,of{}_{}.html'.format(fund_code, str(i))
            res_com = requests.get(fundCom_url, headers=headers)
            if 200 == res_com.status_code:
                res_com = res_com.content.decode()
                html_com = etree.HTML(res_com)
                # 阅读量
                reading_list = html_com.xpath(
                    './/div[@class="all fund_list"]//div[@class="articleh normal_post"]//span[1]/text()')
                # 评论数
                comNum_list = html_com.xpath(
                    './/div[@class="all fund_list"]//div[@class="articleh normal_post"]//span[2]/text()')
                # 标题
                title_list = html_com.xpath(
                    './/div[@class="all fund_list"]//div[@class="articleh normal_post"]//span[3]//a/text()')
                # 链接
                url_list = html_com.xpath(
                    './/div[@class="all fund_list"]//div[@class="articleh normal_post"]//span[3]//a/@href')
                url_list = ['http://guba.eastmoney.com' + x for x in url_list]
                # 作者
                author_list = html_com.xpath(
                    './/div[@class="all fund_list"]//div[@class="articleh normal_post"]//span[4]//a//text()')
                # 更新时间
                updatedate_list = html_com.xpath(
                    './/div[@class="all fund_list"]//div[@class="articleh normal_post"]//span[5]/text()')
                print('阅读量：长度{}，{}'.format(len(reading_list), reading_list))
                print('评论数：长度{}，{}'.format(len(comNum_list), comNum_list))
                print('标题：长度{}，{}'.format(len(title_list), title_list))
                print('链接：长度{}，{}'.format(len(url_list), url_list))
                print('作者：长度{}，{}'.format(len(author_list), author_list))
                print('更新时间：长度{}，{}'.format(len(updatedate_list), updatedate_list))

                df = pd.DataFrame({
                    '阅读量': reading_list,
                    '评论数': comNum_list,
                    '标题': title_list,
                    '链接': url_list,
                    '作者': author_list,
                    '更新时间': updatedate_list,
                })
                df['预测值'] = df['标题'].apply(lambda x: SnowNLP(x).sentiments)
                df['评价类别'] = df['预测值'].apply(lambda x: '正面' if float(x) >= 0.5 else '负面')
                df['基金代码'] = fund_code
                df = df[['基金代码', '阅读量', '评论数', '标题', '链接', '作者', '更新时间', '预测值', '评价类别']]
                df_list.append(df)
                time.sleep(2)
        if df_list:
            allDf = pd.concat(df_list)
            allDf.to_excel('基金{}评论情感分析.xlsx'.format(fund_code), index=False)


if __name__ == '__main__':
    fund_code = '009548'
    fund_com(fund_code)
    # df = pd.read_excel('./基金003834评论语义分析.xlsx')
    # df['评价类别'] = df['预测值'].apply(lambda x:'正面' if float(x)>=0.5 else '负面')
    # df.to_excel('./基金003834评论语义分析.xlsx',index=False)

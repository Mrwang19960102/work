# -*- coding: utf-8 -*-
# @File:       |   qianchengwuyou.py 
# @Date:       |   2020/10/12 9:32
# @Author:     |   ThinkPad
# @Desc:       |  前程无忧数据爬取
import re
import requests
import pandas as pd
import numpy as np
from datetime import datetime
from lxml import etree

headers = {
    'Host': 'search.51job.com',
    # 'Referer': 'https://search.51job.com/list/070200,000000,0000,00,0,99,+,2,2.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=04&jobterm=01&companysize=99&ord_field=0&dibiaoid=0&line=&welfare=',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}


def spider_info(url):
    '''
    数据爬取
    @return:
    '''
    res = requests.get(url, headers=headers).content.decode('gbk')
    html = etree.HTML(res)
    print(res)
    # print(type(res))
    # info = re.findall('window.__SEARCH_RESULT__ = >(.*)</script>', res)
    # print(info)
    info = html.xpath('.//script[3]//text()')
    print(info)


if __name__ == '__main__':
    url = 'https://search.51job.com/list/010000%252c020000,000000,0000,00,0,99,+,2,2.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=04&jobterm=01&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
    spider_info(url)

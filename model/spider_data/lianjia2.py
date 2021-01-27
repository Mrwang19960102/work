# -*- coding: utf-8 -*-
# @File:       |   lianjia.py 
# @Date:       |
# @Author:     |
# @Desc:       |  链家数据爬取：城市二手房数据
import time
import requests
import pandas as pd
import numpy as np
from lxml import etree
from bokeh.io import show
from bokeh.plotting import figure
from bs4 import BeautifulSoup


def get_areaUrl(url):
    '''
    获取各个区域的url
    @param url:
    @return: urlList
    '''
    area_df = pd.DataFrame()
    # 伪造请求头
    headers = {
        'Referer': url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    if 200 == res.status_code:
        res = res.content.decode()
        html = etree.HTML(res)
        areaUrl_list = html.xpath('.//div[@class="position"]//dl[2]//dd//div//div//a/@href')
        areaname_list = html.xpath('.//div[@class="position"]//dl[2]//dd//div//div//a/text()')
        print(areaUrl_list)
        print(areaname_list)
        area_df = pd.DataFrame({
            'url': areaUrl_list,
            'area_name': areaname_list
        })
        need_area = [x for x in areaUrl_list if 'ershoufang' in x]

        area_df = area_df[area_df['url'].isin(need_area)]
    return area_df


def house_info(url, area_name):
    '''
    获取二手房房子数据信息
    @param url: 解析的页面url
    @param area_name: 区域名称
    @return:
    '''
    # 声明变量：追加某一个区每一页的数据，数据类型为dataframe
    df_list = []
    area_df = pd.DataFrame()

    # 为了避免封ip 每个区就爬取5页
    for p in range(1, 6):
        parse_url = url + 'pg{}'.format(p)
        print('开始采集--->area={},page={},url={}'.format(area_name, p, parse_url))
        # 伪造请求头
        headers = {
            'Referer': parse_url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }
        res = requests.get(parse_url, headers=headers)
        # 利用状态码判断是不是页面响应是否正常
        if 200 == res.status_code:
            res = res.content.decode()
            soup = BeautifulSoup(res, "html.parser")
            house_name = soup.find_all('a', class_='title')
            house_name = [x.string for x in house_name]
            house_new = []
            for x in house_name:
                name = x.string
                house_new.append(name)
            community_name_list1 = soup.find_all('div', class_='positionInfo')
            community_name_list = [i.find_all('a')[0].string.strip() for i in community_name_list1]

            house_detail_list = soup.find_all('div', class_='houseInfo')
            house_detail_list = [i.get_text() for i in house_detail_list]

            totalPrice = soup.find_all('div', class_='totalPrice')
            totalPrice = [i.get_text() for i in totalPrice]

            unitPrice = soup.find_all('div', class_='unitPrice')
            unitPrice = [i.get_text() for i in unitPrice]

            print(len(house_name), house_name)
            print(len(community_name_list), community_name_list)
            print(len(house_detail_list), house_detail_list)
            print(len(totalPrice), totalPrice)
            print(len(unitPrice), unitPrice)
            every_page_df = pd.DataFrame({
                'house_name': house_name,
                'house_address': community_name_list,
                'house_info': house_detail_list,
                'house_tot': totalPrice,
                'house_unitPrice': unitPrice,
            })
            every_page_df['area'] = area_name
            df_list.append(every_page_df)
            # 每一次获取数据 要延时3秒  避免因为短时间内访问次数太多而造成封IP
            # time.sleep(3)
    if df_list:
        area_df = pd.concat(df_list)
    return area_df


def get_ershouhouse_data(url):
    '''
    获取二手房数据信息
    @return:
    '''
    # 声明变量：追加每一个区域爬取的数据
    df_list = []
    basic_url = url.split('.com/')[0]
    # 获取每个城市的各区域的url
    area_url_df = get_areaUrl(url)
    # 判断是否为空
    if not area_url_df.empty:
        # 获取每个区域的页数
        for index, info in area_url_df.iterrows():
            area_url = info['url']
            area_name = info['area_name']
            parse_url = basic_url + '.com' + area_url
            print(parse_url, area_name)
            everyDf = house_info(parse_url, area_name)
            df_list.append(everyDf)
    if df_list:
        allDf = pd.concat(df_list)

        print(allDf)
        # 生成excel数据文件
        allDf.to_excel('./二手房数据信息.xlsx', index=False)


if __name__ == '__main__':
    # 城市首字母缩写简称  例如：上海  sh;厦门  xm
    city = 'sh'
    # 链接拼接
    url = 'https://{}.lianjia.com/ershoufang/rs/'.format(city)
    # 获取二手房信息
    get_ershouhouse_data(url)

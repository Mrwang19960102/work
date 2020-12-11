# -*- coding: utf-8 -*-
# @File:       |   lianjia.py 
# @Date:       |   2020/11/18 14:28
# @Author:     |   ThinkPad
# @Desc:       |  链家数据爬取
import re
import json
import time
import requests
from datetime import datetime
import pandas as pd
import numpy as np
from lxml import etree
from model.spider_data import tools


def get_areaUrl(url):
    '''
    获取各个区域的url
    @param url:
    @return: urlList
    '''
    area_df = pd.DataFrame()
    headers = {
        'Referer': url,
        # 'Cookie': url,
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


def house_info(url, area_name, page):
    '''
    获取二手房房子数据信息
    @param url: 解析的页面url
    @param area_name: 区域名称
    @param page: 区域的数据页数
    @return:
    '''
    for p in range(1, page + 1):
        parse_url = url + 'pg{}'.format(p)
        print('开始采集--->area={},page={},url={}'.format(area_name, p, parse_url))
        headers = {
            'Referer': parse_url,
            # 'Cookie': url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }
        res = requests.get(parse_url, headers=headers)
        if 200 == res.status_code:
            res = res.content.decode()
            html = etree.HTML(res)
            house_name = html.xpath('.//div[@class="info clear"]//div[@class="title"]//a/text()')
            house_url = html.xpath('.//div[@class="info clear"]//div[@class="title"]//a/@href')
            community_name_list1 = html.xpath(
                './/div[@class="info clear"]//div[@class="flood"]//div[@class="positionInfo"]//a[1]//text()')
            community_name_list2 = html.xpath(
                './/div[@class="info clear"]//div[@class="flood"]//div[@class="positionInfo"]//a[2]//text()')
            house_detail_list = html.xpath(
                './/div[@class="info clear"]//div[@class="address"]//div[@class="houseInfo"]//text()')
            totalPrice = html.xpath('.//div[@class="totalPrice"]//span/text()')
            unitPrice = html.xpath('.//div[@class="unitPrice"]//text()')
            print(len(house_url), house_url)
            print(len(house_name), house_name)
            community_name_list = [x+' '+community_name_list2[community_name_list1.index(x)] for x in community_name_list1]
            print(len(community_name_list), community_name_list)
            print(len(house_detail_list), house_detail_list)
            print(len(totalPrice), totalPrice)
            print(len(unitPrice), unitPrice)


def get_page(url):
    '''
    获取页数
    @return:
    '''
    page_count = None
    headers = {
        'Referer': url,
        # 'Cookie': url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    if 200 == res.status_code:
        res = res.content.decode()
        html = etree.HTML(res)
        page_data = html.xpath('.//div[@class="page-box house-lst-page-box"]/@page-data')
        if page_data:
            page_count = json.loads(str(page_data[0]))['totalPage']

    return page_count


def get_ershouhouse_data(url):
    '''
    获取二手房数据信息
    @return:
    '''
    basic_url = url.split('.com/')[0]
    # 获取每个城市的各区域的url以及一共的页数
    area_url_df = get_areaUrl(url)
    if not area_url_df.empty:
        # 获取每个区域的页数
        for index, info in area_url_df.iterrows():
            area_url = info['url']
            area_name = info['area_name']
            parse_url = basic_url + '.com' + area_url
            page_count = get_page(parse_url)
            if page_count:
                print(parse_url, area_name, page_count)
                house_info(parse_url, area_name, page_count)


if __name__ == '__main__':
    city = 'sh'
    url = 'https://{}.lianjia.com/ershoufang/rs/'.format(city)

    get_ershouhouse_data(url)

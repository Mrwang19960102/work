# -*- coding: utf-8 -*-
# @File:       |   baidu_data.py 
# @Date:       |   2020/10/23 23:08
# @Author:     |   ThinkPad
# @Desc:       |    百度地图数据
import time
import re
import requests
import json
import pandas as pd
from lxml import etree
from model.spider_data.dao import dbhandler


def shops_list(parameter):
    '''
    获取商家列表（url）数据
    @return:
    '''
    headers = {
        'Referer': 'https://map.baidu.com/@13225221.26,3748918.53,12z',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }

    url = 'http://map.baidu.com/'
    htm = requests.get(url, params=parameter, headers=headers)

    htm = htm.text.encode('latin-1').decode('unicode_escape')  # 转码
    print(htm)
    pattern = r'(?<=\baddress_norm":"\[).+?(?="ty":)'
    htm = re.findall(pattern, htm)  # 按段落匹配
    for r in htm:
        pattern = r'(?<=\b"\},"name":").+?(?=")'
        name = re.findall(pattern, r)
        if not name:
            pattern = r'(?<=\b,"name":").+?(?=")'
            name = re.findall(pattern, r)
        print(name[0])  # 名称

        pattern = r'.+?(?=")'
        adr = re.findall(pattern, r)
        pattern = r'\(.+?\['
        address = re.sub(pattern, ' ', adr[0])
        pattern = r'\(.+?\]'
        address = re.sub(pattern, ' ', address)
        print(address)  # 地址

        pattern = r'(?<="phone":").+?(?=")'
        phone = re.findall(pattern, r)
        print(phone[0])


def request_hospital_data():
    ak = "kG7mgYDk9p5FX5EM3Y6yL9nK73O4lhPv"  # 换成自己的 AK，需要申请
    city = '绥中县'
    pw = '火锅'
    url = "http://api.map.baidu.com/place/v2/search?query={}&page_size=20&scope=1&region={}&output=json&ak=".format(pw,
                                                                                                                    city) + ak
    params = {'page_num': 0}  # 请求参数，页码
    request = requests.get(url, params=params)  # 请求数据
    total = json.loads(request.text)['total']  # 数据的总条数
    total_page_num = (total + 19) // 20  # 每个页面大小是20，计算总页码
    items = []  # 存放所有的记录，每一条记录是一个元素
    for i in range(total_page_num):
        params['page_num'] = i
        request = requests.get(url, params=params)
        for item in json.loads(request.text)['results']:
            if "telephone" in item:
                # telephone = item['telephone']
                name = item['name']
                telephone = item.get('telephone', '')
                # print('店名:' + name + "\t\t" + '电话：' + telephone)
            name = item['name']

            # lat = item['location']['lat']
            # lng = item['location']['lng']
            address = item.get('address', '')
            # street_id = item.get('street_id', '')
            telephone = item.get('telephone', '')
            # detail = item.get('detail', '')
            # uid = item.get('uid', '')
            print(name, address, telephone)
            new_item = (name, address, telephone)
            items.append(new_item)
        time.sleep(5)

    # 使用pandas的DataFrame对象保存二维数组
    df = pd.DataFrame(items, columns=['name', 'adderss', 'telephone'])
    df.to_excel('百度数据{}.xlsx'.format(city), header=True, index=False)


if __name__ == '__main__':
    request_hospital_data()

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
from model.spider_data.dao import dbhandler, dbmanager_baidu


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
    # ak = "0GXHE8iEvBAYcRWLNwTWZuCxHR9zpqPd"  # 换成自己的 AK，需要申请   wei
    area_df = pd.read_excel('./行政区划乡镇清单.xlsx')
    area_df = area_df[['prov_code', 'prov_name', 'city_code', 'city_name', 'coun_code', 'coun_name']]
    area_df.drop_duplicates(inplace=True)
    pw = '串串香'
    # 获取已经计算过的区域
    already_df = dbmanager_baidu.already_area(pw)
    if not already_df.empty:
        need_area_df = area_df[~area_df['coun_code'].isin(already_df['coun_code'].tolist())]
    else:
        need_area_df = area_df
    need_area_df = need_area_df[~need_area_df['prov_code'].isin(['500000', '510000'])]
    for index, info in need_area_df.iterrows():
        prov_code = info['prov_code']
        prov_name = info['prov_name']
        city_name = info['city_name']
        coun_name = info['coun_name']
        city_code = info['city_code']
        coun_code = info['coun_code']
        area = prov_name + city_name + coun_name
        print('开始采集area={}数据'.format(area))
        url = "http://api.map.baidu.com/place/v2/search?query={}&page_size=20&scope=1&region={}&output=json&ak=".format(
            pw, area) + ak
        print(url)
        # input()
        params = {'page_num': 0}  # 请求参数，页码
        request = requests.get(url, params=params)  # 请求数据
        if 200==request.status_code:
            # total = json.loads(request.text)['total']  # 数据的总条数
            print(json.loads(request.text))
            # input()
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
                # time.sleep(2)
            if items:
                # 使用pandas的DataFrame对象保存二维数组
                data_df = pd.DataFrame(items, columns=['shop_name', 'address', 'phone'])
                data_df['prov_code'] = prov_code
                data_df['prov_name'] = prov_name
                data_df['city_name'] = city_name
                data_df['coun_name'] = coun_name
                data_df['city_code'] = city_code
                data_df['coun_code'] = coun_code
                data_df['shop_type'] = pw
                # df.to_excel('百度数据{}.xlsx'.format(city), header=True, index=False)
                inbo = dbmanager_baidu.save_baidu_phone(data_df, pw)
                print('save data area={},status={}'.format(area, inbo))


if __name__ == '__main__':
    request_hospital_data()


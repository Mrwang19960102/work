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
from model.spider_data import conf
from model.spider_data.dao import dbmanager_baidu, dbmanager_gaode


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


def search_baidu_map_data(pro_list, pw_list):
    '''
    获取指定省份的数据信息
    @param pro_list:
    @return:
    '''
    ak = "kG7mgYDk9p5FX5EM3Y6yL9nK73O4lhPv"  # 换成自己的 AK，需要申请
    # ak = "0GXHE8iEvBAYcRWLNwTWZuCxHR9zpqPd"  # 换成自己的 AK，需要申请   wei
    prov_city_df = dbmanager_gaode.get_need_city(pro_list)
    for pw in pw_list:
        # 获取pw店铺类型已经计算过的城市乡镇
        al_city_coun = dbmanager_gaode.al_prov_city(2, pw)
        if not al_city_coun.empty:
            prov_city_df_new = prov_city_df.append(al_city_coun)
            prov_city_df_new = prov_city_df_new.append(al_city_coun)
            need_prov_city = prov_city_df_new.drop_duplicates(subset=['coun_code', 'coun_name'], keep=False)
        else:
            need_prov_city = prov_city_df
        print('pw={}需要采集的城镇有：'.format(pw))
        print(need_prov_city)
        for index, info in need_prov_city.iterrows():
            prov_code = info['prov_code']
            prov_name = info['prov_name']
            city_name = info['city_name']
            coun_name = info['coun_name']
            city_code = info['city_code']
            coun_code = info['coun_code']
            area = prov_name + city_name + coun_name
            print('开始采集area={}数据'.format(area))
            url = "http://api.map.baidu.com/place/v2/search?query={}&page_size=20&region={}&output=json&ak=".format(
                pw, area) + ak
            params = {'page_num': 0}  # 请求参数，页码
            request = requests.get(url, params=params)  # 请求数据
            if 200 == request.status_code:
                total = json.loads(request.text, strict=False)['total']  # 数据的总条数
                total_page_num = (total + 19) // 20  # 每个页面大小是20，计算总页码
                items = []  # 存放所有的记录，每一条记录是一个元素
                for i in range(total_page_num):
                    params['page_num'] = i
                    res = requests.get(url, params=params)
                    for item in json.loads(res.text, strict=False)['results']:
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
                    data_df['s_type'] = 2
                    inbo = dbmanager_baidu.save_baidu_phone(data_df, pw, 2)
                    print('save data area={},shape={},status={}'.format(area, data_df.shape[0], inbo))


def searchData_api_BD(pw, region):
    '''
    根据参数和行政区获取百度地图搜索参数
    @param pw:搜索参数
    @param region:行政区
    @return:
    '''
    ak = "kG7mgYDk9p5FX5EM3Y6yL9nK73O4lhPv"  # 换成自己的 AK，需要申请
    url = "http://api.map.baidu.com/place/v2/search?query={}&page_size=20&scope=1&region={}&output=json&ak=".format(
        pw, region) + ak
    print(url)
    input()
    params = {'page_num': 0}  # 请求参数，页码
    request = requests.get(url, params=params)  # 请求数据
    if 200 == request.status_code:
        # 数据的总条数
        total = json.loads(request.text)['total']
        # 每个页面大小是20，计算总页码
        total_page_num = (total + 19) // 20

        for i in range(total_page_num):
            allData_dict = {}
            allData = []
            params['page_num'] = i
            # 根据页page请求
            request = requests.get(url, params=params)
            for item in json.loads(request.text)['results']:
                # 存放所有的记录，每一条记录是一个元素
                everyDict = {}
                name = item.get('name', '')
                lat = item['location']['lat']
                lng = item['location']['lng']
                address = item.get('address', '')
                street_id = item.get('street_id', '')
                telephone = item.get('telephone', '')
                detail = item.get('detail', '')
                uid = item.get('uid', '')
                # print(name, lat, lng, street_id, address, telephone, detail, uid)
                everyDict['name'] = name
                everyDict['lat'] = lat
                everyDict['lng'] = lng
                everyDict['street_id'] = street_id
                everyDict['address'] = address
                everyDict['telephone'] = telephone
                everyDict['detail'] = detail
                everyDict['uid'] = uid
                allData.append(everyDict)
                # new_item = (name, lat, lng, street_id, address, telephone, detail, uid)
                # items.append(new_item)
            allData_dict['info'] = allData
            print(allData_dict)
            print('****************************************')


def deal_phone():
    '''
    处理手机号
    @return:
    '''
    df = pd.read_excel('./广西福建数据.xlsx')
    # df = pd.DataFrame(list(res), columns=['shop_name', 'address', 'prov_name', 'city_name', 'phone'])
    print(df)
    allData = []
    for index, info in df.iterrows():
        shop_name = info['shop_name']
        address = info['address']
        prov_name = info['prov_name']
        phone = info['phone']
        if len(phone) > 15:
            phone_list = []
            for symbol in [',', ';']:
                if symbol in phone:
                    phone_list = phone.split(symbol)
                    print(phone_list)
                    break
            for p in phone_list:
                every_data = []
                every_data.append(shop_name)
                every_data.append(address)
                every_data.append(prov_name)
                # every_data.append(coun_name)
                every_data.append(p)
                print(every_data)
                allData.append(every_data)
        else:
            every_data = []
            every_data.append(shop_name)
            every_data.append(address)
            every_data.append(prov_name)
            # every_data.append(coun_name)
            every_data.append(phone)
            print(every_data)
            allData.append(every_data)
    allDf = pd.DataFrame(allData, columns=['shop_name', 'address', 'prov_name', 'phone'])
    allDf['len'] = allDf['phone'].apply(lambda x: len(x))
    allDf = allDf[allDf['len'] == 11]
    allDf = allDf[['shop_name', 'address', 'prov_name', 'phone']]
    allDf.drop_duplicates(inplace=True)
    tel_list = []
    allData_send = []
    for i, info in allDf.iterrows():
        every_data = []
        shop_name = info['shop_name']
        address = info['address']
        prov_name = info['prov_name']
        phone = info['phone']
        if phone not in tel_list:
            every_data.append(shop_name)
            every_data.append(address)
            every_data.append(prov_name)
            every_data.append(phone)
            tel_list.append(phone)
            allData_send.append(every_data)

    if allData_send:
        send_df = pd.DataFrame(allData_send, columns=['shop_name', 'address', 'prov_name', 'phone'])
        send_df.to_excel('./222.xlsx', index=False)


def shop_phone_dzdp(shop_name, city, region):
    '''
    大众点评调用
    @param shop_name:店铺名称
    @param city: 城市名称
    @param region: 行政区
    @return:
    '''
    phone = None
    ak = "kG7mgYDk9p5FX5EM3Y6yL9nK73O4lhPv"  # 换成自己的 AK，需要申请
    url = "http://api.map.baidu.com/place/v2/search?query={}&page_size=20&scope=1&region={}&output=json&ak=".format(
        shop_name, city + region) + ak
    print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    if 200 == res.status_code:
        res = res.content.decode()
        info_json = json.loads(res)
        total = info_json['total']
        data = info_json['results']
        for every_data in data:
            name_res = every_data['name']
            city_res = every_data['city']
            area_res = every_data['area']
            if name_res == shop_name and city_res == city and area_res == region:
                if 'telephone' in list(every_data.keys()):
                    phone = every_data['telephone']
                # else:
                #     phone = '无添加'
    return phone


if __name__ == '__main__':
    pro_list = ['北京市', '江苏省', '上海市']
    pw_list = ['火锅', '烤鱼', '麻辣烫', '串串香', '小龙虾', '龙虾']
    search_baidu_map_data(pro_list, pw_list)
    deal_phone()

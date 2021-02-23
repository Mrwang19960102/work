# -*- coding: utf-8 -*-
# @File:       |   map_gaode.py 
# @Date:       |   2020/11/13 10:50
# @Author:     |   ThinkPad
# @Desc:       |
import random
import time

import requests
import json
import pandas as pd
from model.spider_data import conf
from model.spider_data.dao import dbmanager_gaode, dbhandler


def deal_phone(pro_list):
    '''
    手机号处理
    @return:
    '''
    allData = []
    allData_send = []

    sql = '''SELECT DISTINCT shop_name,address,prov_name,phone
    FROM `gaodemap_baidu_data`
    WHERE prov_name IN {}
    AND phone != '' and phone!='[]'  ORDER BY prov_name'''.format(tuple(pro_list))
    print(sql)

    res = dbhandler.get_date(sql, conf.gaodemap_baidu_data_table)
    if res:
        df = pd.DataFrame(list(res), columns=['shop_name', 'address', 'prov_name', 'phone'])
        df.drop_duplicates(inplace=True)

        for index, info in df.iterrows():
            shop_name = info['shop_name']
            address = info['address']
            prov_name = info['prov_name']
            # coun_name = info['coun_name']
            phone = info['phone']
            if len(phone) > 15:
                print(phone)
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
                    every_data.append(p)
                    print(every_data)
                    allData.append(every_data)
            else:
                every_data = []
                every_data.append(shop_name)
                every_data.append(address)
                every_data.append(prov_name)
                every_data.append(phone)
                print(every_data)
                allData.append(every_data)
        allDf = pd.DataFrame(allData, columns=['shop_name', 'address', 'prov_name', 'phone'])
        allDf['len'] = allDf['phone'].apply(lambda x: len(x))
        allDf = allDf[allDf['len'] == 11]
        allDf = allDf[['shop_name', 'address', 'prov_name', 'phone']]
        allDf.drop_duplicates(inplace=True)
        tel_list = []
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
        send_df.to_excel('./百度数据_北上江苏.xlsx', index=False)


def deal_phone2(pro_list):
    '''
    手机号处理
    @return:
    '''
    allData = []
    allData_send = []
    df1 = pd.read_excel('./百度数据_北上江苏.xlsx')
    df = pd.read_excel('./无标题.xlsx')
    df = df[['shop_name', 'city', 'phone']]
    df['address']=''
    df.drop_duplicates(inplace=True)

    for index, info in df.iterrows():
        shop_name = info['shop_name']
        address = info['address']
        prov_name = info['city']
        # coun_name = info['coun_name']
        phone = info['phone']
        if len(phone) > 15:
            print(phone)
            phone_list = []
            for symbol in [',', ';',' ']:
                if symbol in phone:
                    phone_list = phone.split(symbol)
                    print(phone_list)
                    break
            for p in phone_list:
                every_data = []
                every_data.append(shop_name)
                every_data.append(address)
                every_data.append(prov_name)
                every_data.append(p)
                print(every_data)
                allData.append(every_data)
        else:
            every_data = []
            every_data.append(shop_name)
            every_data.append(address)
            every_data.append(prov_name)
            every_data.append(phone)
            print(every_data)
            allData.append(every_data)
    allDf = pd.DataFrame(allData, columns=['shop_name', 'address', 'prov_name', 'phone'])
    allDf['len'] = allDf['phone'].apply(lambda x: len(x))
    allDf = allDf[allDf['len'] == 11]
    allDf = allDf[['shop_name', 'address', 'prov_name', 'phone']]
    allDf.drop_duplicates(inplace=True)
    tel_list = []
    for i, info in allDf.iterrows():
        every_data = []
        shop_name = info['shop_name']
        address = info['address']
        prov_name = info['prov_name']
        phone = info['phone']
        if phone not in tel_list and phone not in df1['phone'].tolist():
            every_data.append(shop_name)
            every_data.append(address)
            every_data.append(prov_name)
            every_data.append(phone)
            tel_list.append(phone)
            allData_send.append(every_data)
    if allData_send:
        send_df = pd.DataFrame(allData_send, columns=['shop_name', 'address', 'prov_name', 'phone'])
        send_df.to_excel('./百度数据_北上江苏2.xlsx', index=False)

def get_shop_info():
    prov_city_df = dbmanager_gaode.get_need_city()
    # 获取已经计算过的城市
    al_prov_city = dbmanager_gaode.al_prov_city()
    need_prov_city = prov_city_df[~prov_city_df['city_name'].isin(al_prov_city)]
    print(need_prov_city['city_name'].tolist())
    if not need_prov_city.empty:
        for index, info in need_prov_city.iterrows():
            city = info['city_name']
            prov_name = info['prov_name']
            for pw in ['火锅', '烤鱼', '麻辣烫', '串串香', '小龙虾', '龙虾']:
                for page in range(1, 50):
                    print('采集city={},pw={}数据'.format(city, pw))
                    shopName_list = []
                    shopAddress_list = []
                    shopTel_list = []
                    shopLocation_list = []
                    key = '514dff9359c2d332b294c8997ecd7719'  # peng
                    # key = 'b5c93eda62217cd84f6c4f37a4488c26'  #song
                    url = 'https://restapi.amap.com/v3/place/text?keywords={}&city={}&output=xml&offset=20&page={}&key={}&extensions=all'.format(
                        pw, city, page, key)
                    print(url)
                    params = {
                        # 'key': 'b5c93eda62217cd84f6c4f37a4488c26',
                        # 'keywords': '火锅',
                        'output': 'JSON'
                    }
                    res = requests.get(url, params=params)

                    if 200 == res.status_code:
                        res = res.content.decode()
                        json_info = json.loads(res)
                        shop_info = json_info['pois']
                        for i in range(len(shop_info)):
                            shop = shop_info[i]
                            shopName = shop['name']
                            shopAddress = shop['address']
                            shopTel = shop['tel']
                            shopLocation = shop['location']
                            shoppcode = shop['pcode']
                            shoppname = shop['pname']
                            shopcitycode = shop['citycode']
                            shocitynamep = shop['cityname']
                            shopadcode = shop['adcode']
                            shopadname = shop['adname']
                            shopName_list.append(shopName)
                            shopAddress_list.append(shopAddress)
                            shopTel_list.append(shopTel)
                            shopLocation_list.append(shopLocation)
                            # shopName = shop['name']
                    print(page, len(shopName_list), shopName_list)
                    print(page, shopAddress_list)
                    print(page, shopTel_list)
                    if shopName_list and shopAddress_list and shopTel_list:
                        df = pd.DataFrame({
                            'shop_name': shopName_list,
                            'address': shopAddress_list,
                            'phone': shopTel_list,
                        })
                        df['city_name'] = city
                        df['prov_name'] = prov_name
                        df['phone'] = df['phone'].astype(str)
                        df['prov_name'] = df['prov_name'].astype(str)
                        df['city_name'] = df['city_name'].astype(str)
                        df['address'] = df['address'].astype(str)
                        in_bo = dbmanager_gaode.save_gaode_phone_data(df)
                        print('save data to {},status={},shape={}'.format(conf.gaodemap_baidu_data_table, in_bo,
                                                                          df.shape[0]))
                    else:
                        break

if __name__ == '__main__':
    get_shop_info()
    pro_list = ['北京市','上海市','江苏省']
    deal_phone(pro_list)
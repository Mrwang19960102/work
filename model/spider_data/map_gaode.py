# -*- coding: utf-8 -*-
# @File:       |   map_gaode.py 
# @Date:       |   2020/11/13 10:50
# @Author:     |   ThinkPad
# @Desc:       |  
import requests
import json
import pandas as pd

for page in range(1, 50):
    shopName_list = []
    shopAddress_list = []
    shopTel_list = []
    shopLocation_list = []
    url = 'https://restapi.amap.com/v3/place/text?keywords=火锅&city=南京&output=xml&offset=20&page={}&key=b5c93eda62217cd84f6c4f37a4488c26&extensions=all'.format(
        page)
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
            # shopName = shop['name']
    print(page, shopName_list)
    print(page, shopAddress_list)
    print(page, shopTel_list)
    # shopName = shop_info['']

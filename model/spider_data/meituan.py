# -*- coding: utf-8 -*-
# @File:       |   meituan.py 
# @Date:       |   2020/11/11 15:49
# @Author:     |   ThinkPad
# @Desc:       |  美团网站数据
import re
import requests
import json
import pandas as pd
from lxml import etree
from model.spider_data import conf


# from model.spider_data.dao import dbmanger_maoyan

def shop_list():
    '''
    获取美团网站商铺信息
    @return:
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Cookie': '_lxsdk_cuid=1741f4185c3c8-0b60d31d052895-7a1437-100200-1741f4185c3c8; _hc.v=d73e00f0-18d2-e7d2-a6a0-7a587f93c991.1601440076; Hm_lvt_f66b37722f586a240d4621318a5a6ebe=1602841101; __utma=211559370.1161541328.1602841101.1602841101.1602841101.1; __utmz=211559370.1602841101.1.1.utmcsr=baidu|utmccn=baidu|utmcmd=organic|utmcct=zt_search; ci=55; rvct=55%2C552; uuid=f1c22b7b14b944cdabbc.1604992671.1.0.0; mtcdn=K; lt=2vGsPP1DDC_Ekkyta4jEZmiDcBgAAAAABgwAAJzmXt66rh4hqxqMabbrJ2nm3FhiSMbeOhUne989DCyMtv1uaQCSWzPI_uZw-IXQog; u=173036261; n=MrWang%E5%B0%91; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk=1741f4185c3c8-0b60d31d052895-7a1437-100200-1741f4185c3c8; unc=MrWang%E5%B0%91; __mta=49641113.1598252238998.1602841106761.1605080855186.4; client-id=e384a095-f2c5-4532-9e7a-1d014ad7ba56; firstTime=1605080878402; _lxsdk_s=175b6462ec5-a12-9a2-70d%7C%7C7'
    }
    for i in range(1, 29):
        url = 'https://nj.meituan.com/meishi/c17b273/pn{}/'.format(str(i))
        print(url)
        res = requests.get(url, headers=headers, verify=False)
        if 200 == res.status_code:
            res = str(res.content.decode())
            info = re.findall('window._appState = (.*);</script>', res)
            if info:
                info = info[0]
                json_info = json.loads(info)
                shop_info = json_info['poiLists']['poiInfos']
                shopId_list = []
                shopName_list = []
                shopScore_list = []
                shopAddress_list = []
                shopavgPrice_list = []
                for i in range(len(shop_info)):
                    shop = shop_info[i]
                    shopId = shop['poiId']
                    shopName = shop['title']
                    shopScore = shop['avgScore']
                    shopAddress = shop['address']
                    shopavgPrice = shop['avgPrice']
                    shopId_list.append(shopId)
                    shopName_list.append(shopName)
                    shopScore_list.append(shopScore)
                    shopAddress_list.append(shopAddress)
                    shopavgPrice_list.append(shopavgPrice)
                print('店铺ID', len(shopId_list), shopId_list)
                print('名称', len(shopName_list), shopName_list)
                print('评分', len(shopScore_list), shopScore_list)
                print('地址', len(shopAddress_list), shopAddress_list)
                print('均价', len(shopavgPrice_list), shopavgPrice_list)


def meituan_hotel():
    '''
    美团酒店数据
    @return:
    '''
    ...


if __name__ == '__main__':
    shop_list()

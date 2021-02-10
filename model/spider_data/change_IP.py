# -*- coding: utf-8 -*-
# @File:       |   change_IP.py 
# @Date:       |   2021/1/20 10:31
# @Author:     |   ThinkPad
# @Desc:       |  
import json
import time
import requests
import pandas as pd
from datetime import datetime


def change_ipdf():
    '''
    获取ip
    @return:
    '''
    ip_df = pd.DataFrame()
    url = 'http://napi.zhuzhaiip.com:9999/iplist?passageId=1319159857041154050&num=1&protocol=2&province=&city=&minute=30&format=2&split=&splitChar=&dedupe=1&secret=c6nxY5'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    res = res.content.decode()
    res_json = json.loads(res)
    info_list = res_json['data']
    ip_list = []
    port_list = []
    for info in info_list:
        ip_list.append(info['ip'])
        port_list.append(info['port'])

    if ip_list and port_list:
        ip_df = pd.DataFrame({
            'ip': ip_list,
            'port': port_list,
        })

    return ip_df


def change_IP(ip_df):
    '''

    @param ip_df:
    @return:
    '''
    ip_df_random = ip_df.sample(n=1)
    meta = "http://%(host)s:%(port)s" % {
        "host": ip_df_random['ip'].tolist()[0],
        "port": ip_df_random['port'].tolist()[0],
    }
    proxies = {
        "http": meta,
        "https": meta
    }
    return proxies


if __name__ == '__main__':
    ip_df = change_ipdf()
    s_time = datetime.now()
    for i in range(10000):
        program_time = datetime.now()
        if (program_time - s_time).seconds > 60 * 13:
            ip_df = change_ipdf()
            s_time = program_time
            print('重新加载')
        changeip = change_IP(ip_df)
        print(ip_df)
        print(i, changeip)
        time.sleep(2)

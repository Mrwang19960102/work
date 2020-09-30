# -*- coding: utf-8 -*-
# @File:       |   weidianhui.py 
# @Date:       |   2020/9/30 15:34
# @Author:     |   ThinkPad
# @Desc:       |   微电汇数据爬取
import time
import json
import requests
import warnings
from datetime import datetime
import pandas as pd
import numpy as np
from lxml import etree

warnings.filterwarnings('ignore')
com_headers = {
    'accept-encoding': 'gzip, deflate, br',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'cookie': 'XSRF-TOKEN=I2iWfLdqHiEuwMztMzrJ9YQfcSg8ybAAeXi7Osp1; wsid=bpehVsTXENBnOAAtJL7qq66qXhgNAoEMwyHrtBqO; sid=60005',
    'x-csrf-token': 'I2iWfLdqHiEuwMztMzrJ9YQfcSg8ybAAeXi7Osp1',
    'x-requested-with': 'XMLHttpRequest',
    'x-xsrf-token': 'I2iWfLdqHiEuwMztMzrJ9YQfcSg8ybAAeXi7Osp1',
    'accept-language': 'zh-CN,zh;q=0.9',
    'referer': 'https://ec.oneminds.cn/home/member_regimental'
}


def members_info():
    '''

    @param url: 链接
    @return:
    '''
    url = 'https://ec.oneminds.cn/home-api/memberRegimental/index?name=&mobile=&status=&pickup_type=&page=1&limit=600&order_by=&sort=&sid=60005'
    res = requests.get(url, headers=com_headers).content.decode('unicode-escape')
    # html = etree.HTML(res)

    res_list = json.loads(res)['data']
    print(res)
    print(len(res))
    all_data = []
    for i in range(0, 590):
        every_data = []
        print(i)
        res = res_list[i]
        print(res.keys())
        member_phone = res['member_phone']
        print(member_phone)
        name = res['name']
        print(name)
        mobile = res['mobile']
        print(mobile)
        store_name = res['store_name']
        print(store_name)
        add = res['addresses']
        print(add)
        created_at = res['created_at']
        print(created_at)
        pickup_type_name = res['pickup_type_name']
        print(pickup_type_name)
        status_name = res['status_name']
        print(status_name)
        every_data.append(member_phone)
        every_data.append(name)
        every_data.append(mobile)
        every_data.append(store_name)
        every_data.append(add)
        every_data.append(created_at)
        every_data.append(pickup_type_name)
        every_data.append(status_name)
        all_data.append(every_data)
    df = pd.DataFrame(all_data, columns=['会员手机号', '自提点名', '联系方式', '所属店铺', '地址', '加入时间', '类型', '状态'])
    df.to_excel('./数据.xlsx', index=False)


if __name__ == '__main__':
    members_info()

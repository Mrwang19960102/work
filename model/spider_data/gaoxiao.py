# -*- coding: utf-8 -*-
# @File:       |   gaoxiao.py
# @Date:       |   2021/1/5 20:30
# @Author:     |   ThinkPad
# @Desc:       |
import time
import requests
import os
import pandas as pd
from lxml import etree
from openpyxl import Workbook
from urllib.parse import quote
from re import findall, sub, S
from os.path import isdir, isfile
from urllib.request import urlopen

root_dir = '高校在山东省的招生科目要求2'
if not isdir(root_dir):
    os.mkdir(root_dir)

start_url = 'http://xkkm.sdzk.cn/web/xx.html#'
with urlopen(start_url) as res:
    content = res.read().decode('utf-8')
pattern = (r'<tr>.*?<td.+?</td>.*?<td.+?>(.+?)</td>'
           '.*?<td.+?>(.+?)</td>.*?<td.+?>(.*?)</td>')

for item in findall(pattern, content, S):

    # if 2 == len(item[0]):
    wb = Workbook()
    ws = wb.worksheets[0]
    columns = ['层次', '专业名称', '选考科目要求', '类中所含专业']
    ws.append(columns)
    pro_name, dm, school_name = item
    file_name = './{}/{}_{}.xlsx'.format(root_dir, pro_name, school_name)
    print(file_name)
    if isfile(file_name):
        continue
    print('正在采集{}学校的信息'.format(school_name))

    xuexiao_rul = 'http://xkkm.sdzk.cn/xkkm/queryXxInfor'
    data = {
        'dm': dm,
        'mc': quote(school_name),
        'yzm': 'ok'
    }

    headers = {
        'Referer': 'http://xkkm.sdzk.cn/web/xx.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    }

    res = requests.post(xuexiao_rul, data=data, headers=headers).text
    html = etree.HTML(res)
    infos = html.xpath('.//tr')
    all_data = []
    for k in infos:
        every_data = []
        num = ''.join(k.xpath('./td[1]//text()'))
        # t1:层次
        t1 = ''.join(k.xpath('./td[2]//text()')).strip()
        # t2:专业名称
        t2 = ''.join(k.xpath('./td[3]//text()')).strip()
        # t3:选考科目范围
        t3 = ''.join(k.xpath('./td[4]//text()')).strip()
        # t4:类中所含专业
        t4 = [i.replace('\r\n', '').replace(' ', '') for i in (k.xpath('./td[5]//text()'))]
        t4 = '|'.join(list(filter(None, t4))).strip()
        every_data.append(num)
        every_data.append(t1)
        every_data.append(t2)
        every_data.append(t3)
        every_data.append(t4)
        all_data.append(every_data)

    if all_data:
        df = pd.DataFrame(all_data, columns=['序号', '层次', '专业（类）名称', '选考科目范围', '类中所含专业'])
        df['学校名称'] = school_name
        df = df[['学校名称', '序号', '层次', '专业（类）名称', '选考科目范围', '类中所含专业']]
        df.to_excel(file_name, index=False)
        # time.sleep(10)

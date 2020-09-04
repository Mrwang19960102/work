# -*- coding: utf-8 -*-
# @File:       |   zhongxin.py 
# @Date:       |   2020/9/1 16:44
# @Author:     |   ThinkPad
# @Desc:       |
import time
import numpy as np
import pandas as pd
from model.p import conf

df = pd.read_excel('./data_source/信政合作产品_到期.xlsx', sheet_name='Sheet2')

name = list(df['产品名称'])
zhaiyaos = list(df['摘要'])
check_df = pd.DataFrame({
    '产品名称': name,
    '摘要': zhaiyaos
})
print(check_df)
city_list = []
for index, row in check_df.iterrows():
    name = row['产品名称']
    zhaiyao = row['摘要']
    in_city=None
    all_citys = []
    for every_pro_city in list(conf.city_map.values()):
        all_citys.extend(every_pro_city)
    for every_city in all_citys:
        if every_city in name:
            in_city = every_city
        elif every_city in zhaiyao:
            in_city = every_city
        if in_city:
            break
    if in_city:
        city_list.append(in_city)
    else:
        city_list.append(None)
    print(name)
    print(zhaiyao)
    print(in_city)
    time.sleep(10)

check_df['city'] = city_list
print(len(city_list), city_list)
all_pro = []
for city in city_list:
    in_pro = None
    for every_pro_citys in list(conf.city_map.values()):
        if city in every_pro_citys:
            in_pro = every_pro_citys[0]
            break
    if in_pro:
        all_pro.append(in_pro)
    else:
        all_pro.append(None)
check_df['province'] = all_pro
print(len(all_pro),all_pro)
check_df.to_excel('./results.xlsx',index=False)

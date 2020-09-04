# -*- coding: utf-8 -*-
# @File:       |   zhongxin.py 
# @Date:       |   2020/9/1 16:44
# @Author:     |   ThinkPad
# @Desc:       |
import time
import re
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
date_list = []
for index, row in check_df.iterrows():
    zhaiyao = row['摘要']
    print(zhaiyao)
    regex_res = re.findall(r"(\d{4}-\d{2}-\d{2})|(\d{4}/\d{2}/\d{2})|(\d{8})|(\d{4}年\d+月\d+日)", zhaiyao)
    # date = None
    if regex_res:
        date = list(regex_res[0])
        date = [x.replace('\n', '').replace('\r', '').replace(' ', '') for x in date]
        date = list(filter(None, date))[0]
        if date:
            date_list.append(date)
        else:
            date_list.append(None)
    else:
        date_list.append(None)
    print(date)
print(len(date_list))
check_df['时间'] = date_list
# check_df.to_excel('./results.xlsx',index=False)

res_df = pd.merge(df, check_df[['产品名称', '时间']], on=['产品名称'])
res_df['时间'] = res_df['时间'].apply(lambda x: x[0:4] if x else x)
res_df.to_excel('./res_df.xlsx', index=False)

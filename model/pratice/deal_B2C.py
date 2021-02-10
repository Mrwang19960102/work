# -*- coding: utf-8 -*-
# @File:       |   deal_B@C.py 
# @Date:       |   2021/1/21 15:52
# @Author:     |   ThinkPad
# @Desc:       |  
import pandas as pd

df = pd.read_excel('./B2C退货数据.xlsx', converters={'入库单': str})
print(list(df.columns))
df.sort_values(by='创建日期', inplace=True)
print(df)
sum = 0
sum_list = []
n = 1
n_list = []
all_data = []
for index, info in df.iterrows():
    print('上一个sum{}'.format(sum))
    every_data = []
    v1 = str(info['入库单'])
    v2 = info['业务类型']
    v3 = info['创建日期']
    v4 = info['退货箱号']
    v5 = info['货品']
    v6 = info['季节']
    v7 = info['款号']
    v8 = info['颜色']
    v9 = info['尺码']
    value = info['退货数量']
    sum += value
    n_list.append(n)
    if sum == 25:
        every_data.append(v1)
        every_data.append(v2)
        every_data.append(v3)
        every_data.append(v4)
        every_data.append(v5)
        every_data.append(v6)
        every_data.append(v7)
        every_data.append(v8)
        every_data.append(v9)
        every_data.append(value)
        every_data.append(sum)
        every_data.append(n)
        all_data.append(every_data)
        print(sum, n)
        sum = 0
        n += 1
    elif sum > 25:
        sum = sum - value
        # count = value - sum
        for i in range(value):
            every_data.append(v1)
            every_data.append(v2)
            every_data.append(v3)
            every_data.append(v4)
            every_data.append(v5)
            every_data.append(v6)
            every_data.append(v7)
            every_data.append(v8)
            every_data.append(v9)
            every_data.append(1)

            sum = sum + 1
            every_data.append(sum)
            every_data.append(n)
            print(sum, n)
            if sum + 1 > 25:
                n += 1
                sum = 0
            every_data = []
            all_data.append(every_data)
    else:
        every_data.append(v1)
        every_data.append(v2)
        every_data.append(v3)
        every_data.append(v4)
        every_data.append(v5)
        every_data.append(v6)
        every_data.append(v7)
        every_data.append(v8)
        every_data.append(v9)
        every_data.append(value)
        every_data.append(sum)
        every_data.append(n)
        all_data.append(every_data)
        print(sum, n)
if all_data:
    df_new = pd.DataFrame(all_data, columns=['入库单', '业务类型', '创建日期', '退货箱号',
                                             '货品', '季节', '款号', '颜色', '尺码', '退货数量', '累加', '编号'])
    df_new.to_excel('./B2C退货数据_new.xlsx', index=False)

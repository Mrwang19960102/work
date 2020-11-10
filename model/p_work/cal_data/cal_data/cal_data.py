# -*- coding: utf-8 -*-
# @File:       |   cal_data.py
# @Date:       |   2020/6/20 13:52
# @Author:     |
# @Desc:       |
import pandas as pd
import numpy as np

# 读取源数据文件
data_source_df = pd.read_csv('./result.csv')
if not data_source_df.empty:
    # 选择需要的列
    data_result_df = data_source_df[['Distance', 'Device', 'Tx-power']].drop_duplicates()
    data_result_list = np.array(data_result_df).tolist()
    all_data = []
    for i in data_result_list:
        every_data = []
        # 距离
        l = i[0]
        # 设备型号
        equipment_model = i[1]
        # Tx - power
        tx = i[2]
        if 'Signal(1_minute）' in list(data_source_df.columns):
            data_source_df.rename(columns={'Signal(1_minute）': 'Signal(1_minute)'}, inplace=True)
        else:
            pass
        # 筛选数据
        count_df = data_source_df[(data_source_df['Device'] == equipment_model) & (data_source_df['Tx-power'] == tx) & (
            (data_source_df['Distance'] == l))][
            ['Device', 'Tx-power', 'RSSI Max', 'Signal(1_minute)']]
        count_df['Signal(1_minute)'] = count_df['Signal(1_minute)'].apply(lambda x: 0 if x == 'OUT ZONE' else x)
        count_df['Signal(1_minute)'] = count_df['Signal(1_minute)'].astype(float)
        # 个数
        count = len(count_df)
        # 定义变量
        greater_than_count = 0
        signal_count = 0
        # RSSi有多少是大于等 - 75
        rssi_data_list = list(count_df['RSSI Max'])
        signal_data_list = list(count_df['Signal(1_minute)'])
        for i in range(len(count_df)):
            if rssi_data_list[i] >= -75:
                greater_than_count += 1
            if signal_data_list[i] >= 51:
                signal_count += 1

        # 计算RSSI百分比  小数
        pec = greater_than_count / count
        # 计算Signal百分比  小数
        pec_signal = signal_count / count
        # 数据追加
        every_data.append(l)
        every_data.append(equipment_model)
        every_data.append(tx)
        every_data.append(count)
        every_data.append(greater_than_count)
        every_data.append(pec)
        every_data.append(signal_count)
        every_data.append(pec_signal)
        all_data.append(every_data)
        print(every_data)
    print(all_data)
    data_df = pd.DataFrame(all_data, columns=['距离', '设备型号', 'Tx-power', '一共有条数据',
                                              'RSSI有多少是>=-75的', '百分比是多少', '一分钟接受的信号>=51', '百分比是多少(接受信号)'])
    data_result_df.rename(columns={'Distance': '距离', 'Device': '设备型号'}, inplace=True)

    data = pd.merge(data_result_df[['距离', '设备型号', 'Tx-power']], data_df, on=['距离', '设备型号', 'Tx-power'], how='left')

    # 生成excel文件d到相对路径
    data_df.to_excel('./Data.xlsx', index=False, encoding='utf-8-sig')
    print('结果文件已生成')
    print('------------------ok------------------')
else:
    print('源数据文件为空，请检查！')

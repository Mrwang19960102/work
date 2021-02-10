# -*- coding: utf-8 -*-
# @File:       |   deal_data.py 
# @Date:       |   2021/1/22 22:37
# @Author:     |   ThinkPad
# @Desc:       |  仓库数据处理
import pandas as pd
from model.pratice.warehouse import conf
from model.pratice.warehouse.dao import dbmanager


def warehouse():
    '''
    仓库数据处理
    @return:
    '''
    # 获取要计算的时间日期
    df = pd.read_csv('./data/return_data.csv')
    cal_date_list = df['date'].unique()
    print(cal_date_list)
    cal_date_list = ['2020-03-01']
    for cal_date in cal_date_list:
        # 读取数据库中当天退货数据
        returnDf = dbmanager.get_return_data_day(cal_date)
        print(returnDf)
        # 从数据库中得到计算时间前一天的库存的数据
        inventoryDf_L = dbmanager.get_inventory_data(cal_date)
        if not inventoryDf_L.empty:
            # 如果当天没有退库  那么前一天的库存数量也是当前时间的库存数量
            if returnDf.empty:
                inventoryDf_before_sale = inventoryDf_L
            else:
                print('************************')
                returnDf_count = returnDf.groupby(by=['sku', 'bin']).agg({'qty': 'count'})
                print('returnDf_count', returnDf_count)

        else:
            print('数据库中没有库存数据')
            inventoryDf_before_sale = returnDf

        if not inventoryDf_before_sale.empty:
            inventoryDf_before_sale = inventoryDf_before_sale.groupby(by=['sku', 'bin_no']).agg(
                {'qty': 'count'}).reset_index()
            # 当天发商品前的库存数据
            inventoryDf_before_sale.columns = ['sku', 'bin_no', 'qty']
            inventoryDf_before_sale['date'] = cal_date
            inbo = dbmanager.save_defore_sale_data(inventoryDf_before_sale)
            print('存储数据至={},大小为={},状态为={}'.format(conf.before_sale_data_table,
                                                  inventoryDf_before_sale.shape[0], inbo))
            # print(inventoryDf_before_sale)


if __name__ == '__main__':
    warehouse()

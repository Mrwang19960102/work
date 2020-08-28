# -*- coding: utf-8 -*-
# @File:       |   pre_covid.py 
# @Date:       |   2020/7/20 10:04
# @Author:     |   ThinkPad
# @Desc:       |  疫情预测

import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression as LR
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from model.machine_learning.covid_19.dao import dbmanager


def init_data(data_df, countryCode):
    '''
    初始化数据，晒选出国内数据，冰鞋返回测试集和训练集
    :param data_df:某国的疫情数据
    :param countryCode:国家代码
    :return:
    '''
    # 数据处理
    data_df['date'] = data_df['date'].apply(lambda x: datetime.strftime(x, '%Y-%m-%d'))
    X_label = list(data_df['date'])
    data_df['date'] = data_df['date'].astype(str)
    # data_df.to_excel('./国内疫情数据.xlsx',index=False)
    xdata = list(range(0, len(data_df)))
    X = np.array(xdata).reshape(-1, 1)
    Y = data_df[['confirmed']]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.8, random_state=20)
    return X_train, X_test, Y_train, Y_test


def cal_pre_covid():
    '''
    预测国内疫情数据
    :return:
    '''
    data_df = pd.read_excel('./dataSource/covid_19.xlsx')
    countryCode = 'CN'
    # data_df = dbmanager.get_data_all(countryCode)
    if not data_df.empty:
        X_train, X_test, Y_train, Y_test = init_data(data_df, countryCode)
        # 建立线性模型
        re_model = LR().fit(X_train, Y_train)
        print(re_model.coef_)
        print('训练集分数：{}'.format(re_model.score(X_train, Y_train)))
        print('测试集分数：{}'.format(re_model.score(X_test, Y_test)))
    else:
        print('没有关于{}国家的数据'.format(countryCode))





if __name__ == '__main__':
    cal_pre_covid()

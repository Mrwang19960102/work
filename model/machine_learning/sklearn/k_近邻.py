# -*- coding: utf-8 -*-
# @File:       |   k_近邻.py 
# @Date:       |   2020/8/5 16:57
# @Author:     |   ThinkPad
# @Desc:       |  
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
# k邻近算法模型
from sklearn.neighbors import KNeighborsClassifier

# 手动创建训练数据集
feature = np.array([[170, 65, 41], [166, 55, 38], [177, 80, 39], [179, 80, 43], [170, 60, 40], [170, 60, 38]])
target = np.array(['男', '女', '女', '男', '女', '女'])

# 实例k邻近模型，指定k值=3
knn = KNeighborsClassifier(n_neighbors=3)

# 训练数据
knn.fit(feature, target)

# 模型评分
s = knn.score(feature, target)
print('训练得分：{}'.format(s))
# 预测
p = knn.predict(np.array([[176, 71, 38]]))
print(p)

# -*- coding: utf-8 -*-
# @File:       |   sk_psbys.py 
# @Date:       |   2021/1/5 10:25
# @Author:     |   ThinkPad
# @Desc:       |  朴素贝叶斯分类算法练习
from time import time
from sklearn.datasets import load_files

print('开始加载训练数据集')
t1 = time()
new_train = load_files('dataset/mlcomp/379/train')
print("summary :{} documents in {} categories.".format(len(new_train.data), len(new_train.target_names)))
print('done in {} s'.format(time()-t1))

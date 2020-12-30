# -*- coding: utf-8 -*-
# @File:       |   pytorch_linemodel_pol.py 
# @Date:       |   2020/12/28 16:00
# @Author:     |   ThinkPad
# @Desc:       |  

import torch
import numpy as np
from torch.autograd import Variable
import matplotlib.pyplot as plt


def make_features(x):
    '''

    @param x:
    @return:
    '''
    x = x.unsqueeze(1)
    return torch.cat([x ** i for i in range(1, 4)], 1)


x = np.array([[1, 2, 3], [4, 5, 6]])
print(x)
b = torch.from_numpy(x)
print("b")
print(b)
print(b.size())  # torch.Size([2, 3])

c = b.unsqueeze(1)  # 在第二维增加一个维度
print("c")
print(c)
print(c.size())

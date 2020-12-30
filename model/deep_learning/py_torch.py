# -*- coding: utf-8 -*-
# @File:       |   py_torch.py 
# @Date:       |   2020/12/18 10:52
# @Author:     |   ThinkPad
# @Desc:       |  
from __future__ import print_function
import torch
from torch.autograd import Variable

x = Variable(torch.Tensor([1]), requires_grad=True)
w = Variable(torch.Tensor([2]), requires_grad=True)
b = Variable(torch.Tensor([3]), requires_grad=True)
y = w * x + b
y.backward()
print(y)
print(x.grad)
print('------------------------------')
x = torch.randn(3)
print(x)
x = Variable(x, requires_grad=True)
y = x * 2
print(y)
y.backward(torch.FloatTensor([1, 0.1, 0.01]))
print(x.grad)

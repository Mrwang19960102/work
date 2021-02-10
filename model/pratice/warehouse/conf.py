# -*- coding: utf-8 -*-
# @File:       |   conf.py 
# @Date:       |   2021/01/23 02:04
# @Author:     |   ThinkPad
# @Desc:       |  配置文件
import os
import datetime
import configparser
from model.conf.project_cfg import projtecName

cf = configparser.ConfigParser()
currPath = os.path.abspath(os.path.dirname(__file__))
projectRoot = currPath[:currPath.find(projtecName) + len(projtecName)]
cf.read(projectRoot + '/conf_database/conf.cfg')  # 里面为cfg文件的路径

db_src_conf = dict(cf.items('db_src'))
db_dest_conf = dict(cf.items('db_dest'))
# 数据库最大连接次数
max_con_number = 10


sale_data_table = 'sale_data'
return_data_table = 'return_data'
inventory_data_table = 'inventory_data'
before_sale_data_table = 'before_sale_data'

# -*- coding: utf-8 -*-
# @File:       |   conf.py 
# @Date:       |   2020/7/20 9:59
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


covid_19_table = 'covid_19'
qiye_data_table = 'qiye_data'
qiye_info_table = 'qiye_info'

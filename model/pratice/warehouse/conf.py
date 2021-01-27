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

area_dict = {
    'tianjin': '天津'
}
# 手机号字体加密对应字典
num_dict = {
    'ea1a': 0,
    'f6f3': 2,
    'f304': 3,
    'f567': 4,
    'e3d2': 5,
    'ea4d': 6,
    'e860': 7,
    'e1bf': 8,
    'f08c': 9,
}

qiye_data_table = 'qiye_data'
qiye_info_table = 'qiye_info'
film_reviews_table = 'film_reviews'

# 表名
dianping_new_shaosong_table = 'dianping_new_shaosong'
map_baidu_data_table = 'map_baidu_data'
gaodemap_baidu_data_table = 'gaodemap_baidu_data'
dzdp_shop_table = 'dzdp_shop_new'
dzdp_shop_phone_table = 'dzdp_shop_phone_new'
area_division_table = 'area_division'
douban_book_table = 'douban_book'

maoyan_movie_table = 'maoyan_movie'
stack_overflow_table = 'stack_overflow'
stack_answer_table = 'stack_answer'

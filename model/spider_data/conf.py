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
    # 'guangzhou': '广州',
    'hangzhou': '杭州',
    'suzhou': '苏州',
    'chengdu': '成都',
    'wuhan': '武汉',
    'chongqing': '重庆',
    'xian': '西安',
}
# 手机号字体加密对应字典
num_dict = {
    'e2bc': 0,
    'f582': 2,
    'ed4c': 3,
    'e911': 4,
    'e51e': 5,
    'e359': 6,
    'e7f5': 7,
    'f0c5': 8,
    'ebc8': 9,
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

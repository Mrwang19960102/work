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
    'nanjing': '南京'
}
# 手机号字体加密对应字典
num_dict = {
    'f51c': 0, 'e0f7': 5, 'ead1': 9, 'ebd9': 8,
    'e09d': 3, 'f21d': 6, 'e302': 2, 'eb33': 4,
    'e16f': 7,
}

qiye_data_table = 'qiye_data'
qiye_info_table = 'qiye_info'
film_reviews_table = 'film_reviews'

# 表名
dianping_new_shaosong_table = 'dianping_new_shaosong'
map_baidu_data_table = 'map_baidu_data_copy'
gaodemap_baidu_data_table = 'gaodemap_baidu_data'
dzdp_shop_table = 'dzdp_shop_new'
dzdp_shop_phone_table = 'dzdp_shop_phone_new'
area_division_table = 'area_division'
douban_book_table = 'douban_book'

maoyan_movie_table = 'maoyan_movie'

headers = {
    'Cookie': '_lxsdk_cuid=173ff7d706188-077c53bf069b0e-7a1437-100200-173ff7d7062c8; _lxsdk=173ff7d706188-077c53bf069b0e-7a1437-100200-173ff7d7062c8; _hc.v=988add77-4561-fac0-8537-5c5e93a36451.1597719278; s_ViewType=10; aburl=1; __utma=1.1058588512.1597720339.1597720339.1597720339.1; __utmz=1.1597720339.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ctu=9b1f465040be0773106db2215a3dccfe8202cfd8432c82a331683c3ac2f8b056; cy=5; cye=nanjing; fspop=test; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1604216368,1604280839,1604284867,1605582236; lgtoken=0d4979f3f-8e70-42f4-b296-bddf8a275eb1; dper=0395629c9e6208d8dc3cfe612de8f85292252c96e0ffae0fc47cebe21b105f786840ecc837230691da936af6794e4552cff2949660e5876ab6cf55df7f779e9804bff2f8f065aefa9dd342966d456d339651f30b55364df5026ec928e5d66afb; ll=7fd06e815b796be3df069dec7836c3df; ua=Song%E5%93%A5; uamo=15195903925; dplet=20dae2454ede3d8255249fc6651baa3a; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1605583358; _lxsdk_s=175d428a672-bc-ab5-9b6%7C%7C102',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}

# -*- coding: utf-8 -*-
# @File:       |   aiqiyi_music.py 
# @Date:       |   2020/8/19 13:22
# @Author:     |   ThinkPad
# @Desc:       |  网易云音乐
import requests
import pandas as pd
from model.spider_data.dao import dbmanager

headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}

def get_music_listing(singer_name):
    '''
    获取某歌手的歌曲清单列表
    :param singer_name: 歌手名称
    :return:
    '''
    url = 'https://music.163.com/#/search/m/?s='+singer_name+'type=1'
    res = requests.get(url,)



if __name__ == '__main__':
    singer_name = None

    get_music_listing(singer_name)


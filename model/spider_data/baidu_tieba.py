# -*- coding: utf-8 -*-
# @File:       |   baidu_tieba.py 
# @Date:       |   2021/1/26 13:16
# @Author:     |   ThinkPad
# @Desc:       |   百度贴吧数据采集
import time
import requests
import pandas as pd
from lxml import etree
from datetime import datetime
from model.spider_data import conf
from model.spider_data.dao import dbmanager
from model.spider_data.change_IP import change_ipdf, change_IP

headers = {
    'Host': 'tieba.baidu.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}


def get_post_list(url):
    '''
    请求链接 解析帖子列表信息
    @param url:请求的链接
    @return:
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    if 200 == res.status_code:
        res = res.content.decode()
        # print(res)
        html = etree.HTML(res)
        title_list = html.xpath('.//div[@class="t_con cleafix"]//text()')
        # print(title_list)


def get_tie_info(url):
    '''
    获取每个帖子的详细信息
    @param url: 帖子url
    @return:
    '''

    res = requests.get(url, headers=headers)
    if 200 == res.status_code:
        res = res.content.decode()
        html = etree.HTML(res)
        title_list = html.xpath('.//h1[@class="core_title_txt  "]/text()')
        title = None
        if title_list:
            title = title_list[0]

        original_poster = html.xpath(
            './/div[@class="l_post j_l_post l_post_bright noborder "]//div[@class="d_author"]//ul[@class="p_author"]//li[@class="d_name"]//a/text()')
        if original_poster:
            original_poster = original_poster[0]
        print('标题：{},楼主：{}'.format(title, original_poster))
        for i in range(1, 31):
            com_author_list = html.xpath(
                './/div[@class="l_post j_l_post l_post_bright  "][{}]//div[@class="d_author"]//ul[@class="p_author"]//li[@class="d_name"]//a/text()'.format(
                    i))
            postId_list = html.xpath(
                './/div[@class="l_post j_l_post l_post_bright  "][{}]//div[@class="d_post_content_main"]//div[1]//cc//div[2]/@id'.format(
                    i))
            com_list = html.xpath(
                './/div[@class="l_post j_l_post l_post_bright  "][{}]//div[@class="d_post_content_main"]//div[1]//cc//div[2]/text()'.format(
                    i))
            if com_author_list:
                com_list = [x.replace(' ', '') for x in com_list]
                postId_list = [x.replace(' ', '').replace('post_content_', '') for x in postId_list]
                print('评论作者：{},post_id={},内容：{}'.format(com_author_list, postId_list, com_list))
        print('=============================开始采集再评论=============================')
        tid = url.replace('https://tieba.baidu.com/p/', '')
        get_com_again('https://tieba.baidu.com/p/totalComment?tid={}&pn=1'.format(tid))


def get_com_again(url):
    '''
    获取再评论数据集
    @param url:
    @return:
    '''
    res = requests.get(url, headers=headers)
    if 200 == res.status_code:
        res = res.content.decode()
        info = json.loads(res)
        info = info['data']['comment_list']
        comments_list = list(info.keys())
        for com_id in comments_list:
            com_info = info[com_id]['comment_info']
            for i in range(len(com_info)):
                post_id = com_info[i]['post_id']
                thread_id = com_info[i]['thread_id']
                content = com_info[i]['content']
                username = com_info[i]['username']
                timeStamp = com_info[i]['now_time']
                date = time.localtime(timeStamp)
                otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", date)
                print('再评论---》post_id：{},thread_id:{},username:{},content:{}'.format(post_id, thread_id,
                                                                                     username, content))


if __name__ == '__main__':
    import json

    url = 'https://tieba.baidu.com/p/7206683853'
    print(url)
    get_tie_info(url)
    # url = 'https://tieba.baidu.com/p/totalComment?tid=5868518972&pn=3'
    # res = requests.get(url, headers={
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    # })
    # if 200 == res.status_code:
    #     res = res.content.decode()
    #     info_json = json.loads(res)
    #     print(info_json)

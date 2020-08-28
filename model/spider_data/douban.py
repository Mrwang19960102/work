# -*- coding: utf-8 -*-
# @File:       |   douban.py 
# @Date:       |   2020/8/19 13:55
# @Author:     |   ThinkPad
# @Desc:       |  豆瓣影评
import re
import time
import requests
import pandas as pd
import numpy as np
from lxml import etree
from datetime import datetime
from multiprocessing import Pool
from model.spider_data.dao import dbmanager


def get_comments_url():
    '''
    获取每条影评的基本信息
    :return:data_df columns = [id,author,date,title]
    '''
    headers = {
        'Referer': 'https://movie.douban.com/subject/26754233/?from=showing',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    url = 'https://movie.douban.com/subject/26754233/reviews'
    res = requests.get(url, headers=headers).content.decode()
    html = etree.HTML(res)
    # 解析数据
    comments_ids = html.xpath(('//div[contains(@class,"review-list")]//div/@data-cid'))
    # 影评作者
    authors = html.xpath(('//div[contains(@class,"review-list")]//div//div//header//a[@class="name"]/text()'))
    # 时间
    date = html.xpath(('//div[contains(@class,"review-list")]//div//div//header//span[@class="main-meta"]/text()'))
    # 标题
    title = html.xpath(('//div[contains(@class,"review-list")]//div//div//div[@class="main-bd"]//h2//a/text()'))
    # print(comments_ids)
    # print(authors)
    # print(date)
    # print(title)
    data_df = pd.DataFrame({
        'id': comments_ids,
        'author': authors,
        'date': date,
        'title': title,
    })
    print(data_df)
    return data_df


def get_info(data_df):
    '''
    获取每个评论的详细信息
    :param data_df:
    :return:
    '''
    # 请求头
    headers = {
        'Referer': 'https://movie.douban.com/subject/26754233/?from=showing',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    info_list = np.array(data_df).tolist()
    s_time = time.time()
    for info in info_list:
        spider_one(info)
    e_time = time.time()
    print('所用时间为：{}'.format(e_time - s_time))
    print('使用进程池')
    pool = Pool(processes=3)
    s_time2 = time.time()
    pool.map(spider_one, info_list)
    e_time2 = time.time()
    print('使用进程池所用时间为：{}'.format(e_time2 - s_time2))


def spider_one(info):
    headers = {
        'Referer': 'https://movie.douban.com/subject/26754233/?from=showing',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    id = info[0]
    url = 'https://movie.douban.com/j/review/' + id + '/full'
    res = requests.get(url, headers=headers).json()
    res = res['html']
    html = etree.HTML(res)
    infos = ''.join(html.xpath('//text()')).replace('\n', '').strip()
    print(infos)
    time.sleep(3)


def get_short_commentary(i):
    '''
    获取影视短评信息
    :param url: 链接
    :return:
    '''
    print('第{}页开始爬取'.format(i + 1))
    url = 'https://movie.douban.com/subject/26754233/comments?start=' + str(
        20 * i) + '&limit=20&sort=new_score&status=P&comments_only=1'
    print(url)
    headers = {
        'Cookie': 'll="118159"; bid=xotbcpbjlXw; __yadk_uid=vQrO67ppEnxeCEurYGNa9FWCKj4AjE1n; _vwo_uuid_v2=D6A50BF304C3EB7D1C320480769D2846B|53a7334fc25df749b95b3d751eddbc32; __gads=ID=e97a7339d6544c13:T=1597816470:S=ALNI_MbDlZc1I-nldxgd826z9GBqpWQncQ; __utma=30149280.1754329733.1597816468.1597836564.1597848110.4; __utmc=30149280; __utmz=30149280.1597848110.4.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; __utmb=30149280.1.10.1597848110; __utma=223695111.630311409.1597816473.1597836564.1597848118.4; __utmb=223695111.0.10.1597848118; __utmc=223695111; __utmz=223695111.1597848118.4.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1597848118%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; ap_v=0,6.0; _pk_id.100001.4cf6=49145572cba375a5.1597816473.4.1597848214.1597836684.',
        'Referer': 'https://movie.douban.com/subject/26754233/comments?start=40&limit=20&sort=new_score&status=P',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    res = requests.get(url, headers=headers).json()
    res = res['html']
    html = etree.HTML(res)
    author = html.xpath('.//div[@class="comment-item"]//div[@class="avatar"]//a/@title')
    # is_look = html.xpath('.//div[@class="comment-item"]//div[@class="comment"]//h3//span[@class="comment-info"]//span[1]/text()')
    stars = html.xpath(
        './/div[@class="comment-item"]//div[@class="comment"]//h3//span[@class="allstar50 rating"]/@title')
    date = html.xpath('.//div[@class="comment-item"]//div[@class="comment"]//h3//span[@class="comment-time "]/@title')
    content = html.xpath('.//div[@class="comment-item"]//div[@class="comment"]//p//span[@class="short"]/text()')
    date = [str(i)[0:10] for i in date]
    print(author)
    # print(len(is_look),is_look)
    # print(stars)
    print(date)
    print(content)
    data_df = pd.DataFrame({
        'author': author,
        'comment_time': date,
        'essay': content
    })
    data_df['movie_name'] = '八佰'
    in_bo = dbmanager.save_film_rebiews(data_df)
    print('The data storage state is：{},shape={}'.format(in_bo, data_df.shape[0]))
    time.sleep(5)
    return in_bo

def movie_short_comments():
    '''
    收集影视短评
    :return:
    '''
    for i in range(5, int(107443 / 20)):
        inbo = get_short_commentary(i)
        if inbo:
            pass
        else:
            break


if __name__ == '__main__':
    data_df = get_comments_url()
    get_info(data_df)
    #
    # 短评



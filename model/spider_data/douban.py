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
from model.spider_data import conf
from model.spider_data.dao import dbmanager, dbmanager_douban


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


def book_info(index, url):
    '''
    获取每个书籍的信息
    @return:
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Host': 'book.douban.com',
        'Referer': 'https://accounts.douban.com/passport/login?redir=https%3A%2F%2Fbook.douban.com%2Fsubject%2F2669319%2F',
        'Cookie': 'll="118159"; bid=xotbcpbjlXw; _vwo_uuid_v2=D6A50BF304C3EB7D1C320480769D2846B|53a7334fc25df749b95b3d751eddbc32; __utmv=30149280.19352; gr_user_id=c09d944a-24c1-4a21-bb50-abb8cfdc22a8; __yadk_uid=d2k5XQYXYjizDT3KLN2ISP2USZbCRk4e; douban-fav-remind=1; __utmc=30149280; __utmc=81379588; viewed="30434353_3414397_10608514_25799070_26879323_30190107_35105377_35080870_30284742"; __utmz=81379588.1607581968.8.5.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/passport/login; push_noty_num=0; push_doumail_num=0; __gads=ID=e97a7339d6544c13-22a5bf7212c5000f:T=1607323687:R:S=ALNI_MbQcMiR0rPl4QtFTpVQcUHuAGFbMw; __utma=81379588.893114469.1598860748.1607650410.1607657760.15; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1607657760%2C%22https%3A%2F%2Faccounts.douban.com%2Fpassport%2Flogin%3Fredir%3Dhttps%253A%252F%252Fbook.douban.com%252Fsubject%252F2669319%252F%22%5D; _pk_id.100001.3ac3=116a81bea9c1b00e.1598860748.15.1607657766.1607650747.; dbcl2="193522778:b3o7FnEq3y4"; ck=hcby; __utma=30149280.1754329733.1597816468.1607657748.1607664860.28; __utmz=30149280.1607664860.28.17.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/passport/login; __utmt=1; __utmb=30149280.2.10.1607664860'
    }
    every_data = []
    book_name = None
    author_name = None
    isbn = None
    score = None
    com_num = None
    # url = 'https://book.douban.com/subject/26879323/'

    res = requests.get(url, headers=headers, allow_redirects=False)
    if 200 == res.status_code:
        res = res.content.decode()
        html = etree.HTML(res)
        book_title = html.xpath('.//div[@id="wrapper"]//h1//span/text()')
        if book_title:
            book_name = book_title[0]
        author = html.xpath('.//div[@id="info"]//a[1]/text()')
        author = [x.replace(' ', '').replace('\n', '') for x in author]
        if author:
            author_name = author[0]
        isbn_list = html.xpath('.//div[@id="info"]//text()')
        isbn_list = [x.replace(' ', '').replace('\n', '') for x in isbn_list]
        if 'ISBN:' in isbn_list:
            isbn_index = isbn_list.index('ISBN:')
            isbn = isbn_list[isbn_index + 1]
        score_list = html.xpath('.//div[@class="rating_self clearfix"]//strong[@class="ll rating_num "]/text()')
        if score_list:
            score = score_list[0]
        com_num_list = html.xpath('.//div[@class="rating_sum"]//span//a//span/text()')
        if com_num_list:
            com_num = com_num_list[0]
        # print(book_name)
        # print(author_name)
        # print(isbn)
        # print(score)
        # print(com_num)
        every_data.append(url)
        every_data.append(book_name)
        every_data.append(author_name)
        every_data.append(isbn)
        every_data.append(score)
        every_data.append(com_num)
        print(index, every_data)
    return every_data


def get_book_info():
    while True:
        s_time = datetime.now()
        pool = Pool(processes=5)
        df = pd.read_excel('./data_source/URL三万场.xlsx')
        # 获取已经爬取过的
        url_df = dbmanager_douban.get_book_already()
        if url_df.empty:
            need_df = df
        else:
            need_df = df[~df['URL'].isin(url_df['url'].tolist())]
        all_data = []
        if need_df.empty:
            break
        else:
            print('未更新条数：{}'.format(len(need_df)))
            for index, info in need_df.iterrows():
                url = info['URL']
                try:
                    every_data = pool.apply_async(book_info, (index, url))
                    # every_data = book_info(index, url)
                    if every_data:
                        all_data.append(every_data)
                except Exception as e:
                    print(e)

                time.sleep(1)
            pool.close()
            pool.join()
            if all_data:
                all_data = [x.get() for x in all_data]
                save_df = pd.DataFrame(all_data, columns=['url', 'book_name', 'book_author',
                                                          'book_isdn', 'score', 'com_num'])
                save_df.dropna(subset=['url'], inplace=True)
                in_bo = dbmanager_douban.save_douban_book(save_df)
                e_time = datetime.now()
                print('Save data to {} shape:{},status:{},need:{}'.format(conf.douban_book_table,
                                                                          save_df.shape[0],
                                                                          in_bo,
                                                                          e_time - s_time))


if __name__ == '__main__':
    ...

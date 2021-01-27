# -*- coding: utf-8 -*-
# @File:       |   stackoverflow.py 
# @Date:       |   2021/1/14 10:06
# @Author:     |   ThinkPad
# @Desc:       |  
import time
import requests
import pandas as pd
from lxml import etree
from model.spider_data import conf
from model.spider_data.stack.sql import dbmanager


def get_data(pw, page_num):
    '''
    采集数据
    @param pw:java 或者别的
    @param page_num:页数
    @return:
    '''
    for i in range(1, int(page_num)):
        url = 'https://stackoverflow.com/questions/tagged/{}?tab=newest&page={}&pagesize=50'.format(pw, i)
        print('开始采集pw={},第{}页数据，url={}'.format(pw, i, url))
        check_bo = dbmanager.check_already(pw, i)
        if check_bo:
            print('已经采集过pw={},第{}页数据，url={}'.format(pw, i, url))
        else:
            headers = {
                'Referer': url,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
            }
            res = requests.get(url, headers=headers, timeout=6)
            if 200 == res.status_code:
                res = res.content.decode()
                html = etree.HTML(res)
                title_list = html.xpath(
                    './/div[@class="summary"]//h3//a//text()')
                print('标题--->长度：{},{}'.format(len(title_list), title_list))
                ID_list = html.xpath(
                    './/div[@class="question-summary"]//@id')
                ID_list = [x.replace('question-summary-', '') for x in ID_list]
                print('ID--->长度：{},{}'.format(len(ID_list), ID_list))
                url_list = html.xpath(
                    './/div[@class="summary"]//h3//a//@href')
                url_list = ['https://stackoverflow.com' + x for x in url_list]
                print('链接--->长度：{},{}'.format(len(url_list), url_list))
                votes_list = html.xpath(
                    './/div[@class="statscontainer"]//div[@class="stats"]//div[@class="votes"]//span//strong//text()')
                print('票数--->长度：{},{}'.format(len(votes_list), votes_list))
                answerNum_list = html.xpath(
                    './/div[@class="statscontainer"]//div[@class="stats"]//div[2]//strong//text()')
                print('回答量--->长度：{},{}'.format(len(answerNum_list), answerNum_list))
                views_list = html.xpath('.//div[@class="statscontainer"]//div[@class="views "]//text()')
                views_list = [x.replace('\r', '').replace('\n', '').replace(' ', '') for x in views_list]
                print('浏览量--->长度：{},{}'.format(len(views_list), views_list))

                authors_list = html.xpath('.//div[@class="user-details"]//a//text()')
                print('作者--->长度：{},{}'.format(len(authors_list), authors_list))

                date_list = html.xpath('.//div[@class="user-action-time"]//span[@class="relativetime"]/@title')
                date_list = [x.replace('Z', '') for x in date_list]
                print('时间--->长度：{},{}'.format(len(date_list), date_list))
                df = pd.DataFrame({
                    'title': title_list,
                    'url': url_list,
                    'vote': votes_list,
                    'answer': answerNum_list,
                    'v_num': views_list,
                    'author': authors_list,
                    'date': date_list,
                })
                df['pw'] = pw
                df['page'] = i
                inbo = dbmanager.save_stack(df)
                print('pw={},第{}页数据存储至{},len={},status={}'.format(pw, i, conf.stack_overflow_table, df.shape[0], inbo))
                time.sleep(3)


def get_answer_details(url, name):
    '''
    对有回答的获取回答作者详情
    @param url: 链接
    @return:
    '''

    headers = {
        'Referer': url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'cookie': 'prov=a5728a2c-c3ee-41d0-bb0c-b01e5c0adb99; __gads=ID=14435953eefea19c-22ce1ea1e3c40026:T=1606098072:R:S=ALNI_MZgiKB-F55TNjf7HlcZnE_JOsUaTw; usr=p=%5b160%7c%3bNewest%3b%5d%5b10%7c50%5d'
    }

    res = requests.get(url, headers=headers, timeout=6)
    if 200 == res.status_code:
        res = res.content.decode()
        html = etree.HTML(res)
        answers_list = html.xpath(
            './/div[@class="user-details"]//a/text()')
        answers_list = [x.replace(name, '') for x in answers_list]
        answers_list = list(filter(None, answers_list))
        print(answers_list)
        time_list = html.xpath(
            './/div[@class="user-info "]//div[@class="user-action-time"]//span[@class="relativetime"]/@title')
        time_list = [x.replace('Z', '') for x in time_list]
        time_list = time_list[-len(answers_list):]
        print(time_list)
        save_df = pd.DataFrame({
            'author': answers_list,
            'date': time_list,
        })
        save_df['url'] = url

        inbo = dbmanager.save_stack_answer(save_df)
        print('url={}的数据存储至{},len={},status={}'.format(url, conf.stack_answer_table, save_df.shape[0], inbo))


def spider_answer_info():
    '''
    采集湖大作者信息
    @return:
    '''
    needDf = dbmanager.get_need_url()
    if not needDf.empty:
        for index, info in needDf.iterrows():
            url = info['url']
            author = info['author']
            try:
                get_answer_details(url, author)
            except Exception as e:
                pass


if __name__ == '__main__':
    '''
    分类列表
    '''
    # 类别
    # pw = 'javascript'
    # 页数
    # page_num = 2
    # get_data(pw, page_num)


    '''
    回答详情
    '''
    spider_answer_info()

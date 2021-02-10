# -*- coding: utf-8 -*-
# @File:       |   stackoverflow.py 
# @Date:       |   2021/1/14 10:06
# @Author:     |   ThinkPad
# @Desc:       |  
import time
import requests
import pandas as pd
from lxml import etree
from multiprocessing import Pool
from model.spider_data import conf
from model.spider_data.stack.sql import dbmanager


def get_data(pw, start_page_num, end_page_num):
    '''
    采集数据
    @param pw:java 或者别的
    @param page_num:页数
    @return:
    '''
    page_list = dbmanager.check_already(pw)
    print(page_list)
    pool = Pool(processes=3)
    for p in range(int(start_page_num), int(end_page_num)):
        url = 'https://stackoverflow.com/questions/tagged/{}?tab=newest&page={}&pagesize=50'.format(pw, p)
        if p in page_list:
            print('已经采集过pw={},第{}页数据，url={}'.format(pw, p, url))
        else:
            print('开始采集pw={},第{}页数据，url={}'.format(pw, p, url))
            pool.apply(worker, args=(url, p, pw))
    pool.close()
    # 阻塞进程
    pool.join()


def worker(url, p, pw):
    try:
        headers = {
            'Referer': url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }
        res = requests.get(url, headers=headers, timeout=6)
        print('res')
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
            # views_list = html.xpath('.//div[@class="statscontainer"]//div[@class="views "]//text()')
            # views_list = [x.replace('\r', '').replace('\n', '').replace(' ', '') for x in views_list]
            # print('浏览量--->长度：{},{}'.format(len(views_list), views_list))

            # authors_list = html.xpath('.//div[@class="user-details"]//a//text()')
            # print('作者--->长度：{},{}'.format(len(authors_list), authors_list))
            authors_list = []
            views_list = []
            for i in range(1, 51):
                name = html.xpath(
                    './/div[@class="question-summary"][{}]//div[@class="summary"]//div[@class="started fr"]//div[@class="user-details"]//a//text()'.format(
                        i))
                print('第1', name)
                if name:
                    pass
                else:
                    name = html.xpath(
                        './/div[@class="question-summary"][{}]//div[@class="statscontainer"]//div[@class="started fr"]//div[@class="user-details"]/text()'.format(
                            i))
                    print('第2', name)
                    if name:
                        pass
                    else:
                        name = html.xpath(
                            './/div[@class="question-summary"][{}]//div[@class="statscontainer"]//div[@class="started fr"]//div[@class="user-info "]//div[@class="user-details"]/text()'.format(
                                i))
                        print('第3', name)
                        if name:
                            pass
                        else:
                            name = html.xpath(
                                './/div[@class="question-summary"][{}]//div[@class="summary"]//div[@class="started fr"]//div[@class="user-info "]//div[@class="user-details"]/text()'.format(
                                    i))
                            print('第4', name)
                            if name:
                                pass
                            else:
                                name = html.xpath(
                                    './/div[@class="question-summary"][{}]//div[@class="summary"]//div[@class="started fr"]//div[@class="user-info "]//div[@class="user-details"]//a/text()'.format(
                                        i))
                                print('第5', name)
                                if name:
                                    pass
                                else:
                                    name = html.xpath(
                                        './/div[@class="question-summary"][{}]//div[@class="summary"]//div[@class="started fr"]//div[@class="user-info user-hover"]//div[@class="user-details"]//a/text()'.format(
                                            i))
                                    print('第6', name)

                name = [x.replace('\r', '').replace('\n', '').replace(' ', '') for x in name]
                print(i, name)
                name = list(filter(None, name))
                authors_list.append(name[0])

                view = html.xpath('.//div[@class="question-summary"][{}]//div[@class="views "]//text()'.format(i))
                if view:
                    pass
                else:
                    view = html.xpath(
                        './/div[@class="question-summary"][{}]//div[@class="views warm"]//text()'.format(i))
                view = [x.replace('\r', '').replace('\n', '').replace(' ', '') for x in view]
                view = list(filter(None, view))
                views_list.append(view[0])
            print('浏览量--->长度：{},{}'.format(len(views_list), views_list))
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
            df['page'] = p
            inbo = dbmanager.save_stack(df)
            print('pw={},第{}页数据存储至{},len={},status={}'.format(pw, p, conf.stack_overflow_table,
                                                              df.shape[0], inbo))
    except Exception as e:
        print(e)


def get_answer_details(url, answer):
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
    print(answer, url)
    save_df = pd.DataFrame()
    res = requests.get(url, headers=headers, timeout=6)
    if 200 == res.status_code:
        res = res.content.decode()
        html = etree.HTML(res)
        answers_list = []
        time_list = []

        for i in range(1, int(answer) + 1):
            if 1 == i:
                answerName = html.xpath(
                    './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[2]//div[1]//div[@class="user-details"]//a/text()'.format(
                        2 * i))
                if answerName:
                    answers_list.append(answerName[0])
                else:
                    answerName = html.xpath(
                        './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[3]//div[1]//div[@class="user-details"]//a/text()'.format(
                            2 * i))
                    if answerName:
                        answers_list.append(answerName[0])
                    else:
                        answerName = html.xpath(
                            './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[3]//div[1]//div[@class="user-details"]//span/text()'.format(
                                2 * i))
                        if answerName:
                            answers_list.append(answerName[0])

                        pubDate = html.xpath(
                            './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[3]//div[1]//div[@class="user-action-time"]//span/@title'.format(
                                2 * i))
                        if pubDate:
                            time_list.append(pubDate[0])
                        continue
                    pubDate = html.xpath(
                        './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[3]//div[1]//div[@class="user-action-time"]//span/@title'.format(
                            2 * i))
                    if pubDate:
                        time_list.append(pubDate[0])
                    else:
                        pubDate = html.xpath(
                            './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[2]//div[1]//div[@class="user-action-time"]//span/@title'.format(
                                2 * i))
                        if pubDate:
                            time_list.append(pubDate[0])
                    continue
                pubDate = html.xpath(
                    './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[2]//div[1]//div[@class="user-action-time"]//span/@title'.format(
                        2 * i))
                if pubDate:
                    time_list.append(pubDate[0])
                    continue
                else:
                    pubDate = html.xpath(
                        './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[3]//div[1]//div[@class="user-action-time"]//span/@title'.format(
                            2 * i))
                    if pubDate:
                        time_list.append(pubDate[0])
            elif 2 == i:
                answerName = html.xpath(
                    './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[2]//div[1]//div[@class="user-details"]//a/text()'.format(
                        2 * i))
                if answerName:
                    answers_list.append(answerName[0])
                else:
                    answerName = html.xpath(
                        './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[3]//div[1]//div[@class="user-details"]//a/text()'.format(
                            2 * i))
                    if answerName:
                        answers_list.append(answerName[0])
                    else:
                        answerName = html.xpath(
                            './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[2]//div[1]//div[@class="user-details"]//span/text()'.format(
                                2 * i))
                        if answerName:
                            answers_list.append(answerName[0])
                        pubDate = html.xpath(
                            './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[2]//div[1]//div[@class="user-action-time"]//span/@title'.format(
                                2 + i))
                        if pubDate:
                            time_list.append(pubDate[0])
                            continue
                    pubDate = html.xpath(
                        './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[3]//div[1]//div[@class="user-action-time"]//span/@title'.format(
                            2 + i))
                    if pubDate:
                        time_list.append(pubDate[0])
                        continue
                pubDate = html.xpath(
                    './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[2]//div[1]//div[@class="user-action-time"]//span/@title'.format(
                        2 + i))
                if pubDate:
                    time_list.append(pubDate[0])
                    continue
            elif 3 == i:
                answerName = html.xpath(
                    './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[2]//div[1]//div[@class="user-details"]//span/text()'.format(
                        2+ i))
                if answerName:
                    answers_list.append(answerName[0])
                else:
                    answerName = html.xpath(
                        './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[3]//div[1]//div[@class="user-details"]//span/text()'.format(
                            2 + i))
                    if answerName:
                        answers_list.append(answerName[0])
                    pubDate = html.xpath(
                        './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[3]//div[1]//div[@class="user-action-time"]//span/@title'.format(
                            2 + i))
                    if pubDate:
                        time_list.append(pubDate[0])
                        continue
                pubDate = html.xpath(
                    './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[2]//div[1]//div[@class="user-action-time"]//span/@title'.format(
                        2+i))
                if pubDate:
                    time_list.append(pubDate[0])
                    continue
            elif i == 4:
                answerName = html.xpath(
                    './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[2]//div[1]//div[@class="user-details"]//a/text()'.format(
                        3 + i))
                if answerName:
                    answers_list.append(answerName[0])
                else:
                    answerName = html.xpath(
                        './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[3]//div[1]//div[@class="user-details"]//a/text()'.format(
                            3 + i))
                    if answerName:
                        answers_list.append(answerName[0])
                    pubDate = html.xpath(
                        './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[3]//div[1]//div[@class="user-action-time"]//span/@title'.format(
                            3 + i))
                    if pubDate:
                        time_list.append(pubDate[0])
                        continue
                pubDate = html.xpath(
                    './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[2]//div[1]//div[@class="user-action-time"]//span/@title'.format(
                        3 + i))
                if pubDate:
                    time_list.append(pubDate[0])
                    continue
            elif i == 5:
                answerName = html.xpath(
                    './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[2]//div[1]//div[@class="user-details"]//a/text()'.format(
                        3 + i))
                if answerName:
                    answers_list.append(answerName[0])
                else:
                    answerName = html.xpath(
                        './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[3]//div[1]//div[@class="user-details"]//a/text()'.format(
                            3 + i))
                    if answerName:
                        answers_list.append(answerName[0])
                    pubDate = html.xpath(
                        './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[3]//div[1]//div[@class="user-action-time"]//span/@title'.format(
                            3 + i))
                    if pubDate:
                        time_list.append(pubDate[0])
                        continue
                pubDate = html.xpath(
                    './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[2]//div[1]//div[@class="user-action-time"]//span/@title'.format(
                        3 + i))
                if pubDate:
                    time_list.append(pubDate[0])
                    continue
            elif i == 6:
                answerName = html.xpath(
                    './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[3]//div[1]//div[@class="user-details"]//a/text()'.format(
                        3 + i))
                if answerName:
                    answers_list.append(answerName[0])
                else:
                    answerName = html.xpath(
                        './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[2]//div[1]//div[@class="user-details"]//a/text()'.format(
                            9))
                    if answerName:
                        answers_list.append(answerName[0])
                    pubDate = html.xpath(
                        './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[2]//div[1]//div[@class="user-action-time"]//span/@title'.format(
                            9))
                    if pubDate:
                        time_list.append(pubDate[0])
                        continue

                pubDate = html.xpath(
                    './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[3]//div[1]//div[@class="user-action-time"]//span/@title'.format(
                        3 + i))
                if pubDate:
                    time_list.append(pubDate[0])
                    continue
            elif i == 7:
                answerName = html.xpath(
                    './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[3]//div[1]//div[@class="user-details"]//a/text()'.format(
                        3 + i))
                if answerName:
                    answers_list.append(answerName[0])
                else:
                    answerName = html.xpath(
                        './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[2]//div[1]//div[@class="user-details"]//a/text()'.format(
                            3 + i))
                    if answerName:
                        answers_list.append(answerName[0])
                    pubDate = html.xpath(
                        './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[2]//div[1]//div[@class="user-action-time"]//span/@title'.format(
                            3 + i))
                    if pubDate:
                        time_list.append(pubDate[0])
                        continue


                pubDate = html.xpath(
                    './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[3]//div[1]//div[@class="user-action-time"]//span/@title'.format(
                        3 + i))
                if pubDate:
                    time_list.append(pubDate[0])
                    continue
            elif i == 8:
                answerName = html.xpath(
                    './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[3]//div[1]//div[@class="user-details"]//a/text()'.format(
                        3 + i))
                if answerName:
                    answers_list.append(answerName[0])
                else:
                    answerName = html.xpath(
                        './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[2]//div[1]//div[@class="user-details"]//a/text()'.format(
                            3 + i))
                    if answerName:
                        answers_list.append(answerName[0])
                    pubDate = html.xpath(
                        './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[2]//div[1]//div[@class="user-action-time"]//span/@title'.format(
                            3 + i))
                    if pubDate:
                        time_list.append(pubDate[0])
                        continue


                pubDate = html.xpath(
                    './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[3]//div[1]//div[@class="user-action-time"]//span/@title'.format(
                        3 + i))
                if pubDate:
                    time_list.append(pubDate[0])
                    continue
            elif i == 9:
                answerName = html.xpath(
                    './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[3]//div[1]//div[@class="user-details"]//a/text()'.format(
                        3 + i))
                if answerName:
                    answers_list.append(answerName[0])
                else:
                    answerName = html.xpath(
                        './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[2]//div[1]//div[@class="user-details"]//a/text()'.format(
                            3 + i))
                    if answerName:
                        answers_list.append(answerName[0])
                    pubDate = html.xpath(
                        './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[2]//div[1]//div[@class="user-action-time"]//span/@title'.format(
                            3 + i))
                    if pubDate:
                        time_list.append(pubDate[0])
                        continue


                pubDate = html.xpath(
                    './/div[@id="answers"]//div[{}]//div[@class="post-layout"]//div[2]//div[@class="mt24"]//div[@class="grid fw-wrap ai-start jc-end gs8 gsy"]//div[3]//div[1]//div[@class="user-action-time"]//span/@title'.format(
                        3 + i))
                if pubDate:
                    time_list.append(pubDate[0])
                    continue


        if time_list:
            time_list = [x.replace('Z', '') for x in time_list]
        if answers_list:
            answers_list = [x.replace('\r', '').replace('\n', '').replace(' ', '') for x in answers_list]
        print(answers_list)
        print(time_list)
        if answers_list and time_list and len(time_list)==int(answer) and len(answers_list)==int(answer):
            save_df = pd.DataFrame({
                'author': answers_list,
                'date': time_list,
            })
            save_df['url'] = url

    return save_df

def spider_answer_info(pw):
    '''
    采集湖大作者信息
    @return:
    '''
    needDf = dbmanager.get_need_url(pw)
    df_list = []
    if not needDf.empty:
        for index, info in needDf.iterrows():
            url = info['url']
            answer = info['answer']
            save_df = pd.DataFrame()
            print('一共{}个，开始采集第{}个，url={}'.format(len(needDf), index, url))
            try:
                save_df = get_answer_details(url, answer)
            except Exception as e:
                pass
            if not save_df.empty:
                df_list.append(save_df)
                if 20 == len(df_list):
                    save_df_all = pd.concat(df_list)
                    inbo = dbmanager.save_stack_answer(save_df_all)
                    print('的数据存储至{},len={},status={}'.format(conf.stack_answer_table,
                                                             save_df_all.shape[0], inbo))
                    df_list = []


if __name__ == '__main__':
    '''
    分类列表
    '''
    # 类别
    pw = 'c%23'
    # 页数
    start_page_num = 3986
    end_page_num = 6360
    # get_data(pw, start_page_num, end_page_num)

    '''
    回答详情
    '''
    spider_answer_info(pw)
    # url = 'https://stackoverflow.com/questions/48515642/identify-common-lists-in-list-and-return-distinct-lists-in-list'
    # answer = 5
    # save_df = get_answer_details(url, answer)

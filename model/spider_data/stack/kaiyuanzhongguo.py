# -*- coding: utf-8 -*-
# @File:       |   kaiyuanzhongguo.py 
# @Date:       |   2021/1/24 16:51
# @Author:     |   ThinkPad
# @Desc:       |  开源中国数据爬取
import time
import requests
import pandas as pd
from lxml import etree
from datetime import datetime
from model.spider_data.stack import conf
from model.spider_data.stack.sql import dbmanager
from model.spider_data.change_IP import change_ipdf, change_IP


def get_list(pw):
    '''
    获取开源中国数据信息
    @param pw:
    @return:
    '''
    headers = {
        'Host': 'www.oschina.net',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Cookie': '_user_behavior_=6a77ecbc-722d-4ef9-bb28-b55278e5dd00; Hm_lvt_a411c4d1664dd70048ee98afe7b28f0b=1611477730; _circle_articles_unique_key=26768507109541033; Hm_lpvt_a411c4d1664dd70048ee98afe7b28f0b=1611478111'
    }
    # 获取数据库中已经采集过的页面
    page_list = dbmanager.get_already_pw_page(pw)
    for i in range(1, 101):
        if i not in page_list:
            url = 'https://www.oschina.net/question/widgets/_question_tag_list?tag={}&show=time&p={}&type=ajax'.format(
                pw, i)
            print('pw={},开始采集第{}页数据,url={}'.format(pw, i, url))
            res = requests.get(url, headers=headers)
            if 200 == res.status_code:
                res = res.content.decode()
                html = etree.HTML(res)
                answers_count = html.xpath('.//div[@class="ui statistic"]//div[1]/text()')
                title_list = html.xpath('.//div[@class="content"]//a[@class="header"]/text()')
                title_list = [x.replace('\n', '').replace(' ', '') for x in title_list]
                title_list = list(filter(None, title_list))
                url_list = html.xpath('.//div[@class="content"]//a[@class="header"]/@href')
                # author_list = html.xpath('.//div[@class="ui horizontal list"]//div[@class="item"]//a/text()')
                # time_list = html.xpath('.//div[@class="ui horizontal list"]//div[@class="item"]//a/text()')
                print('回答量--->长度：{},{}'.format(len(answers_count), answers_count))
                print('标题--->长度：{},{}'.format(len(title_list), title_list))
                print('链接--->长度：{},{}'.format(len(url_list), url_list))
                save_df = pd.DataFrame({
                    'title': title_list,
                    'url': url_list,
                })
                save_df['pw'] = pw
                save_df['page'] = i
                in_bo = dbmanager.save_kaiyuan(save_df)
                print('pw={},第{}页数据存储至{},len={},status={}'.format(pw, i, conf.kaiyuan_table, save_df.shape[0], in_bo))
                time.sleep(1)
        else:
            print('pw={},第{}数据已经采集过'.format(pw, i))


def get_info_details(pw):
    '''
    采集详情数据
    @param url:链接
    @return:
    '''
    headers = {
        'Host': 'www.oschina.net',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Cookie': '_user_behavior_=6a77ecbc-722d-4ef9-bb28-b55278e5dd00; Hm_lvt_a411c4d1664dd70048ee98afe7b28f0b=1611477730; _circle_articles_unique_key=26768507109541033; Hm_lpvt_a411c4d1664dd70048ee98afe7b28f0b=1611478111'
    }
    need_url_df = dbmanager.get_need_url_kaiyuan(pw)
    df_list1 = []
    df_list2 = []
    for index, info in need_url_df.iterrows():
        program_time = datetime.now()
        # global ip_df
        # global s_time
        # if (program_time - s_time).seconds > 60 * 25:
        #     ip_df = change_ipdf()
        #     s_time = program_time
        #     print('重新加载')
        # proxies = change_IP(ip_df)
        url = info['url']
        print('pw={}一共{}个，开始采集第{}个，url={}'.format(pw, len(need_url_df), index, url))
        try:
            res = requests.get(url, headers=headers,timeout=5)
            # print(res.status_code, proxies)
            if 200 == res.status_code:
                res = res.content.decode()
                html = etree.HTML(res)
                author_list = html.xpath(
                    './/div[@class="extra ui horizontal list meta-wrap"]//div[@class="item"][1]//a//span/text()')
                pubdate_list = html.xpath(
                    './/div[@class="extra ui horizontal list meta-wrap"]//div[@class="item"][1]//text()')
                author_name = None
                pubdate = None
                read_count = None
                collection_count = None
                answer = None
                if author_list:
                    author_name = author_list[0]
                pubdate_list = [x.replace('\n', '').replace(' ', '').replace(author_name, '') for x in pubdate_list]
                pubdate_list = list(filter(None, pubdate_list))
                if pubdate_list:
                    pubdate = pubdate_list[0]
                    pubdate = pubdate.replace('发布于', '')
                read_count_list = html.xpath(
                    './/div[@class="extra ui horizontal list meta-wrap"]//div[@class="item"][2]/text()')
                if read_count_list:
                    read_count = read_count_list[0]
                collection_count_list = html.xpath(
                    './/div[@class="extra ui horizontal list meta-wrap"]//div[@class="item collect-btn "]//span/text()')
                if collection_count_list:
                    collection_count = collection_count_list[0]
                answer_list = html.xpath(
                    './/div[@class="extra ui horizontal list meta-wrap"]//div[@class="item comment-count"]//a//span/text()')
                if answer_list:
                    answer = answer_list[0]

                print('作者:{},发布时间:{},阅读量:{},收藏量:{},答案:{}'.format(author_name, pubdate,
                                                                 read_count, collection_count, answer))
                infoDf = pd.DataFrame({
                    'url': [url],
                    'author': [author_name],
                    'pub_date': [pubdate],
                    'read_count': [read_count],
                    'col_count': [collection_count],
                    'answer_count': [answer],
                })
                if not infoDf.empty:
                    df_list1.append(infoDf)
                # 评论区
                if answer:
                    comments_author_list = html.xpath(
                        './/div[@class="answer-content-wrap"]//div[@class="content"]//a[@class="author"]/text()')
                    comments_date_list = html.xpath(
                        './/div[@class="answer-content-wrap"]//div[@class="content"]//div[@class="metadata"]//span/text()')
                    comments_date_list = [x.replace('\n', '').replace(' ', '').replace('\xa0', '') for x in
                                          comments_date_list]
                    comments_date_list = list(filter(None, comments_date_list))
                    print('评论作者：长度{}，{}'.format(len(comments_author_list), comments_author_list))
                    print('评论时间：长度{}，{}'.format(len(comments_date_list), comments_date_list))
                    answerDf = pd.DataFrame({
                        'com_author': comments_author_list,
                        'pub_date': comments_date_list,
                    })
                    answerDf['url'] = url
                    if not answerDf.empty:
                        df_list2.append(answerDf)
            if len(df_list1) == 8:
                all_infodf = pd.concat(df_list1)
                in_bo = dbmanager.save_kaiyuan(all_infodf, conf.kaiyuan_info_table)
                print('pw={},数据存储至{},len={},status={}'.format(pw, conf.kaiyuan_info_table, all_infodf.shape[0], in_bo))
                df_list1 = []
            if len(df_list2) == 10:
                all_answerDf = pd.concat(df_list2)
                in_bo = dbmanager.save_kaiyuan(all_answerDf, conf.kaiyuan_comment_table)
                print('pw={},数据存储至{},len={},status={}'.format(pw, conf.kaiyuan_comment_table, all_answerDf.shape[0],
                                                              in_bo))
                df_list2 = []
            # time.sleep(2)
        except Exception as e:
            pass


if __name__ == '__main__':
    # s_time =datetime.now()
    pw_list = ['java', 'android-os', 'php', 'mysql', 'spring',
               'jfinal', 'python', 'eclipse', 'linux', 'jquery',
               'tomcat', 'ubuntu', 'centos', 'android', 'echarts']
    # get_list('android-os')
    get_info_details('android-os')

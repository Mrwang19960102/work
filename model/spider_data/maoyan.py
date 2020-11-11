# -*- coding: utf-8 -*-
# @File:       |   maoyan.py 
# @Date:       |   2020/11/10 14:41
# @Author:     |   ThinkPad
# @Desc:       |  猫眼电影数据
import requests
import pandas as pd
from lxml import etree
from model.spider_data import conf
from model.spider_data.dao import dbmanger_maoyan


def maoyan_movie():
    '''
    获取猫眼电影数据
    @return:
    '''
    for p in range(0, 67):
        print('第{}页'.format(p + 1))
        url = 'https://maoyan.com/films?catId=3&showType=3&offset={}'.format(str(30 * p))
        headers = {
            'Referer': 'https://maoyan.com/films?catId=3&showType=3',
            'Cookie': 'uuid_n_v=v1; uuid=40E29DC0231911EB96DF7B12A07503B62F627A54A6AA4DA3849A7A67B727AFEE; _csrf=293a33d33dfefff6429158faf4941b04f616ff316419b6e7007924d2445cc719; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1604987693; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=175b0b8a850c8-0cef7a3e4c6087-7a1437-100200-175b0b8a8500; _lxsdk=40E29DC0231911EB96DF7B12A07503B62F627A54A6AA4DA3849A7A67B727AFEE; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1604990573; __mta=45915675.1604987693266.1604990363086.1604990573342.10; _lxsdk_s=175b0d50ca0-eb8-279-8fa%7C%7C25',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }
        res = requests.get(url, headers=headers)
        if 200 == res.status_code:
            res = res.content.decode()
            html = etree.HTML(res)
            movie_names = html.xpath('.//div[@class="channel-detail movie-item-title"]//a/text()')
            score_list = html.xpath('.//div[@class="channel-detail channel-detail-orange"]//text()')
            url_list = html.xpath('.//div[@class="movie-item film-channel"]//div[@class="movie-item-hover"]//a/@href')

            complate_score_list = []
            for i in range(len(score_list)):
                s = score_list[i]
                if '.' in s:
                    complate_score = s + score_list[i + 1]
                    complate_score_list.append(complate_score)
                elif '暂无评分' == s:
                    complate_score = s
                    complate_score_list.append(complate_score)
                else:
                    pass

            print('电影名称：', len(movie_names), movie_names)
            print('电影链接：', len(url_list), url_list)
            print('电影评分：', len(complate_score_list), complate_score_list)
            save_df = pd.DataFrame({
                'movie_name': movie_names,
                'url': url_list,
                'score': complate_score_list
            })
            save_df['page'] = p + 1
            inbo = dbmanger_maoyan.save_maoyan_movie(save_df)
            print('save data to {} shape={},status={}'.format(conf.maoyan_movie_table, save_df.shape[0], inbo))


def movie_infos():
    '''
    获取每部电影的基本信息
    @return:
    '''
    url = 'https://maoyan.com/films/246390'
    headers = {
        'Referer': 'https://maoyan.com/films?catId=3&showType=3',
        'Cookie': 'uuid_n_v=v1; uuid=40E29DC0231911EB96DF7B12A07503B62F627A54A6AA4DA3849A7A67B727AFEE; _csrf=293a33d33dfefff6429158faf4941b04f616ff316419b6e7007924d2445cc719; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1604987693; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=175b0b8a850c8-0cef7a3e4c6087-7a1437-100200-175b0b8a8500; _lxsdk=40E29DC0231911EB96DF7B12A07503B62F627A54A6AA4DA3849A7A67B727AFEE; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1604990573; __mta=45915675.1604987693266.1604990363086.1604990573342.10; _lxsdk_s=175b0d50ca0-eb8-279-8fa%7C%7C25',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    if 200 == res.status_code:
        res = res.content.decode()
        html = etree.HTML(res)
        eng_name = html.xpath('.//div[@class="ename ellipsis"]/text()')
        movie_type = html.xpath('.//div[@class="movie-brief-container"]//ul//li[@class="ellipsis"]//text()')
        movie_score = html.xpath('.//span[@class="index-left info-num "]//span[@class="stonefont"]/text()')
        comments_user = html.xpath('.//div[@class="user"]//span[@class="name"]/text()')
        comments_time = html.xpath('.//div[@class="time"]//span/@title')
        comments = html.xpath('.//div[@class="comment-content"]//text()')
        print(eng_name)
        print(movie_type)
        print(movie_score)
        print(len(comments_user), comments_user)
        print(len(comments_time), comments_time)
        print(len(comments), comments)


def maoyan_movie_phone():
    '''

    @return:
    '''
    url = 'https://m.maoyan.com/ajax/moreClassicList?sortId=1&showType=3&limit=100&offset=0&optimus_uuid=6C26AC7023C711EB8297174E8F78EC04D276343670EB40C38C7AF592B64B9354&optimus_risk_level=71&optimus_code=10'
    headers = {
        'Host': 'm.maoyan.com',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Mobile Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    if 200 == res.status_code:
        res = res.content.decode()
        html = etree.HTML(res)
        url_list = html.xpath('.//a/@href')
        name_list = html.xpath('.//div[@class="title line-ellipsis"]/text()')
        type_list = html.xpath('.//div[@class="actors line-ellipsis"]/text()')
        releaseTime_list=[]
        for i in range(1, 101):
            releaseTime = html.xpath(
                './/a[{}]//div[@class="movie-info"]//div[@class="show-info line-ellipsis"]//text()'.format(str(i)))
            if releaseTime:
                releaseTime_list.append(releaseTime[0])
            else:
                releaseTime_list.append(None)
        score_list = html.xpath('.//div[@class="movie-score"]//text()')
        score_list = [x.replace('\n', '').replace('分', '').replace(' ', '') for x in score_list]
        score_list = list(filter(None, score_list))
        print(len(url_list), url_list)
        print(len(name_list), name_list)
        print(len(type_list), type_list)
        print(len(releaseTime_list), releaseTime_list)
        print(len(score_list), score_list)


if __name__ == '__main__':
    maoyan_movie_phone()

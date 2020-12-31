# -*- coding: utf-8 -*-
# @File:       |   qq_new.py 
# @Date:       |   2020/12/4 9:49
# @Author:     |   ThinkPad
# @Desc:       |  腾讯新闻
import time
import json
import requests
from lxml import etree
from datetime import datetime
import pandas as pd


def pe_news_list():
    '''
    获取体育类新闻信息
    @return:
    '''
    headers = {
        'cookie': 'ts_refer=www.baidu.com/link; pgv_pvid=7440172957; ts_uid=3743848320; tvfe_boss_uuid=480ded564c320d60; pgv_pvi=3096041472; RK=qEoR5tf2Zq; ptcz=cbd390483cd86472d6678aa39af3e991eae84b38a9dc15ff29187fb218ab021a; pac_uid=0_146faebdaab70; pgv_info=ssid=s2940479828; ts_last=news.qq.com/; pt_local_token=123456789',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    for i in range(50):
        url = 'https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?sub_srv_id=sports&srv_id=pc&offset={}'.format(
            str(
                i * 20)) + '&limit=20&strategy=1&ext={%22pool%22:[%22top%22],%22is_filter%22:14,%22check_title%22:0,%22check_type%22:true}'
        res = requests.get(url, headers=headers)
        if 200 == res.status_code:
            res = res.content.decode()
            info_json = json.loads(res)

            news_info = info_json['data']['list']
            url_list = []
            title_list = []
            content_list = []
            for info in news_info:
                url_list.append(info['url'])

                content = news_content(info['url'])
                print(info['url'], content)
                content_list.append(content)
                title_list.append(info['title'])
                time.sleep(0.5)
            print(len(url_list), url_list)
            print(len(title_list), title_list)
            print(len(content_list), content_list)


def news_content(url):
    '''
    获取新闻内容
    @param url: 新闻链接
    @return:
    '''
    content = None
    headers = {
        'cookie': 'pgv_pvid=7440172957; tvfe_boss_uuid=480ded564c320d60; pgv_pvi=3096041472; RK=qEoR5tf2Zq; ptcz=cbd390483cd86472d6678aa39af3e991eae84b38a9dc15ff29187fb218ab021a; ts_uid=2082792192; pac_uid=0_146faebdaab70; pgv_info=ssid=s2940479828; pt_local_token=123456789; ts_refer=sports.qq.com/; ts_last=new.qq.com/omn/20201204/20201204A01J6000.html; ad_play_index=41',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    if 200 == res.status_code:
        res = res.content.decode('gbk')
        html = etree.HTML(res)
        content = html.xpath('.//div[@class="content-article"]//p//text()')
        if content:
            pass
        else:
            print('跳转链接')
            id = url.replace('https://new.qq.com/omn/20201230/', '').replace('.html', '')
            new_url = 'https://new.qq.com/rain/a/' + id
            res_new = requests.get(new_url, headers=headers)
            if 200 == res_new.status_code:
                res_new = res_new.content.decode()
                html_new = etree.HTML(res_new)
                content = html_new.xpath('.//div[@class="content-article"]//p//text()')

    if content:
        content = [x.replace('\n', '').replace(' ', '') for x in content]
        content = list(filter(None,content))

    return content


if __name__ == '__main__':
    pe_news_list()
    # url = 'https://new.qq.com/omn/20201204/20201204A05U1M00.html'
    # news_info(url)

# -*- coding: utf-8 -*-
# @File:       |   public_comments.py 
# @Date:       |   2020/8/31 9:31
# @Author:     |   ThinkPad
# @Desc:       |  大众网评  评论
import time
import requests
from lxml import etree
from datetime import datetime

headers = {
    'Cookie': '_lxsdk_cuid=173ff7d706188-077c53bf069b0e-7a1437-100200-173ff7d7062c8; _lxsdk=173ff7d706188-077c53bf069b0e-7a1437-100200-173ff7d7062c8; _hc.v=988add77-4561-fac0-8537-5c5e93a36451.1597719278; s_ViewType=10; aburl=1; __utma=1.1058588512.1597720339.1597720339.1597720339.1; __utmz=1.1597720339.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); fspop=test; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1597719326,1597722680,1597904377,1598836940; cy=5; cye=nanjing; dplet=86d219cec2636475feba74520ea5a120; dper=70039cd3d2a2aa6eb6af464d7fa48ed947f1a6b2d8af56fc693fc36cc1bbf9abbbb6ed48900b3bd888a09121226146e4aa0fd1453744b108a177e49765e500e8112515512fec93769c382cf038f5860be24c99afdd9e1eb20d8509d9ce938628; ll=7fd06e815b796be3df069dec7836c3df; ua=Song%E5%93%A5; ctu=9b1f465040be0773106db2215a3dccfe8202cfd8432c82a331683c3ac2f8b056; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1598837446; _lxsdk_s=174421b9cc7-522-0cd-880%7C%7C322',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate'
}


def commments_info():
    '''
    获取店铺评论
    '''
    # 定义变量
    desc_list = []
    url = 'http://www.dianping.com/shop/G6YOcLMLGbwwNRi6/review_all/p3'
    res = requests.get(url, headers=headers).content.decode()
    html = etree.HTML(res)
    # print(res)
    # 评论作者
    authors = html.xpath(
        './/div[@class="reviews-items"]//ul//li//div[@class="main-review"]//div[@class="dper-info"]//a[@class="name"]/text()')
    authors = [x.replace('\n', '').replace('\r', '').replace(' ', '') for x in authors]
    # 评论时间
    com_date = html.xpath(
        './/div[@class="reviews-items"]//ul//li//div[@class="main-review"]//div[@class="misc-info clearfix"]//span[@class="time"]/text()')
    com_date = [x.replace('\n', '').replace('\r', '').replace(' ', '') for x in com_date]
    com_date = [x[:10]+' '+x[11:] for x in com_date]
    for i in range(1, 16):
        comments = html.xpath(
            './/div[@class="reviews-items"]//ul//li[{}]//div[@class="main-review"]//div[3]/text()'.format(
                i))
        desc = html.xpath(
            './/div[@class="reviews-items"]//ul//li[{}]//div[@class="main-review"]//div[@class="review-rank"]//span[@class="score"]//span/text()'.format(
                i))
        desc = [x.replace('\n', '').replace('\r', '').replace(' ', '') for x in desc]
        desc_list.append(desc)

    print('评论作者：', authors)
    print('评论描述：', desc_list)
    print('评论时间：', com_date)


if __name__ == '__main__':
    commments_info()

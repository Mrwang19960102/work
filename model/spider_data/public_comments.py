# -*- coding: utf-8 -*-
# @File:       |   public_comments.py 
# @Date:       |   2020/8/31 9:31
# @Author:     |   ThinkPad
# @Desc:       |  大众网评  评论
import re
import time
import math
import copy
import requests
import pandas as pd
from lxml import etree
from datetime import datetime
from model.spider_data import tools

headers = {
    'Cookie': '_lxsdk_cuid=173ff7d706188-077c53bf069b0e-7a1437-100200-173ff7d7062c8; _lxsdk=173ff7d706188-077c53bf069b0e-7a1437-100200-173ff7d7062c8; _hc.v=988add77-4561-fac0-8537-5c5e93a36451.1597719278; s_ViewType=10; aburl=1; __utma=1.1058588512.1597720339.1597720339.1597720339.1; __utmz=1.1597720339.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); fspop=test; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1597719326,1597722680,1597904377,1598836940; cy=5; cye=nanjing; dplet=86d219cec2636475feba74520ea5a120; dper=70039cd3d2a2aa6eb6af464d7fa48ed947f1a6b2d8af56fc693fc36cc1bbf9abbbb6ed48900b3bd888a09121226146e4aa0fd1453744b108a177e49765e500e8112515512fec93769c382cf038f5860be24c99afdd9e1eb20d8509d9ce938628; ll=7fd06e815b796be3df069dec7836c3df; ua=Song%E5%93%A5; ctu=9b1f465040be0773106db2215a3dccfe8202cfd8432c82a331683c3ac2f8b056; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1598837446; _lxsdk_s=174421b9cc7-522-0cd-880%7C%7C322',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate',
    'Host': 'www.dianping.com'
}
headers_svg = {
    'Cookie': '_lxsdk_cuid=173ff7d706188-077c53bf069b0e-7a1437-100200-173ff7d7062c8; _lxsdk=173ff7d706188-077c53bf069b0e-7a1437-100200-173ff7d7062c8; _hc.v=988add77-4561-fac0-8537-5c5e93a36451.1597719278; s_ViewType=10; aburl=1; __utma=1.1058588512.1597720339.1597720339.1597720339.1; __utmz=1.1597720339.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); fspop=test; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1597719326,1597722680,1597904377,1598836940; cy=5; cye=nanjing; dplet=86d219cec2636475feba74520ea5a120; dper=70039cd3d2a2aa6eb6af464d7fa48ed947f1a6b2d8af56fc693fc36cc1bbf9abbbb6ed48900b3bd888a09121226146e4aa0fd1453744b108a177e49765e500e8112515512fec93769c382cf038f5860be24c99afdd9e1eb20d8509d9ce938628; ll=7fd06e815b796be3df069dec7836c3df; ua=Song%E5%93%A5; ctu=9b1f465040be0773106db2215a3dccfe8202cfd8432c82a331683c3ac2f8b056; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1598837446; _lxsdk_s=174421b9cc7-522-0cd-880%7C%7C322',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate'
}

headers_comments = {
    'Cookie': '_lxsdk_cuid=173ff7d706188-077c53bf069b0e-7a1437-100200-173ff7d7062c8; _lxsdk=173ff7d706188-077c53bf069b0e-7a1437-100200-173ff7d7062c8; _hc.v=988add77-4561-fac0-8537-5c5e93a36451.1597719278; s_ViewType=10; aburl=1; __utma=1.1058588512.1597720339.1597720339.1597720339.1; __utmz=1.1597720339.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); fspop=test; cy=5; cye=nanjing; dplet=86d219cec2636475feba74520ea5a120; dper=70039cd3d2a2aa6eb6af464d7fa48ed947f1a6b2d8af56fc693fc36cc1bbf9abbbb6ed48900b3bd888a09121226146e4aa0fd1453744b108a177e49765e500e8112515512fec93769c382cf038f5860be24c99afdd9e1eb20d8509d9ce938628; ua=Song%E5%93%A5; ctu=9b1f465040be0773106db2215a3dccfe8202cfd8432c82a331683c3ac2f8b056; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; ll=7fd06e815b796be3df069dec7836c3df; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1598855917,1598855925,1598925904,1599013518; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1599113591; _lxsdk_s=174528e4f8f-44b-794-02%7C%7C887',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate'
}

headers_css = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'accept-encoding': 'gzip, deflate, br'
}


def get_comment_map(svg_link, status=0):
    '''
    根据样式链接获取每个字体对应的映射关系
    @param svg_link: 链接
    @param status: svg标签样式不同 0：标签为textlength  1:表示：标签为y
    @return: 字典映射
    '''''
    if 0 == status:
        res = requests.get(svg_link, headers=headers_svg).content
        html = etree.HTML(res)
        href_list = html.xpath('.//defs//path/@d')
        href_list = [x.replace('M0', '').replace('H600', '').replace(' ', '') for x in href_list]
        tag_message = re.compile('>(.*)</text')
        tag_message = tag_message.findall(res.decode())
    elif 1 == status:
        res = requests.get(svg_link, headers=headers_svg).content.decode()
        href_list = re.findall(r'y="(\d+)"', res)
        href_list = [x.replace('M0', '').replace('H600', '').replace(' ', '') for x in href_list]
        tag_message = re.compile('>(.*)</text')
        tag_message = tag_message.findall(res)
    font_map = pd.DataFrame({
        'y_up': href_list,
        'fonts': tag_message
    })
    font_map['y_up'] = font_map['y_up'].astype(int)
    font_map['y_low'] = font_map['y_up'].shift(1)
    font_map = font_map[['y_low', 'y_up', 'fonts']]
    font_map.fillna(0, inplace=True)
    font_map['y_low'] = font_map['y_low'].astype(int)

    return font_map


def get_css_svg_link(url):
    '''
    获取url页面中两个链接 css 链接和 svg 链接
    @param url:
    @return: css_link,svg_link
    '''
    css_link = None
    print('评论链接：{}'.format(url))
    res = requests.get(url, headers=headers_comments).content.decode()
    html = etree.HTML(res)
    css_link_list = html.xpath('.//link[@type="text/css"]/@href')
    for css in css_link_list:
        if css.startswith('//s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/'):
            css_link = 'https:' + css
            break
    svg_link = 'http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/6f55592cbc6d8de0ec364b670f62bb3a.svg'
    print('css链接：{}'.format(css_link))
    print('svg链接：{}'.format(svg_link))
    return css_link, svg_link


def get_font_map_data(url):
    '''
    获取字体加密对应关系
    1、获取css和svg的链接
    2、获取（每一行，和backgroup区间所在行）文字的dataframe对象
    3、获取前端页面中每一个隐藏字体的class background_x background_y 所组成的dataframe数据 offset_df
    4、循环遍历offset_df  确定所隐藏的字
    '''
    font_map_df = pd.DataFrame()
    # 评论rul链接拼接
    url += '/review_all/p1'
    # 获取css和svg的链接
    res = requests.get(url, headers=headers).content.decode()
    css_link, svg_link = get_css_svg_link(url)
    if css_link and svg_link:
        # 获取（每一行，和backgroup区间所在行）文字的dataframe对象
        fonts_xy = get_comment_map(svg_link, 1)
        # 获取前端页面中每一个隐藏字体的class background_x background_y 所组成的dataframe数据 offset_df
        css_res = requests.get(css_link, headers=headers_css).text
        font_key_list = re.findall(r'<svgmtsi class="(.*?)"></svgmtsi>', res)
        offset_data = []
        for font_key in font_key_list:
            every_offset_data = []
            pos_key = re.findall(r'.' + font_key + '{background:-(.*?).0px -(.*?).0px;}', css_res)
            background_x = int(pos_key[0][0])
            background_y = int(pos_key[0][1])
            every_offset_data.append(font_key)
            every_offset_data.append(background_x)
            every_offset_data.append(background_y)
            offset_data.append(every_offset_data)
        offset_df = pd.DataFrame(offset_data, columns=['class', 'background_x', 'background_y'])

        print('加密字体的偏移坐标获取完毕')
        all_fonts = []
        if not fonts_xy.empty and not offset_df.empty:
            # 循环遍历offset_df、确定所隐藏的字
            for index, row in offset_df.iterrows():
                x = row['background_x'] / 14 + 1
                background_y = row['background_y']
                fonts = \
                    fonts_xy[(fonts_xy['y_low'] < background_y) & (background_y <= fonts_xy['y_up'])]['fonts'].tolist()[
                        0]
                font = fonts[int(x) - 1:int(x)]
                all_fonts.append(font)
        offset_df['font'] = all_fonts
        font_map_df = offset_df[['class', 'font']]
        print('class标签对应字体数据解析完毕')

    else:
        print('获取url = {}对应的css链接和svg链接，暂不爬取'.format(url))
    return font_map_df


def shop_infos():
    '''
    商家信息:名称、地址、电话等信息
    '''
    url = 'http://www.dianping.com/shop/ESgfeYKnyRWgqNy6'
    headers = {
        'Cookie': '_lxsdk_cuid=173ff7d706188-077c53bf069b0e-7a1437-100200-173ff7d7062c8; _lxsdk=173ff7d706188-077c53bf069b0e-7a1437-100200-173ff7d7062c8; _hc.v=988add77-4561-fac0-8537-5c5e93a36451.1597719278; s_ViewType=10; aburl=1; __utma=1.1058588512.1597720339.1597720339.1597720339.1; __utmz=1.1597720339.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); fspop=test; cy=5; cye=nanjing; dplet=86d219cec2636475feba74520ea5a120; dper=70039cd3d2a2aa6eb6af464d7fa48ed947f1a6b2d8af56fc693fc36cc1bbf9abbbb6ed48900b3bd888a09121226146e4aa0fd1453744b108a177e49765e500e8112515512fec93769c382cf038f5860be24c99afdd9e1eb20d8509d9ce938628; ua=Song%E5%93%A5; ctu=9b1f465040be0773106db2215a3dccfe8202cfd8432c82a331683c3ac2f8b056; ll=7fd06e815b796be3df069dec7836c3df; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1598854675,1598855917,1598855925,1598925904; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1598940244; _lxsdk_s=1744837056d-468-3ae-e5f%7C%7C371',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    res = requests.get(url, headers=headers).content.decode()
    # 获取数字加密映射关系
    num = tools.get_num_font('1e0a7e13.woff')
    for key in num:
        if key in res:
            res = res.replace(key, str(num[key]))
    html = etree.HTML(res)

    # 店铺名称
    shop_name = html.xpath('.//div[@id="basic-info"]//h1[@class="shop-name"]//text()')
    shop_name = [x.replace('\n', '').replace('\r', '').replace(' ', '') for x in shop_name]
    shop_name = list(filter(None, shop_name))
    shopName = ''
    for n in shop_name:
        shopName += n
    # 人均价格
    price = html.xpath('.//div[@id="basic-info"]//div[@class="brief-info"]//span[@id="avgPriceTitle"]//text()')
    price_unit = ''
    for n in price:
        price_unit += n

    # 评论条数
    com_count = html.xpath('.//div[@id="basic-info"]//div[@class="brief-info"]//span[@id="reviewCount"]//text()')
    com_count = [x.replace('\n', '').replace('\r', '').replace(' ', '') for x in com_count]
    com_count = list(filter(None, com_count))
    com_count = [x.replace('条评价', '') for x in com_count]
    com_count = list(filter(None, com_count))
    count_comment = ''
    for c in com_count:
        count_comment += c
    # count_comment = int(count_comment)
    # 公共评分
    comment_score = html.xpath('.//div[@id="basic-info"]//div[@class="brief-info"]//span[@id="comment_score"]//text()')
    comment_score = [x.replace('\n', '').replace('\r', '').replace(' ', '') for x in comment_score]
    comment_score = list(filter(None, comment_score))
    commentScore = ''
    for s in comment_score:
        commentScore += s

    # 电话
    telephone = html.xpath('.//div[@id="basic-info"]//p[@class="expand-info tel"]//text()')
    telephone = [x.replace('\n', '').replace('\r', '').replace(' ', '') for x in telephone]
    telephone = list(filter(None, telephone))
    tel_phone = ''
    for n in telephone:
        tel_phone += n

    # 获取文字加密映射关系
    num = tools.get_num_font('06d91562.woff')
    for key in num:
        if key in res:
            res = res.replace(key, str(num[key]))
    html = etree.HTML(res)
    # 地址
    address = html.xpath(
        './/div[@id="basic-info"]//div[@class="expand-info address"]//div[@id="J_map-show"]//span[@class="item"]//text()')
    address = [x.replace(' ', '') for x in address]
    address = list(filter(None, address))
    address_real = ''
    for f in address:
        address_real += f

    print(price_unit)
    print(commentScore)
    print(shopName)
    print(address_real)
    print(tel_phone)
    print('评论条数:', count_comment)
    print('商家基本信息获取完毕')
    print('开始采集商家:{}评论信息'.format(shopName))
    # commments_info(url, count_comment)


def commments_info(url, count_comment):
    '''
    爬取评论信息
    1、获取加密字体对应关系
    2、替换
    3、提取字段
    @param url:商铺详情页 str
    @param count_comment:评论条数 int
    @return:
    '''
    font_map_df = get_font_map_data(url)
    if not font_map_df.empty:
        font_map = dict(zip(list(font_map_df['class']), list(font_map_df['font'])))
        for i in range(1, math.ceil(count_comment / 15) + 1):
            print('评论第{}页'.format(i))
            url += '/review_all/p{}'.format(i)
            res = requests.get(url, headers=headers).content.decode()

            for key, value in font_map.items():
                res = res.replace('<svgmtsi class="{}"></svgmtsi>'.format(key),
                                  '<svgmtsi class="{}">{}</svgmtsi>'.format(key, value))
            # 数据解析
            html = etree.HTML(res)
            # 评论作者
            authors = html.xpath(
                './/div[@class="reviews-items"]//ul//li//div[@class="main-review"]//div[@class="dper-info"]//a[@class="name"]/text()')
            authors = [x.replace('\n', '').replace('\r', '').replace(' ', '') for x in authors]
            # 评论时间
            com_date = html.xpath(
                './/div[@class="reviews-items"]//ul//li//div[@class="main-review"]//div[@class="misc-info clearfix"]//span[@class="time"]/text()')
            com_date = [x.replace('\n', '').replace('\r', '').replace(' ', '') for x in com_date]
            com_date = [x[:10] + ' ' + x[11:] for x in com_date]

            # 评论内容
            all_comments = []
            # 评分内容
            all_score = []

            for i in range(1, 16):
                desc = html.xpath(
                    './/div[@class="reviews-items"]//ul//li[{}]//div[@class="main-review"]//div[@class="review-words Hide"]//text()'.format(
                        i))
                desc_list = [x.replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '') for x in desc]
                desc = ''
                for font in desc_list:
                    desc += font
                all_comments.append(desc)

                # 评分列表
                score_list = html.xpath(
                    './/div[@class="reviews-items"]//ul//li[{}]//div[@class="main-review"]//div[@class="review-rank"]//span[@class="score"]//text()'.format(
                        i))
                score_list = [x.replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '') for x in score_list]
                score_list = list(filter(None, score_list))
                all_score.append(score_list)

            print('评论作者：长度={}，数据={}'.format(len(authors), authors))
            print('评论描述：长度={}，数据={}'.format(len(all_comments), all_comments))
            print('评分时间：长度={}，数据={}'.format(len(all_score), all_score))
            print('评论时间：长度={}，数据={}'.format(len(com_date), com_date))
            time.sleep(10)

    else:
        print('没有获取到加密字体映射数据')


if __name__ == '__main__':
    url = shop_infos()
    # url = 'http://www.dianping.com/shop/G8KdwGcs7WDIJqhQ'
    # commments_info(url)

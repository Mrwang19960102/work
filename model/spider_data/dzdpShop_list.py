# -*- coding: utf-8 -*-
# @File:       |   dzdpShop_list.py
# @Date:       |   2020/12/31 10:09
# @Author:     |   ThinkPad
# @Desc:       |  
import os
import re
import time
import math
import copy
import random
import requests
import pandas as pd
from lxml import etree
from datetime import datetime
from multiprocessing import Pool
from model.spider_data import tools, conf
from model.spider_data.dao import dbmanager_dzdp
from model.spider_data.change_IP import change_ipdf, change_IP

headers = {
    'Cookie': '_lxsdk_cuid=173ff7d706188-077c53bf069b0e-7a1437-100200-173ff7d7062c8; _lxsdk=173ff7d706188-077c53bf069b0e-7a1437-100200-173ff7d7062c8; _hc.v=988add77-4561-fac0-8537-5c5e93a36451.1597719278; s_ViewType=10; aburl=1; __utma=1.1058588512.1597720339.1597720339.1597720339.1; __utmz=1.1597720339.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ctu=9b1f465040be0773106db2215a3dccfe8202cfd8432c82a331683c3ac2f8b056; fspop=test; cy=7; cye=shenzhen; ua=Song%E5%93%A5; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1610345032,1610415333,1610428148,1610515452; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1610515892; _lxsdk_s=176fa3391cd-190-2c6-d3b%7C%7C67',
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

# 列表页
headers_list = {
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36 Edg/88.0.705.62',
    'Cookie': '_lxsdk=177232c0259c8-0d4b57e89af59c8-51a2f73-100200-177232c025951; _lxsdk_cuid=177232c0259c8-0d4b57e89af59c8-51a2f73-100200-177232c025951; s_ViewType=10; _hc.v=e5b4b74a-1b1f-54dd-2d0c-1b6cc0fc8055.1612425530; dper=5c306da43ba500e1c29230b5f8d70333bc84e8d8ce3ef6906ab4051a01206c012bcac373748106fcf00cfe7978e7ba78c58159649da2365c8c70492037ee7b9504f76e03cad0f8f7554140f20ce97e82cf3018ebd18bb1440fcab4e3bf7d07d1; ua=Song%E5%93%A5; ctu=c6a16fefdaffcb0927e88c1a28a2fd7cbd59e65223c0b3bbdb009bc6e2f13ba9; fspop=test; cy=5; cye=nanjing; ll=7fd06e815b796be3df069dec7836c3df; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1612496386,1612502548,1612502592,1612505548; dplet=b89f1d2d950b1babf9c64c265ee2eb08; _lxsdk_s=17770a439f9-b43-f4d-304%7C%7C124; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1612507051',
    'Host': 'www.dianping.com'
}


def get_citylist():
    '''
    采集大众点评
    @return: 
    '''
    dataDf = pd.DataFrame()
    url = 'http://www.dianping.com/citylist'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Cookie': '_lxsdk_cuid=173ff7d706188-077c53bf069b0e-7a1437-100200-173ff7d7062c8; _lxsdk=173ff7d706188-077c53bf069b0e-7a1437-100200-173ff7d7062c8; _hc.v=988add77-4561-fac0-8537-5c5e93a36451.1597719278; s_ViewType=10; aburl=1; __utma=1.1058588512.1597720339.1597720339.1597720339.1; __utmz=1.1597720339.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ctu=9b1f465040be0773106db2215a3dccfe8202cfd8432c82a331683c3ac2f8b056; ua=Song%E5%93%A5; fspop=test; cy=160; cye=zhengzhou; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1611811621,1611884488,1611903467,1612152684; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1612152702; _lxsdk_s=1775bc9b6dd-2a2-ac7-04a%7C%7C11',
        'Host': 'www.dianping.com'
    }
    res = requests.get(url, headers=headers)
    if 200 == res.status_code:
        res = res.content.decode()
        html = etree.HTML(res)
        cityList_url = html.xpath('.//div[@class="findHeight"]//a/@href')
        cityList_name = html.xpath('.//div[@class="findHeight"]//a/text()')
        cityList_url = [x.replace('//www.dianping.com/', '') for x in cityList_url]
        cityList_name = [x.replace('市', '') for x in cityList_name]
        dataDf = pd.DataFrame({
            'city_pinyin': cityList_url,
            'city_name': cityList_name,
        })
    return dataDf


def get_all_shops_list(pro_name):
    '''
    获取大众点评中每一个品类下面的所有商家列表
    @param pro_name:省份名称
    @return:
    '''
    print('开始采集省份={}的数据信息'.format(pro_name))
    pro_city_df = dbmanager_dzdp.get_pro_city(pro_name)
    city_name_pinyin = get_citylist()
    if not pro_city_df.empty and not city_name_pinyin.empty:
        pro_city_df = pd.merge(pro_city_df, city_name_pinyin, on=['city_name'], how='left')
    if not pro_city_df.empty:
        for index, info in pro_city_df.iterrows():
            city_pinyin = info['city_pinyin']
            city_name = info['city_name']
            url = 'http://www.dianping.com/{}/ch10/g110'.format(city_pinyin)
            print('开始采集城市={}的数据信息'.format(city_name))
            '''
            查询方法：
            1:---》按照行政区来进行数据查询
            0：---》按照类型下面的小分类方式进行查询
            备注：建议按照行政区
            '''
            select_method = 1
            if 0 == select_method:
                pass
            elif 1 == select_method:
                # 获取城市的所有行政区 和 该城市已经采集过的行政区
                regiondf = get_city_region(url)
                print('采集到city={}的所有行政区为{}'.format(city_name, regiondf['area_name'].tolist()))
                cityArea_already = dbmanager_dzdp.already_cityArea(city_name)
                # 筛选出需要采集的城市区域
                if not cityArea_already.empty:
                    spider_cityArea = regiondf[~regiondf['area_name'].isin(cityArea_already['area_name'].tolist())]
                else:
                    spider_cityArea = regiondf
            else:
                spider_cityArea = pd.DataFrame({
                    'area_url': [url],
                    'area_name': [city_name]
                })
            if not spider_cityArea.empty:
                print('需要采集的为：{}'.format(spider_cityArea))
                for index, info in spider_cityArea.iterrows():
                    area_url = info['area_url']
                    area_name = info['area_name']
                    df_list = []
                    p_count = page_count(area_url)
                    for i in range(1, int(p_count) + 1):
                        parse_url = area_url + 'p{}'.format(str(i))
                        print('city={},area={},采集第{}页,url={}'.format(city_name, area_name, i, parse_url))
                        try:
                            # program_time = datetime.now()
                            # global ip_df
                            # global s_time
                            # if (program_time - s_time).seconds > 60 * 13:
                            #     ip_df = change_ipdf()
                            #     s_time = program_time
                            #     print('重新加载')
                            # proxies = change_IP(ip_df)
                            # res = requests.get(parse_url, headers=headers_list,proxies=proxies)
                            # print('status={},proxies={}'.format(res.status_code, proxies))
                            res = requests.get(parse_url, headers=headers_list)
                            print('status={},proxies='.format(res.status_code))
                            res = res.content.decode()
                            while '验证中心' in str(res):
                                input('请向右拖动滑块')
                                # res_new = requests.get(parse_url, headers=headers_list,proxies=proxies)
                                # print('status={},proxies={}'.format(res_new.status_code, proxies))
                                res_new = requests.get(parse_url, headers=headers_list)
                                print('status={},proxies='.format(res_new.status_code))
                                res = res_new.content.decode()
                            html = etree.HTML(res)
                            shop_name_list = html.xpath('.//div[@class="tit"]/a//h4//text()')
                            shop_url_list = html.xpath('.//div[@class="tit"]/a/@href')
                            shop_url_list = [x for x in shop_url_list if x.startswith('http://www.dianping.com/shop/')]
                            shop_score_list = html.xpath('.//div[@class="nebula_star"]/div[2]/text()')
                            shop_comments_list = html.xpath('.//div[@class="comment"]/a[@class="review-num"]//text()')
                            shop_comments_list = [x.replace('\n', '').replace(' ', '') for x in shop_comments_list]
                            print(len(shop_name_list), shop_name_list)
                            print(len(shop_url_list), shop_url_list)
                            # print(len(shop_score_list), shop_score_list)
                            # print(len(shop_comments_list), shop_comments_list)
                            every_page_df = pd.DataFrame({
                                'shop_name': shop_name_list,
                                'url': shop_url_list,
                            })
                            every_page_df['shop_id'] = every_page_df['url'].apply(
                                lambda x: x.replace('http://www.dianping.com/shop/', ''))
                            df_list.append(every_page_df)
                            # time.sleep(3)
                        except Exception as e:
                            print('异常', e)
                        time.sleep(5)
                    if df_list:
                        allDf = pd.concat(df_list, axis=0)
                        allDf['city'] = city_name
                        allDf['shop_type'] = '火锅'
                        if 1 == select_method:
                            allDf['region'] = area_name
                        in_bo = dbmanager_dzdp.save_dzdp_shoplist(allDf, select_method)
                        print('Save to {},shape={},status={}'.format(conf.dzdp_shop_table, allDf.shape[0], in_bo))

            else:
                print('city={}没有需要采集的行政区'.format(city_name))


def get_city_region(url):
    '''
    获取城市的所有行政区
    @param url: 城市url
    @return:
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Cookie': 's_ViewType=10; _lxsdk_cuid=1776b479ff9c8-02fe0c115d7873-7a1437-100200-1776b479ff917; _lxsdk=1776b479ff9c8-02fe0c115d7873-7a1437-100200-1776b479ff917; _hc.v=560e1bcd-38c8-dafc-36fb-ba7a02368013.1612413651; fspop=test; cy=5; cye=nanjing; ctu=c6a16fefdaffcb0927e88c1a28a2fd7c8a4a56842d548900dec7c3150847539f; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; dper=5c306da43ba500e1c29230b5f8d70333995867679261f0cb0bbecf84d8414a30935994b2240c8344d48db7cd4b540af1e2b8552089b4e013f3a73c3bce9736956fdb548761903bc0f002b48f544d1fcd9e1b0fa07b4a620d471058a3b9af6b76; ua=Song%E5%93%A5; ll=7fd06e815b796be3df069dec7836c3df; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1612425507,1612487239,1612494540,1612501794; dplet=0382bf098b5c9d2829c4137c71fc7a5d; _lxsdk_s=17770b889cd-0fd-2e8-d2a%7C%7C77; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1612506807',
        'Host': 'www.dianping.com'
    }
    df = pd.DataFrame()
    print(url)
    res = requests.get(url, headers=headers)
    if 200 == res.status_code:
        res = res.content.decode()
        while '页面不存在' in str(res):
            input('url={},请向右拖动滑块'.format(url))
            res = requests.get(url, headers=headers).content.decode()
        html = etree.HTML(res)
        region_list = html.xpath('.//div[@id="region-nav"]//a/@href')
        region_name = html.xpath('.//div[@id="region-nav"]//a//span/text()')
        df = pd.DataFrame({
            'area_name': region_name,
            'area_url': region_list,
        })

    return df


def page_count(url):
    '''
    获取一共的页数
    @param url: 要确定页数的链接地址
    @return:
    '''
    p_count = None
    res = requests.get(url, headers=headers_list)
    if 200 == res.status_code:
        while '页面不存在' in str(res):
            input('url={},请向右拖动滑块'.format(url))
            res = requests.get(url, headers=headers_list).content.decode()
        res = res.content.decode()
        html = etree.HTML(res)
        page_list = html.xpath('.//div[@class="page"]/a//text()')
        page_list = [x for x in page_list if x != '下一页']
        if page_list:
            p_count = page_list[-1]
        else:
            p_count = 1
    return p_count


def get_small_classify(url):
    '''
    获取该分类下面的所有小分类
    @param url:
    @return:
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Cookie': 'navCtgScroll=0; _lxsdk_cuid=173ff7d706188-077c53bf069b0e-7a1437-100200-173ff7d7062c8; _lxsdk=173ff7d706188-077c53bf069b0e-7a1437-100200-173ff7d7062c8; _hc.v=988add77-4561-fac0-8537-5c5e93a36451.1597719278; s_ViewType=10; aburl=1; __utma=1.1058588512.1597720339.1597720339.1597720339.1; __utmz=1.1597720339.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ctu=9b1f465040be0773106db2215a3dccfe8202cfd8432c82a331683c3ac2f8b056; cye=nanjing; ua=Song%E5%93%A5; fspop=test; cy=5; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1605582236,1605591555,1605605140,1606371418; dplet=bffd22a916442e317384b63424dd9d36; dper=2d0d9e4d298453f1a91fc71b0b41074e1a957afe928bf1632fe20ad2be3a57b3227193234621812bf9fe038bf45a2c6c79d456664de463d73bd11b1a93e14ed1f480b7919d8aaeeb3bc5eb1b5c24a6e529f62a1f321419d7c45761f0c435ad8d; ll=7fd06e815b796be3df069dec7836c3df; uamo=15195903925; _lxsdk_s=17603329d06-d15-c9e-711%7C%7C208; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1606372328',
        'Host': 'www.dianping.com'
    }
    small_classify = []
    res = requests.get(url, headers=headers)
    if 200 == res.status_code:
        res = res.content.decode()
        while '页面不存在' in str(res):
            input('url={},请向右拖动滑块'.format(url))
            res = requests.get(url, headers=headers).content.decode()
        html = etree.HTML(res)
        small_classify = html.xpath('.//div[@id="classfy-sub"]//a/@href')[1:]

    return small_classify


'----------------------------------------------------------------------------------------------------------------------'


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
                score_list = [x.replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '') for x in
                              score_list]
                score_list = list(filter(None, score_list))
                all_score.append(score_list)

            print('评论作者：长度={}，数据={}'.format(len(authors), authors))
            print('评论描述：长度={}，数据={}'.format(len(all_comments), all_comments))
            print('评分时间：长度={}，数据={}'.format(len(all_score), all_score))
            print('评论时间：长度={}，数据={}'.format(len(com_date), com_date))
            time.sleep(12)

    else:
        print('没有获取到加密字体映射数据')


def allfile_toexcel():
    '''
    读取所有的excel文件合并为一个excel文件
    @return:
    '''
    all_df = pd.DataFrame()
    writer = pd.ExcelWriter('', engine='xlsxwriter', options={'strings_to_urls': False})
    all_df.to_excel(writer, index=False)
    writer.close()


if __name__ == '__main__':
    pro_name = '山东省'

    # ip_df = change_ipdf()
    # s_time = datetime.now()
    get_all_shops_list(pro_name)

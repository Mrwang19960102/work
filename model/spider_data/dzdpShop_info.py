# -*- coding: utf-8 -*-
# @File:       |   dzdpShop_info.py
# @Date:       |   2020/8/31 9:31
# @Author:     |   ThinkPad
# @Desc:       |  大众点评 店铺详情
import os
import re
import time
import math
import copy
import random
import json
import requests
import pandas as pd
from lxml import etree
from datetime import datetime
from multiprocessing import Pool
from model.spider_data import tools, conf
from model.spider_data.dao import dbmanager_dzdp
from model.spider_data.change_IP import change_ipdf, change_IP

headers = {
    'Host': 'www.dianping.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Cookie': '_lxsdk_cuid=173ff7d706188-077c53bf069b0e-7a1437-100200-173ff7d7062c8; _lxsdk=173ff7d706188-077c53bf069b0e-7a1437-100200-173ff7d7062c8; _hc.v=988add77-4561-fac0-8537-5c5e93a36451.1597719278; s_ViewType=10; aburl=1; __utma=1.1058588512.1597720339.1597720339.1597720339.1; __utmz=1.1597720339.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ctu=9b1f465040be0773106db2215a3dccfe8202cfd8432c82a331683c3ac2f8b056; ua=Song%E5%93%A5; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; fspop=test; cy=5; cye=nanjing; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1610515452,1610947975,1610951352,1611018359; _lxsdk_s=177193e0cc1-b8f-b01-e49%7C%7C18; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1611036239; dplet=21bc45507899eff9265b403f5385ad3a; dper=fc09c43f16b3c496cb53b49958290276fc145177ba67784da69df8e66dec0d8f66089286f63eb961b16c6362aa4e57760106cdd3d096a2700bb9b3f18bbfa9b3c1488e04f1810abcbd6d042b696797e292392060f2669931f7ae8c4c8b33fa54; ll=7fd06e815b796be3df069dec7836c3df; uamo=15195903925'
}



# 手机号等商铺详情信息采集
def spider_info():
    '''
    采集商铺的信息
    @return:
    '''
    # 获取结果表中已经获取过的手机号
    shopInfo_already = dbmanager_dzdp.get_alreadyshop_info()
    # 获取大众点评店铺列表表的全部店铺id
    shopall_df = dbmanager_dzdp.get_all_shop()
    '''
    筛选出需要采集的店铺
    '''
    if not shopInfo_already.empty:
        need_shop_df = shopall_df[~shopall_df['shop_id'].isin(shopInfo_already['shop_id'].tolist())]
    else:
        need_shop_df = shopall_df
    if not need_shop_df.empty:
        '''
        采集手机号
        '''
        all_data = []
        for index, info in need_shop_df.iterrows():
            every_data = []
            shop_id = info['shop_id']
            shop_url = info['url']
            phone_list = phone_api(shop_id)
            # phone_list = shop_infos(shop_url)
            if phone_list:
                every_data.append(shop_id)
                every_data.append(phone_list)
                all_data.append(every_data)
                print(every_data)
            if len(all_data) == 10:
                save_df = pd.DataFrame(all_data, columns=['shop_id', 'phone'])
                save_df['phone'] = save_df['phone'].astype(str)
                inbo = dbmanager_dzdp.save_dzdp_phone_data(save_df)
                print('save data to {}，shape={},status={}'.format(conf.dzdp_shop_phone_table, save_df.shape[0], inbo))
                all_data = []
            # time.sleep(1)


def spider_info_pool():
    '''
    采集商铺的信息
    @return:
    '''
    # 获取结果表中已经获取过的手机号
    shopInfo_already = dbmanager_dzdp.get_alreadyshop_info()
    # 获取大众点评店铺列表表的全部店铺id
    shopall_df = dbmanager_dzdp.get_all_shop()
    '''
    筛选出需要采集的店铺
    '''
    if not shopInfo_already.empty:
        need_shop_df = shopall_df[~shopall_df['shop_id'].isin(shopInfo_already['shop_id'].tolist())]
    else:
        need_shop_df = shopall_df
    if not need_shop_df.empty:
        '''
        采集手机号
        '''
        # print(need_shop_df)
        all_data = []
        pool = Pool(processes=5)
        for index, info in need_shop_df.iterrows():
            every_data = []
            shop_id = info['shop_id']
            shop_url = info['url']
            phone_list = pool.map(shop_infos, (shop_url,))
            if phone_list:
                every_data.append(shop_id)
                every_data.append(phone_list)
                all_data.append(every_data)
                print(every_data)
            if len(all_data) == 10:
                save_df = pd.DataFrame(all_data, columns=['shop_id', 'phone'])
                save_df['phone'] = save_df['phone'].astype(str)
                inbo = dbmanager_dzdp.save_dzdp_phone_data(save_df)
                print('save data to {}，shape={},status={}'.format(conf.dzdp_shop_phone_table, save_df.shape[0], inbo))
                all_data = []
            time.sleep(2)

        pool.close()
        pool.join()


def phone_api(shop_id):
    '''
    获取手机号的api接口
    @return:
    '''
    phone_list = []
    url = 'http://www.dianping.com/ajax/json/shopDynamic/basicHideInfo?shopId={}'.format(shop_id)
    print(url)
    program_time = datetime.now()
    global ip_df
    global s_time
    if (program_time - s_time).seconds > 60 * 13:
        ip_df = change_ipdf()
        s_time = program_time
        print('重新加载')
    proxies = change_IP(ip_df)
    res = requests.get(url, headers=headers, proxies=proxies)
    print(res.status_code, proxies)
    if 200 == res.status_code:
        res = res.content.decode()
        while '验证' in res:
            input('滑动验证：{}'.format(url))
            res_new = requests.get(url, headers=headers, proxies=proxies)
            if 200 == res_new.status_code:
                res = res_new.content.decode()
        # 破解手机号数字字体加密
        for k, num in conf.num_dict.items():
            res = res.replace('&#x' + k, str(num))
        info_json = json.loads(res)
        info_json = info_json['msg']['shopInfo']
        phone1 = info_json['phoneNo']
        phone2 = info_json['phoneNo2']
        phone1 = phone1.replace('<d class="num">', '')
        phone1 = phone1.replace('</d>', '')
        phone1 = phone1.replace(';', '')
        phone2 = phone2.replace('<d class="num">', '')
        phone2 = phone2.replace('</d>', '')
        phone2 = phone2.replace(';', '')
        if phone1:
            phone_list.append(phone1)
        if phone2:
            phone_list.append(phone2)
        if phone1 is None and phone2 is None:
            phone_list.append(None)
    return phone_list


def shop_infos(url):
    '''
    商家信息:名称、地址、电话等信息
    '''
    telephone = ''
    program_time = datetime.now()
    global ip_df
    global s_time
    if (program_time - s_time).seconds > 60 * 13:
        ip_df = change_ipdf()
        s_time = program_time
        print('重新加载')
    proxies = change_IP(ip_df)
    # res = requests.get(url, headers=headers)
    # print('状态码：{},proxies=,url={}'.format(res.status_code, url))
    res = requests.get(url, headers=headers, proxies=proxies)
    print('状态码：{},proxies={},url={}'.format(res.status_code, proxies, url))
    if 200 == res.status_code:
        res = res.content.decode()
        if '验证中心' in str(res):
            input('请向右拖动滑块')
            res = requests.get(url, headers=headers, proxies=proxies).content.decode()
        elif '页面不存在' in str(res):
            return

        # 获取数字加密映射关系
        num = tools.get_num_font('c67e58f2.woff')
        for key in num:
            if key in res:
                res = res.replace(key, str(num[key]))
        html = etree.HTML(res)

        # 人均价格
        price = html.xpath('.//div[@id="basic-info"]//div[@class="brief-info"]//span[@id="avgPriceTitle"]//text()')
        price_unit = ''
        for n in price:
            price_unit += n

        # 评论条数
        com_count = html.xpath(
            './/div[@id="basic-info"]//div[@class="brief-info"]//span[@id="reviewCount"]//text()')
        com_count = [x.replace('\n', '').replace('\r', '').replace(' ', '') for x in com_count]
        com_count = list(filter(None, com_count))
        com_count = [x.replace('条评价', '') for x in com_count]
        com_count = list(filter(None, com_count))
        count_comment = ''
        for c in com_count:
            count_comment += c
        # count_comment = int(count_comment)
        # 公共评分
        comment_score = html.xpath(
            './/div[@id="basic-info"]//div[@class="brief-info"]//span[@id="comment_score"]//text()')
        comment_score = [x.replace('\n', '').replace('\r', '').replace(' ', '') for x in comment_score]
        comment_score = list(filter(None, comment_score))
        commentScore = ''
        for s in comment_score:
            commentScore += s

        # 电话
        num_list = html.xpath('.//div[@id="basic-info"]//p[@class="expand-info tel"]//text()')
        num_list = [x.replace('\n', '').replace('\r', '').replace(' ', '').replace('电话：', '') for x in num_list]
        num_list = list(filter(None, num_list))

        for i in num_list:
            telephone += i
        if '\xa0' in telephone:
            telephone = telephone.split('\xa0')

    return telephone

'-------------------------------------------------------------------------------------------------------------------------'
def get_comment_map(svg_link, status=0):
    '''
    根据样式链接获取每个字体对应的映射关系
    @param svg_link: 链接
    @param status: svg标签样式不同 0：标签为textlength  1:表示：标签为y
    @return: 字典映射
    '''''
    if 0 == status:
        res = requests.get(svg_link, headers=headers).content
        html = etree.HTML(res)
        href_list = html.xpath('.//defs//path/@d')
        href_list = [x.replace('M0', '').replace('H600', '').replace(' ', '') for x in href_list]
        tag_message = re.compile('>(.*)</text')
        tag_message = tag_message.findall(res.decode())
    elif 1 == status:
        res = requests.get(svg_link, headers=headers).content.decode()
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
    res = requests.get(url, headers=headers).content.decode()
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
        css_res = requests.get(css_link, headers=headers).text
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
    ip_df = change_ipdf()
    s_time = datetime.now()
    # 获取手机号
    spider_info()
    # phone_api('l3RVaDVUfD5N5uD8')

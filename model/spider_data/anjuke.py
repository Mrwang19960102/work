# -*- coding: utf-8 -*-
# @File:       |   anjuke.py 
# @Date:       |   2020/8/28 14:13
# @Author:     |   ThinkPad
# @Desc:       |  安居客数据爬取
import re
import time
import requests
from datetime import datetime
import pandas as pd
import numpy as np
from lxml import etree
from model.spider_data import tools

headers = {
    'referer': 'https://nj.zu.anjuke.com/fangyuan/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}


def rent_houses(url, p):
    '''
    根据url爬取租房信息
    :param url:
    :return:
    '''
    print(url)
    res = requests.get(url, headers=headers)
    if '请在五分钟内完成验证' in res.text:
        print('滑动验证')
        pass
    try:
        res = res.content.decode()
        html = etree.HTML(res)
        bs64_str = re.findall("charset=utf-8;base64,(.*?)'\)", res)[0]
        # 房屋名称
        house_names = html.xpath('.//div[@class="zu-itemmod"]//div[@class="zu-info"]//h3//a//b/text()')
        house_names = [tools.get_page_show_ret(i, bs64_str) for i in house_names]
        # 房屋价格
        house_price = html.xpath('.//div[@class="zu-itemmod"]//div[@class="zu-side"]//p//strong//b/text()')

        house_price = [tools.get_page_show_ret(i, bs64_str) for i in house_price]
        # 价格单位
        price_unit = html.xpath('.//div[@class="zu-itemmod"]//div[@class="zu-side"]//p/text()')
        # 户型
        door_model_shi = html.xpath(
            './/div[@class="zu-itemmod"]//div[@class="zu-info"]//p[@class="details-item tag"]//b[@class="strongbox"][1]/text()')
        door_model_shi = [tools.get_page_show_ret(i, bs64_str) for i in door_model_shi]
        door_model_ting = html.xpath(
            './/div[@class="zu-itemmod"]//div[@class="zu-info"]//p[@class="details-item tag"]//b[@class="strongbox"][2]/text()')
        door_model_ting = [tools.get_page_show_ret(i, bs64_str) for i in door_model_ting]

        # 面积
        areas = html.xpath(
            './/div[@class="zu-itemmod"]//div[@class="zu-info"]//p[@class="details-item tag"]//b[@class="strongbox"][3]/text()')
        areas = [tools.get_page_show_ret(i, bs64_str) for i in areas]
        # 联系人
        contact = html.xpath('.//div[@class="zu-itemmod"]//div[@class="zu-info"]//p[@class="details-item tag"]/text()')
        contact = [i.strip() for i in contact]
        contact = [x for x in contact if x != ""]
        contact = [i for i in contact if (1 + contact.index(i)) % 5 == 0]
        # 小区名字
        community_names = html.xpath(
            './/div[@class="zu-itemmod"]//div[@class="zu-info"]//address[@class="details-item"]//a/text()')
        # 地址
        address = html.xpath(
            './/div[@class="zu-itemmod"]//div[@class="zu-info"]//address[@class="details-item"]/text()')
        address = [i.strip() for i in address]
        address = [x for x in address if x != ""]
        details = []
        for i in range(1, 61):
            x = './/div[@class="zu-itemmod"][' + str(
                i) + ']//div[@class="zu-info"]//p[@class="details-item bot-tag"]//span/text()'
            details.append(html.xpath(x))

        print('名称', len(house_names), house_names)
        print('价格', len(house_price), house_price)
        print('单位', len(price_unit), price_unit)
        print('房间室数', len(door_model_shi), door_model_shi)
        print('房间厅数', len(door_model_ting), door_model_ting)
        print('房屋面积', len(areas), areas)
        print('联系人', len(contact), contact)
        print('小区名字', len(community_names), community_names)
        print('地址', len(address), address)
        print('详情', len(details), details)
        data_df = pd.DataFrame({
            '名称': house_names,
            '价格': house_price,
            '单位': price_unit,
            '房间室数': door_model_shi,
            '房间厅数': door_model_ting,
            '房屋面积': areas,
            '联系人': contact,
            '小区名字': community_names,
            '地址': address,
            '详情': details
        })

        data_df['city'] = '上海市'+'浦东'
        data_df.to_excel('./data_source/第{}页.xlsx'.format(p), index=False)
        time.sleep(10)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    for i in range(1, 51):
        print('第{}页'.format(i))
        url = 'https://sh.zu.anjuke.com/fangyuan/pudong/p' + str(i) + '/'
        print(url)
        rent_houses(url, i)

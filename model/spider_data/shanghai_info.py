# -*- coding: utf-8 -*-
# @File:       |   shanghai_info.py 
# @Date:       |   2020/10/14 9:41
# @Author:     |   ThinkPad
# @Desc:       |  
import re
import time

import requests
import pandas as pd
import numpy as np
from datetime import datetime
from lxml import etree

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Cookie': '_gscu_51414243=02486133gbgvum10; ASP.NET_SessionId=xuxs5455sya51eam2fsj5q55; __CSRFCOOKIE=73145f27-6950-414d-b5bf-de0dbacadf6b; _gscbrs_51414243=1; _gscs_51414243=02639495lx3oxr10|pv:1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Host': 'xxgk.shhk.gov.cn'
}

headers_putuo = {
    'Cookie': 'zh_choose=s; _gscu_1035545933=02485954jw30qn62; _gscbrs_1035545933=1; _gscs_1035545933=02664062hhw01p62|pv:1; _pk_id.56.2981=f3834c13e1b630c3.1602485955.2.1602664062.1602664062.; _pk_ses.56.2981=*',
    'Host': 'www.shpt.gov.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}


def spider_info_list():
    '''
    爬取上海市虹口去人民政府数据列表
    @return:
    '''
    all_df = []
    for i in range(1, 3):
        print('第{}页'.format(i))
        url = 'http://xxgk.shhk.gov.cn/hkxxgk/Depart/Default.aspx?categorynum=002&deptcode=001002&Paging={}'.format(
            str(i))
        try:
            res = requests.get(url, headers=headers).content.decode()
            html = etree.HTML(res)
            directory_list = html.xpath('.//tr[@class="ewb-tr"]//td[1]//a//text()')
            directory_list = [x[1:-1] for x in directory_list]
            title_list = html.xpath('.//tr[@class="ewb-tr"]//td[2]//span//a//text()')
            date_list = html.xpath('.//tr[@class="ewb-tr"]//td[3]//text()')
            date_list = [x.replace('\r', '').replace('\n', '').replace(' ', '') for x in date_list]
            url_list = html.xpath('.//tr[@class="ewb-tr"]//td[4]//a/@href')
            url_list = ["http://xxgk.shhk.gov.cn/" + x for x in url_list]

            print(directory_list)
            print(title_list)
            print(date_list)
            print(url_list)
            every_df = pd.DataFrame({
                '目录': directory_list, '标题': title_list, '日期': date_list, '链接': url_list
            })
            all_df.append(every_df)
            time.sleep(5)
        except Exception as e:
            print(e)
            break
    if all_df:
        df = pd.concat(all_df, axis=0)
        df.to_excel('./data_export/上海市政府数据.xlsx', index=False)


def get_details():
    '''
    获取详情
    @return:
    '''
    need_data_df = pd.read_excel('./data_export/上海市政府数据.xlsx')
    all_data = []
    for index, info in need_data_df.iterrows():
        results = None
        every_data = []
        title = info['标题']
        url = info['链接']
        try:
            print(url)
            res = requests.get(url, headers=headers).content.decode()
            html = etree.HTML(res)
            # comments = html.xpath('.//div[@class="DetailMainContainer"]//text()')
            # comments = [x.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa0', '') for x in
            #             comments]
            # comments = str(list(filter(None, comments)))

            comments = html.xpath('.//div[@class="DetailMainContainer"]')
            table = etree.tostring(comments[0], encoding='utf-8').decode()
            df = pd.read_html(table, encoding='utf-8', header=0)[0]
            # 转换成列表嵌
            results = list(df.T.to_dict().values())[0]

            time.sleep(5)
        except Exception as e:
            print(e)
            break
        finally:
            every_data.append(title)
            every_data.append(results)
            all_data.append(every_data)
            print(every_data)
    if all_data:
        comments_df = pd.DataFrame(all_data, columns=['标题', '内容'])
        infos_df = pd.merge(need_data_df, comments_df, on=['标题'], how='left')
        infos_df.to_excel('./data_export/上海市政府数据2.xlsx', index=False)


def area_hongkou():
    '''
    上海市虹口区数据
    @return:
    '''
    # spider_info_list()
    get_details()


def area_putuo():
    '''
    上海市普陀区数据
    @return:
    '''
    # get_data_list()

    get_details_putuo()


def get_data_list():
    '''
    获取普陀区信息列表数据
    @return:
    '''
    url = 'http://www.shpt.gov.cn/shpt/gkfgw-gkmulu/index.html'
    res = requests.get(url, headers=headers_putuo).content.decode()
    html = etree.HTML(res)
    index_code = html.xpath('.//td[@class="col-20"]/text()')[1:]
    print(len(index_code), index_code)
    info_name = html.xpath('.//td[@class="col-30"]//a/@title')
    print(len(info_name), info_name)
    url_list = html.xpath('.//td[@class="col-30"]//a/@href')
    url_list = ['http://www.shpt.gov.cn/' + x for x in url_list]
    print(len(url_list), url_list)
    com_desc = html.xpath('.//td[@class="col-35"]/text()')[1:]
    com_desc = [x.replace('\n', '').replace(' ', '') for x in com_desc]
    print(len(com_desc), com_desc)
    pro_date = html.xpath('.//td[@class="col-15"]/text()')[1:]
    pro_date = [x.replace('\n', '').replace(' ', '') for x in pro_date]
    print(len(pro_date), pro_date)
    df = pd.DataFrame({
        '索引号': index_code,
        '信息名称': info_name,
        '链接': url_list,
        '内容描述': com_desc,
        '产生日期': pro_date
    })


def get_details_putuo():
    '''
    获取普陀区数据详情内容
    @return:
    '''
    url = 'http://www.shpt.gov.cn/shpt/gkfgw-fwshenpi/20201012/525560.html'
    res = requests.get(url, headers=headers_putuo).content.decode()
    html = etree.HTML(res)
    infos = html.xpath('.//div[@id="ivs_content"]//text()')
    infos = [x.replace('\n', '').replace(' ', '').replace('\xa0', '') for x in infos]
    infos = list(filter(None, infos))
    print(infos)

    # infos = html.xpath('.//div[@id="ivs_content"]')
    # print(infos)
    # table = etree.tostring(infos[0], encoding='utf-8').decode()
    # df = pd.read_html(table, encoding='utf-8', header=0)[0]
    # print(str(df))
    # df1 = pd.DataFrame({
    #     'url':[url],
    #     '21':[str(df)]
    # })
    # print(df1)



if __name__ == '__main__':
    area_putuo()

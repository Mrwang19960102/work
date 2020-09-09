# -*- coding: utf-8 -*-
# @File:       |   jingzhufupin.py 
# @Date:       |   2020/9/7 15:34
# @Author:     |   ThinkPad
# @Desc:       |  
import jieba
import json
import time
import requests
from lxml import etree
import pandas as pd

headers = {
    'Referer': 'http://sousuo.gov.cn/a.htm?t=zhengce',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Cookie': 'wdcid=5b8aca6a7a3bf70b; __auc=e2855b05173d6322fb2bbc01ba1; wdses=723db7dea12ac85f; __asc=9109419817467770a41f6b4c84c; allmobilize=mobile; gwdshare_firstime=1599463755798; wdlast=1599463847'
}


def get_info():
    df = pd.read_excel('./data_export/guo_df.xlsx')
    all_url = list(df['url'])
    all_data = []
    for url in all_url:
        print(url)
        every_data = []
        # url = 'http://www.gov.cn/zhengce/2019-07/23/content_5413850.htm'
        headers = {
            'Referer': 'http://sousuo.gov.cn/a.htm?t=zhengce',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'Cookie': 'wdcid=5b8aca6a7a3bf70b; __auc=e2855b05173d6322fb2bbc01ba1; wdses=723db7dea12ac85f; __asc=9109419817467770a41f6b4c84c; allmobilize=mobile; gwdshare_firstime=1599463755798; wdlast=1599463847'
        }
        try:
            res = requests.get(url, headers=headers).content.decode()
            html = etree.HTML(res)
            title = html.xpath('.//div[@class="wrap"]//tbody//tr//td//table//tbody//tr[3]//td[2]//text()')
            title = [x.replace('\n', '').replace('\r', '').replace(' ', '') for x in title]
            title = list(filter(None, title))[0]
            # print(title)
            date = html.xpath('.//div[@class="wrap"]//tbody//tr//td//table//tbody//tr[4]//td[4]//text()')
            date = [x.replace('\n', '').replace('\r', '').replace(' ', '') for x in date][0]
            # date = list(filter(None, date))
            # print(date)
            content = html.xpath('.//div[@class="wrap"]//table[2]//tbody//tr//td//table//tbody//tr//td//text()')
            # content = html.xpath('.//div[@class="article-colum"]//div[@class="pages_content"]//text()')
            content = [x.replace('\n', '').replace('\t', '').replace('\xa0', '').replace('\r', '').replace(' ', '') for
                       x in content]
            content = list(filter(None, content))
            all_content = ''
            for i in content:
                all_content += i

            every_data.append(url)
            every_data.append('国务院')
            every_data.append(title)
            every_data.append(date)
            every_data.append(all_content)
            all_data.append(every_data)
            print(every_data)
            time.sleep(2)
        except Exception as e:
            print(e)

    dataDf = pd.DataFrame(all_data, columns=['url', '发布机构', '标题', '时间', '内容'])
    dataDf.to_excel('./data_export/国务院.xlsx', index=False, encoding='utf-8-sig')


def get_all_url():
    '''
    获取所有的新闻url
    @return:
    '''
    guwData = []
    zhongyangData = []
    for i in range(21):
        print('第{}页'.format(i + 1))
        url = 'http://sousuo.gov.cn/data?t=zhengce_zy_gw&q=%E7%B2%BE%E5%87%86%E6%89%B6%E8%B4%AB&timetype=timezd&mintime=&maxtime=&searchfield=title:content:summary&pcodeJiguan=&puborg=&pcodeYear=&pcodeNum=&filetype=&p={}&n=5&sort=score'.format(
            i)
        res = requests.get(url, headers=headers).json()
        zhongyang_data = res['searchVO']['catMap']['zhongyangfile']['listVO']
        if zhongyang_data:
            for zhongyang in zhongyang_data:
                url_z = zhongyang['url']
                zhongyangData.append(url_z)
        gwy_data = res['searchVO']['catMap']['gongwen']['listVO']
        if gwy_data:
            for gwy in gwy_data:
                url_g = gwy['url']
                guwData.append(url_g)
        print(len(guwData), guwData)
        print(len(guwData), zhongyangData)
        time.sleep(5)
    print(guwData)
    print(zhongyangData)
    zhong_df = pd.DataFrame({
        'url': zhongyangData
    })
    guo_df = pd.DataFrame({
        'url': guwData
    })
    zhong_df.to_excel('./data_export/zhong_df.xlsx', index=False)
    guo_df.to_excel('./data_export/guo_df.xlsx', index=False)


if __name__ == '__main__':
    # 获取所有连接
    get_all_url()
    # 解析数据
    get_info()
    data_df = pd.read_excel('./data_source/中央国务院数据.xlsx')
    # 词频
    all_com = list(data_df['内容'])
    all_com = [x.replace('\n', '').replace('\r', '').replace(' ', '') for x in all_com]
    allStr = ''
    for com in all_com:
        allStr += com
    allD = jieba.lcut(allStr)
    # 读取暂停词
    stopwords = [line.strip() for line in open('./data_source/CS.txt', encoding='utf-8').readlines()]
    print(allD)
    print(stopwords)
    count_data = {}
    n = 1
    for word in allD:
        print('第{}个,word:{},一共{}个'.format(n, word, len(allD)))
        if word not in stopwords:
            if word not in list(count_data.keys()):
                c = 0
                for e in allD:
                    if word == e:
                        c += 1
                count_data[word] = c
                print(count_data)
        n += 1

    df = pd.DataFrame({
        'date': list(count_data.keys()),
        'count': list(count_data.values()),
    })
    df.to_excel('./data_export/词频.xlsx', index=False)

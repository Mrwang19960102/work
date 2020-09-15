# -*- coding: utf-8 -*-
# @File:       |   dongfangcaifu.py 
# @Date:       |   2020/9/10 13:42
# @Author:     |   ThinkPad
# @Desc:       |   东方财富网数据抓取
import re
import time
import requests
from lxml import etree
import pandas as pd
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Referer': 'http://guba.eastmoney.com/list,zssh000001.html',
    'Cookie': 'qgqp_b_id=55e79d0b798ea8e0d228408f98d73c4c; em_hq_fls=js; emshistory=%5B%22%E8%88%AA%E5%8F%91%E5%8A%A8%E5%8A%9B%22%5D; intellpositionL=1079.19px; intellpositionT=1790px; st_si=88358266735180; st_asi=delete; HAList=f-0-000001-%u4E0A%u8BC1%u6307%u6570%2Ca-sz-002030-%u8FBE%u5B89%u57FA%u56E0%2Ca-sh-600893-%u822A%u53D1%u52A8%u529B%2Ca-sz-002400-%u7701%u5E7F%u96C6%u56E2%2Ca-sz-002675-%u4E1C%u8BDA%u836F%u4E1A; waptgshowtime=2020910; EMFUND0=09-04%2009%3A42%3A29@%23%24%u534E%u590F%u56FD%u8BC1%u534A%u5BFC%u4F53%u82AF%u7247ETF@%23%24159995; EMFUND1=09-04%2009%3A42%3A40@%23%24%u56FD%u8054%u5B89%u4E2D%u8BC1%u534A%u5BFC%u4F53ETF%u8054%u63A5C@%23%24007301; EMFUND2=09-04%2009%3A42%3A44@%23%24%u56FD%u6CF0CES%u534A%u5BFC%u4F53%u82AF%u7247%u884C%u4E1AETF%u8054%u63A5C@%23%24008282; EMFUND4=09-07%2009%3A57%3A51@%23%24%u4E2D%u94F6%u533B%u7597%u4FDD%u5065%u6DF7%u5408@%23%24005689; EMFUND5=09-07%2010%3A56%3A31@%23%24%u8BFA%u5B89%u6210%u957F%u6DF7%u5408@%23%24320007; EMFUND8=09-09%2012%3A22%3A28@%23%24%u6613%u65B9%u8FBE%u56FD%u9632%u519B%u5DE5%u6DF7%u5408@%23%24001475; EMFUND6=09-10%2012%3A52%3A28@%23%24%u4E2D%u94F6%u533B%u7597%u4FDD%u5065%u6DF7%u5408A@%23%24005689; EMFUND3=09-10%2012%3A54%3A20@%23%24%u62DB%u5546%u56FD%u8BC1%u751F%u7269%u533B%u836F%u6307%u6570%u5206%u7EA7@%23%24161726; EMFUND9=09-10%2012%3A55%3A44@%23%24%u4E2D%u6B27%u533B%u7597%u5065%u5EB7%u6DF7%u5408A@%23%24003095; EMFUND7=09-10 13:07:55@#$%u62DB%u5546%u4E2D%u8BC1%u767D%u9152%u6307%u6570%u5206%u7EA7@%23%24161725; st_pvi=64436086999909; st_sp=2020-09-09%2016%3A36%3A53; st_inirUrl=https%3A%2F%2Ffund.eastmoney.com%2F; st_sn=175; st_psi=20200910134528791-0-8423363783'
}


def stock_comments():
    '''
    爬取股票股吧评论数据
    @return:
    '''
    for i in range(1, 201):
        print('第{}页'.format(i))
        url = 'http://guba.eastmoney.com/list,zssh000001_{}.html'.format(str(i))
        res = requests.get(url, headers=headers).content.decode()
        html = etree.HTML(res)
        title = html.xpath('.//div[@id="articlelistnew"]//div[@class="articleh normal_post"]//span[3]//text()')
        title = [x.replace(' ', '') for x in title]
        title = list(filter(None, title))
        urls = html.xpath('.//div[@id="articlelistnew"]//div[@class="articleh normal_post"]//span[3]//@href')
        urls = [x.replace(' ', '') for x in urls]
        urls = list(filter(None, urls))
        authors = html.xpath('.//div[@id="articlelistnew"]//div[@class="articleh normal_post"]//span[4]//text()')
        date_com = html.xpath('.//div[@id="articlelistnew"]//div[@class="articleh normal_post"]//span[5]//text()')
        print(len(title), title)
        print(len(urls), urls)
        print(len(authors), authors)
        print(len(date_com), date_com)


if __name__ == '__main__':
    stock_comments()

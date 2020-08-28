# -*- coding: utf-8 -*-
# @File:       |   taobao.py 
# @Date:       |   2020/8/21 21:11
# @Author:     |   ThinkPad
# @Desc:       |  
import re
import time
import requests
import pandas as pd
from lxml import etree

def spider_goods(url):
    '''
    爬取淘宝页面上商品列表信息
    :param url:
    :return:
    '''

    res = requests.get(url,headers=headers).content.decode()
    print(res)
    html = etree.HTML(res)
    print(html)
    goods_name = html.xpath('.//div[@class="item J_MouserOnverReq"]//div[@class="ctx-box J_MouseEneterLeave J_IconMoreNew"]//div[@class="row row-2 title"]//a//span/text()')
    print(goods_name)

if __name__ == '__main__':
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'cookie': 'cna=Jr6uF4DpUFECAbfOpvzsiFx8; lgc=stronger%5Cu677E%5Cu677E; tracknick=stronger%5Cu677E%5Cu677E; enc=rrO0BnudnHQHocOKyDcVOzDLeOgR%2Bg0E%2FFtMnkX%2FFVjLvsuHtBgD4EiOmoppnhRfN6slSEreGbxLTiIWExT0sQ%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; miid=192460323830451525; mt=ci=11_1; sgcookie=E4KwCPeF0TQhjz3Gubg3q; uc3=vt3=F8dCufTDBi8xalV5B1c%3D&nk2=EEotYDXV%2FehSMM9J&lg2=V32FPkk%2Fw0dUvg%3D%3D&id2=UU8Pbn6GwBWNLA%3D%3D; uc4=id4=0%40U22IA6n4HRvfaFGHVV3keYgTIYwT&nk4=0%40EpMm8%2BhBe53LYLbSCtz5GrOok%2F8%2FhXA%3D; _cc_=URm48syIZQ%3D%3D; _samesite_flag_=true; cookie2=1bb6ae459c9058df989e65182b8718ed; t=52c6a946f8cf145a406c8cd71d63580f; _tb_token_=338e10b33d06e; _m_h5_tk=eb8eafff2b9b1800b2ff0840ca35cc7b_1598025523508; _m_h5_tk_enc=b2a6a2e2279cde6d4cec2ea36c94a804; uc1=cookie14=UoTV5Or9KulYQg%3D%3D; v=0; JSESSIONID=77C6CFF1DC33DBB5367438962DB8FBE6; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; isg=BP__hzE5nAmUa5gNWkcFIUEEjtOJ5FOGN0jNx5HIt6_8oBUimbZJ1mTy4nBe-Cv-; l=eBLNYmomOa0iKNbQBO5ahurza77TPCAflsPzaNbMiInca1PG6gp2kNQq-U5eJdtjgtfjqetrq8bBLReWWe4dg2HvCbKrCyCkOc9v-; tfstk=cRjdBFbCu5VhDrJO3wUMFHADd47daMzpZ5Aq2-Q65QBu3qiZjsxFmi59Ucvx9heO.',
        'referer': 'https://s.taobao.com/search?q=%E6%B2%99%E5%8F%91&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306'
    }
    url = 'https://s.taobao.com/search?q=%E6%B2%99%E5%8F%91&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20200821&ie=utf8'
    spider_goods(url)

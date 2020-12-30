# -*- coding: utf-8 -*-
# @File:       |   weibo.py 
# @Date:       |   2020/11/23 9:40
# @Author:     |   ThinkPad
# @Desc:       |  
import json

import requests

from lxml import etree


def asd():
    ''''''
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Host': 's.weibo.com',
        'Referer': 'https://s.weibo.com/weibo/%25E5%2588%259D%25E9%259B%25AA?topnav=1&wvr=6&b=1',
        'Cookie': 'SINAGLOBAL=4259651335291.8765.1596444675238; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFz6B.0sprohA72zRZigx005JpX5KMhUgL.Fo-0ShMfSK-0Shq2dJLoI7v2-XU2xHzLxKqL1-BLB.-t; ALF=1637630888; SSOLoginState=1606094889; SCF=AniQSL9eiDWcn4YwX46zbEmVMIRMaEJOu-x_c4mLuV8BovPgAqnhQtp8NFz2Vzw4RFgunxNJrT0fN7ZqZ4SSVik.; SUB=_2A25yv2B5DeRhGeNN71UU9SvPzzqIHXVRzdaxrDV8PUNbmtAKLVmjkW9NSaVdMFzk0gzIsaOjKZDsc0apPkEoObyu; wvr=6; _s_tentry=login.sina.com.cn; Apache=4251488715656.131.1606094892046; ULV=1606094892121:6:1:1:4251488715656.131.1606094892046:1600146668448; UOR=www.takefoto.cn,widget.weibo.com,www.pythontip.com; webim_unReadCount=%7B%22time%22%3A1606101296170%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A18%2C%22msgbox%22%3A0%7D; WBStorage=8daec78e6a891122|undefined',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    url = 'https://s.weibo.com/weibo/%25E5%2588%259D%25E9%259B%25AA?topnav=1&wvr=6&b=1&page=2'
    res = requests.get(url, headers=headers)
    print(res.status_code)
    if 200 == res.status_code:
        res = res.content.decode()
        html = etree.HTML(res)
        author_list = html.xpath('.//div[@class="content"]//p/@nick-name')
        content_list = html.xpath('.//div[@class="content"][]//p//text()')
        print(len(author_list), author_list)
        print(len(content_list), content_list)


def touxiao():
    '''
    爬取新浪微博头条前100条
    @return:
    '''
    url = 'https://weibo.com/?category=1760'
    headers = {
        'cookie': 'SINAGLOBAL=4259651335291.8765.1596444675238; ALF=1637630888; SCF=AniQSL9eiDWcn4YwX46zbEmVMIRMaEJOu-x_c4mLuV8BovPgAqnhQtp8NFz2Vzw4RFgunxNJrT0fN7ZqZ4SSVik.; SUB=_2AkMog3aZf8NxqwJRmfkXxGnkZI9wzAzEieKe34dCJRMxHRl-yT92qkIktRB6AwNYcyZ70AGh_Ew_l3K9OatEvrysX-0t; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9W5MK7sMjufhd.jczATN6HiR; login_sid_t=211814f79f31c88e646c3029dc1ed06b; cross_origin_proto=SSL; WBStorage=8daec78e6a891122|undefined; _s_tentry=passport.weibo.com; UOR=www.takefoto.cn,widget.weibo.com,www.baidu.com; Apache=3813180197333.1704.1608513968026; ULV=1608513968035:8:2:1:3813180197333.1704.1608513968026:1607394727301; wb_view_log=1366*7681',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    if 200 == res.status_code:
        res = res.content.decode()
        print(res)
        html = etree.HTML(res)
        title_list = html.xpath(
            './/div[@class="UG_list_b"]//div[@class="list_des"]//h3[@class="list_title_b"]//a/text()')
        print(title_list)


if __name__ == '__main__':
    touxiao()

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
        print(len(author_list),author_list)
        print(len(content_list),content_list)


if __name__ == '__main__':
    asd()

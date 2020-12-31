# -*- coding: utf-8 -*-
# @File:       |   zhihu.py 
# @Date:       |   2020/12/30 10:11
# @Author:     |   ThinkPad
# @Desc:       |  知乎热门数据的抓取

import re
import json
import time
import requests
from datetime import datetime
import pandas as pd
import numpy as np
from lxml import etree


def get_hot_info():
    '''
    知乎热门数据的抓取
    @return:
    '''
    url = 'https://www.zhihu.com/hot'
    headers = {
        'cookie': '_zap=6292de36-ba0a-47be-9dd5-b80b31769f74; d_c0="ADDXD1KVtRGPTqpBA7hJeKVP1LKnCfIjy4k=|1597023624"; _ga=GA1.2.62544664.1597023630; _xsrf=3y8yDwXsP2Wf9AF6fvyRe3RrlWcK5hSY; r_cap_id="YWFjOTNmMGEwZjNkNDBkODg3MmRlMjUyOTU0OGFiNzU=|1608083613|a0be2ab84e0367f0490a2c47ba2335cdbc8f61b3"; cap_id="NDVkYjQzMzYyNzQ2NDc4MWIzZDQ4OTgxZGE3ZmY3ZmM=|1608083613|06d613bbc3f11ceef6c97dfb9f858bc70d82133c"; l_cap_id="ZjhjNjkxZGI5YmM2NDMzNmIyOGFlNGJlN2Q5ODdjOTA=|1608083613|11502a419b0d751bfe004096cd4d06e9dd12b63f"; client_id="bzNwMi1qZzBqTEtNQ1pfdHVKdGp2d1F5NGc4TQ==|1608083624|ce2edb40e6cb6ee1b708b0fee3bf1a7d30907f9b"; capsion_ticket="2|1:0|10:1608083625|14:capsion_ticket|44:OGI5N2IwNzA3NzA1NGU0YWI4ZGEyMWM2NjJhNWMyZDI=|a8a77fcfcd5f73df0145e9b27281c07e13ca85652323e4669acc826882914bea"; z_c0="2|1:0|10:1608083696|4:z_c0|92:Mi4xdDlFWUlnQUFBQUFBTU5jUFVwVzFFU1lBQUFCZ0FsVk43N2JHWUFCaldaWHVrTmUxU3BiTFhfTVcwUkJfZUktVXV3|7a4867314e863a666334e4c389583aaf816f6551cd484132fbd51722be568031"; q_c1=e6df33b64d4a4bcfa2f3c020a546fdc3|1608532513000|1608532513000; tst=h; tshl=; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1609206367,1609211817,1609289749,1609294314; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1609294314; KLBRSID=d017ffedd50a8c265f0e648afe355952|1609294315|1609294313; SESSIONID=j71DgUTXGOybycJpqb80RSN2VjcwOqKbq40NUrV4ERI; JOID=U1wRBknHWzVp87A1OMM9b96jIYYsqGwFKpfgYWGDEUwKjdB6SCm72DL1tTQ-6cFzqEKakdj6SIE7LKDGu-BUAZU=; osd=UV8WC0LFWDJk-LI2P842bd2kLI0uq2sIIZXjZmyIE08NgNt4Sy620zD2sjk168J0pUmYkt_3Q4M4K63NueNTDJ4=',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    if 200 == res.status_code:
        res = res.content.decode()
        html = etree.HTML(res)
        title_list = html.xpath('.//div[@class="HotItem-content"]//a//h2/text()')
        print('标题--->长度：{}---{}'.format(len(title_list), title_list))
        url_list = html.xpath('.//div[@class="HotItem-content"]//a/@href')
        print('url--->长度：{}---{}'.format(len(url_list), url_list))
        com_list = html.xpath('.//div[@class="HotItem-content"]//a//p[@class="HotItem-excerpt"]//text()')
        print('内容--->长度：{}---{}'.format(len(com_list), com_list))
        hot_list = html.xpath('.//div[@class="HotItem-content"]//div/text()')
        print('热度--->长度：{}---{}'.format(len(hot_list), hot_list))


if __name__ == '__main__':
    get_hot_info()

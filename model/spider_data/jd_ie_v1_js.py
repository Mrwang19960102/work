# -*- coding: utf-8 -*-
import json
import random
import re
import threading
import time

import demjson
import redis
import requests
import urllib3

r = redis.StrictRedis(host='127.0.0.1', port=6379, decode_responses=True)


def get_timeSwap():
    return (int(round(time.time() * 1000)))


Proxy = [
    'naomizzz:Mr0z7AKXaZ@45.237.171.112:12851',
    'naomizzz:Mr0z7AKXaZ@45.237.171.40:12851',
    'naomizzz:Mr0z7AKXaZ@45.237.170.171:12851',
    'naomizzz:Mr0z7AKXaZ@45.237.171.157:12851',
    'naomizzz:Mr0z7AKXaZ@45.237.170.26:12851',
    'naomizzz:Mr0z7AKXaZ@45.224.228.87:12851',
    # 'naomizzz:Mr0z7AKXaZ@45.224.228.158:12851',
    'naomizzz:Mr0z7AKXaZ@161.0.70.74:12851',
    # 'naomizzz:Mr0z7AKXaZ@45.224.228.234:12851',
    'naomizzz:Mr0z7AKXaZ@161.0.70.178:12851',
]


def get_proxy():
    proxy = random.choice(Proxy)
    return {
        'http': 'http://' + proxy,
        'https': 'https://' + proxy
    }


# 通知
def notify(product_url, product_name):
    dd_url = 'https://oapi.dingtalk.com/robot/send?access_token=e910df7b41ec9fe88a59aadfb1fd04e629845a22f364ea79ec4212a8e31bc1f0'
    dd_another_url = 'https://oapi.dingtalk.com/robot/send?access_token=9e3f1c634db7d1681144d17722704de4bc64d3d73832604bc5c65b7bd5d9fc99'
    dd_header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }
    data_info = {
        "msgtype": "link",
        "link": {
            "text": '监控报警',
            "title": product_name,
            "messageUrl": product_url,
            # "picUrl": image
        }
    }
    json_data = json.dumps(data_info)
    requests.post(dd_url, data=json_data, headers=dd_header)
    requests.post(dd_another_url, data=json_data, headers=dd_header)


# 电话通知
def crawler_monitor(product_name):
    dd_url = 'https://oapi.dingtalk.com/robot/send?access_token=2b5e1d67fde868f1b0318624d011ded0aab1977de5cd3f859ff7a7db50d9501e'
    dd_header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }

    data_info = {
        "msgtype": "text",
        "text": {
            "content": "监控报警\n" + product_name
        },
    }
    json_data = json.dumps(data_info)
    requests.post(dd_url, data=json_data, headers=dd_header, proxies=get_proxy())


headerArray = [
    'UCWEB7.0.2.37/28/999',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)',
    'Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0',
    'Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+',
    'Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13',
    'MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
    'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'
]

headers = {
    'user-agent': random.choice(headerArray),
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
}

urllib3.disable_warnings()


class start_my_bot(threading.Thread):
    # 初始化对象
    def __init__(self, base_url, flag, count):
        threading.Thread.__init__(self)
        self.base_url = base_url
        self.flag = flag
        self.count = count

    def run(self):
        while True:
            product_url = 'https://www.jdsports.ie/product/~/%s/'
            for url in self.base_url:
                number = 0
                while True:
                    try:
                        search_url = url + '_=' + str(get_timeSwap())
                        res = requests.get(url=search_url, headers=headers, verify=False,
                                           timeout=15)
                        if res.status_code == 200:
                            data = re.findall(r'items:(.*?)};', res.text, re.S)[0]
                            # 解析json键值不带引号的问题
                            data_list = demjson.decode(data)
                            if len(data_list) > 0:
                                print(
                                        self.flag + ':' + str(
                                    res.status_code) + ' ,url:' + search_url + ' ,length:' + str(
                                    len(data_list)) + ' ,time:' + time.strftime(
                                    '%Y-%m-%d %H:%M:%S'))
                                break
                    except Exception as e:
                        number += 1
                        if number > 20:
                            crawler_monitor('ie:脚本挂了，打电话给浩哥')
                        print(e)
                        # print(number)
                try:
                    for item in data_list:
                        product_name = item['description']
                        product_id = item['plu']
                        if not r.sismember("jd_ie", product_url % product_id):
                            r.sadd("jd_ie", product_url % product_id)
                            if self.count != 0:
                                notify(product_url % product_id, 'Product Crawler\n' + product_name)
                    time.sleep(5)
                except Exception as e:
                    print(e)
            self.count += 1


if __name__ == '__main__':
    jd_ie_url_1 = [
        'https://www.jdsports.ie/search/Jordan+1/latest/?',
        'https://www.jdsports.ie/search/Jordan+1/latest/?max=204&',
        'https://www.jdsports.ie/search/Jordan/latest/?',
        'https://www.jdsports.ie/search/Jordan/latest/?max=204&',
        'https://www.jdsports.ie/brand/jordan/latest/?',
        'https://www.jdsports.ie/brand/jordan/latest/?max=204&',
        'https://www.jdsports.ie/campaign/new+in/?facet-new=latest&sort=latest&',
    ]

    jd_ie_url_2 = [
        'https://www.jdsports.ie/men/brand/jordan/latest/?',
        # 'https://www.jdsports.ie/men/mens-footwear/brand/jordan/?facet-new=latest&',
        'https://www.jdsports.ie/women/brand/jordan/latest/?',
        'https://www.jdsports.ie/women/womens-footwear/brand/jordan/latest/?',
        'https://www.jdsports.ie/kids/brand/jordan/latest/?',
        'https://www.jdsports.ie/kids/junior-footwear-(sizes-3-5.5)/brand/jordan/latest/?'

    ]

    jd_ie_bot_1 = start_my_bot(jd_ie_url_1, 'url_1', 0)
    jd_ie_bot_1.start()
    jd_ie_bot_2 = start_my_bot(jd_ie_url_2, 'url_2', 0)
    jd_ie_bot_2.start()

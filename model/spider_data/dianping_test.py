# coding:gbk
# @File:       |   dianping_test.py
# @Date:       |   2020/8/31 9:31
# @Author:     |   ThinkPad
# @Desc:       |  大众网评  评论
import json
import random
import time
import requests
from model.spider_data import conf
from datetime import datetime


class DZDP(object):
    def __init__(self):
        self.headers = conf.headers2

    def parse(self, shop_id):
        num_dic = {
            'f261': 0,
            'ebd1': 5,
            'f716': 9,
            'ee51': 8,
            'e1dd': 3,
            'e027': 6,
            'f5b9': 2,
            'e1d8': 4,
            'e745': 7,
        }
        rate_url = 'http://www.dianping.com/ajax/json/shopDynamic/basicHideInfo?shopId={}'.format(shop_id)
        htmls = self.fetch(url=rate_url)
        if htmls:
            htmls = json.loads(htmls)
            phones1 = str(htmls['msg']['shopInfo']['phoneNo'])
            phones2 = str(htmls['msg']['shopInfo']['phoneNo2'])
            phone = phones1.replace(f'<d class="num">&#x', '')
            phone = phone.replace(f'</d>', '')
            try:
                phone1 = phones2.replace(f'<d class="num">&#x', '')
                phone1 = phone1.replace(f'</d>', '')
                for k, v in num_dic.items():
                    t = k + ';'
                    phone1 = phone1.replace(t, str(v))
            except:
                phone1 = ''
            for k, v in num_dic.items():
                t = k + ';'
                phone = phone.replace(t, str(v))
            # 查找店铺信息
            val = {
                'phone': phone,
                'phone1': phone1,
                # 'shop_id': shop_id
            }
            values = list(val.values())
            values = list(filter(None, values))
            if values:
                return values
            else:
                return '手机号：无添加'

    def fetch(self, url):
        i = 1
        while True:
            if i <= 3:
                ip_url = 'http://api.zhuzhaiip.com:498/GetIpPort?passageId=1319159857041154050&num=5&protocol=2&province=&city=&minute=30&format=1&split=1&splitChar=&reset=true&secret=c6nxY5'
                res_ip = requests.get(ip_url).content.decode()

                ip_list = res_ip.split(' ')
                ip_list = ip_list[0].split('\r\n')

                proxyMeta = random.choices(ip_list)
                proxies = {
                    "http": 'http://'+proxyMeta[0],
                    "https": 'https://'+proxyMeta[0]
                }
                print(proxies)
                r = requests.get(url=url, headers=self.headers, proxies=proxies,timeout=3)
                print('状态:{},proxies={},url={}'.format(r.status_code, proxies, url))
                if 200 == r.status_code:
                    html = r.content.decode()
                    html_json = json.loads(html)
                    if '未登录' == html_json['msg']:
                        input('更换cookie，{}'.format(html_json))
                    else:
                        return html
                # time.sleep(1)
            else:
                break
            i += 1

    def run(self, shop_url):
        shop_id = shop_url.rpartition('/')[2]
        values = self.parse(shop_id)
        return values


def main(shop_url):
    # shop_url = 'http://www.dianping.com/shop/103618945'
    dp = DZDP()
    phones = dp.run(shop_url)

    if phones:
        return phones
    else:
        return None

# -*- coding: utf-8 -*-
# @File:       |   ip_text.py 
# @Date:       |   2021/1/19 17:37
# @Author:     |   ThinkPad
# @Desc:       |  
import requests
from datetime import datetime

# 目标网址
targetUrl = "https://www.baidu.com"

# 代理地址
proxyIp = "182.106.136.81"
proxyPort = "45934"

meta = "http://%(host)s:%(port)s" % {
    "host": proxyIp,
    "port": proxyPort,
}
proxies = {
    "http": meta,
    "https": meta
}
print(proxies)
response = requests.get(targetUrl, proxies=proxies)
print(response.status_code)

print(response.text)

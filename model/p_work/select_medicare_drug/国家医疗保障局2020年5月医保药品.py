# -*- coding: utf-8 -*-
# @File:       |   sp-国家医疗保障局2020年5月医保药品.py
# @Date:       |   2020/6/22 17:25
# @Author:     |   
# @Desc:       |  http://code.nhsa.gov.cn:8000/search.html?sysflag=95 国家医疗保障局2020年5月医保药品数据抓取
#                  该网页禁止F12和复制操作，需要使用抓包工具进行查看数据传输方式
import time
import json
import random
import traceback
import requests
import pandas as pd


def get_data(url, page):
    """
    获取当前页面数据
    :param url: 请求连接
    :param page: 当前页页码
    :return: 页面数据
    """
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
               "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
               }
    data = {"batchNumber": 20200507,
            "rows": 50,
            "sord": "asc",
            "page": page}
    datas = requests.post(url, headers=headers, data=data).text
    datas = json.loads(datas)
    page_data = list(datas["rows"])
    # print(page_data)
    # print(len(page_data))
    return page_data


# 如果网站反爬，使用备份数据今进行转换数据表
def data_txt_to_excel():
    """
    读取txt中的json数据转存为Excel
    :return: None
    """
    with open("药品数据备份.txt", "r") as f:
        data = f.readlines()
        df = pd.DataFrame(data)
        df.to_excel("医保药品数据.xlsx", sheet_name="sheet1", startcol=0, index=False)


if __name__ == '__main__':
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    url = "http://code.nhsa.gov.cn:8000/yp/getPublishGoodsDataInfo.html"
    li = []
    try:
        for i in range(1, 1760):
            print("正在爬取第%s页···" % i)
            page_data = get_data(url, i)
            print("爬取完成")
            li.extend(list(page_data))
            # 防止网站反爬，每页数据进行备份, 其中某些特殊字符编码错误进行忽略
            with open("药品数据备份.txt", "a+", errors="ignore") as f:
                f.write(page_data)
            # 防止反爬，随机等待，可取消
            time.sleep(random.randint(1, 5))
        print("所有页面爬取完成,正在转换···")
        df = pd.DataFrame(li)
        df.to_excel("医保药品数据.xlsx", sheet_name="sheet1", startcol=0, index=False)
    except Exception as e:
        print(e, "爬取至第%s页出错, 程序终止"% str(i))
        print(traceback.format_exc())







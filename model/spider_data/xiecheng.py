# -*- coding: utf-8 -*-
# @File:       |   xiecheng.py 
# @Date:       |   2020/9/30 10:42
# @Author:     |   ThinkPad
# @Desc:       |  携程
import time
import requests
from datetime import datetime
import pandas as pd
import numpy as np
from lxml import etree

com_headers = {
    'referer': 'https://hotels.ctrip.com/hotel/24403644.html?isFull=F&masterhotelid=24403644&hcityid=58',
    'content-type':'application/x-www-form-urlencoded; charset=utf-8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'cookie': 'magicid=c2aSLc3a8I49g8l921sevGYb9p6r++RIb4wC4tP8Ov3BaLSQv4yIN4/TI76Mhhde; _RSG=iDK6b2jUCM5uNHsiU25O69; _RDG=283acccf0551dc294901e4f490b53edbdf; _RGUID=558c7ad0-a519-436c-9198-1427acd915f8; MKT_CKID=1596850832243.klbhq.4rt8; _ga=GA1.2.1810525487.1596850832; nfes_isSupportWebP=1; _abtest_userid=2a0716d8-cbeb-485c-8d61-2d697f562226; _RF1=58.213.125.178; Session=SmartLinkCode=U155952&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=&SmartLinkLanguage=zh; MKT_CKID_LMT=1601364755494; _gid=GA1.2.774440709.1601364756; MKT_Pagesource=PC; AHeadUserInfo=VipGrade=0&VipGradeName=%C6%D5%CD%A8%BB%E1%D4%B1&UserName=&NoReadMessageCount=0; Union=OUID=index&AllianceID=4897&SID=155952&SourceID=&createtime=1601428586&Expires=1602033385739; MKT_OrderClick=ASID=4897155952&AID=4897&CSID=155952&OUID=index&CT=1601428585743&CURL=https%3A%2F%2Fwww.ctrip.com%2F%3Fsid%3D155952%26allianceid%3D4897%26ouid%3Dindex&VAL={"pc_vid":"1596850829032.34mq83"}; HotelCityID=2split%E4%B8%8A%E6%B5%B7splitShanghaisplit2020-09-30split2020-10-01split0; ASP.NET_SessionId=vnk1qc4wapkqniv1h4s4zg5j; librauuid=XLNAM2s8HDXZSkd0Tp; hoteluuid=FLPsulDO87oZ2MnZ; OID_ForOnlineHotel=159685082903234mq831601428612627102032; _bfa=1.1596850829032.34mq83.1.1601364752414.1601428582647.5.33; HotelDomesticVisitedHotels1=24403644=0,0,4.8,2796,/200h0y000000m8zpxAE6E.jpg,&444194=0,0,4.8,1846,/200v1b000001ajxrt0748.jpg,; _jzqco=%7C%7C%7C%7C1601364755577%7C1.695249140.1596850832238.1601428631849.1601429861546.1601428631849.1601429861546.undefined.0.0.15.15; __zpspc=9.7.1601428585.1601429861.5%232%7Cwww.baidu.com%7C%7C%7C%25E6%2590%25BA%25E7%25A8%258B%7C%23; _bfi=p1%3D102003%26p2%3D102003%26v1%3D33%26v2%3D32; appFloatCnt=10; MjAxNS8wNi8yOSAgSE9URUwgIERFQlVH=OceanBall_comment; hotelhst=50349362'
}


def hotel_comments(url):
    '''
    爬取酒店评论数据
    @param url: 酒店链接
    @return:
    '''
    res = requests.get(url, headers=com_headers).content.decode()
    # html = etree.HTML(res)
    print(res)



def xiecheng_spider():
    '''
    携程数据爬取
    @return:
    '''
    url = 'https://hotels.ctrip.com/Domestic/tool/AjaxHotelCommentList.aspx?MasterHotelID=24403644&hotel=24403644&NewOpenCount=0&AutoExpiredCount=0&RecordCount=2797&OpenDate=2018-11-01&card=-1&property=-1&userType=-1&productcode=&keyword=&roomName=&orderBy=2&currentPage=3&viewVersion=c&contyped=0&eleven=e815ffbb789ac46684b6a4833684edfb38419719df91b277a7f380d5ab165a34_3096901197&callback=CASiJFucFRMOVDYoD&_=1601432805294'
    hotel_comments(url)


if __name__ == '__main__':
    xiecheng_spider()

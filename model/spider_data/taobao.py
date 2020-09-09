# -*- coding: utf-8 -*-
# @File:       |   taobao.py 
# @Date:       |   2020/8/21 21:11
# @Author:     |   ThinkPad
# @Desc:       |  
import re
import time
import json
import requests
import pandas as pd
from lxml import etree

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'cookie': 'cna=Jr6uF4DpUFECAbfOpvzsiFx8; lgc=stronger%5Cu677E%5Cu677E; tracknick=stronger%5Cu677E%5Cu677E; enc=rrO0BnudnHQHocOKyDcVOzDLeOgR%2Bg0E%2FFtMnkX%2FFVjLvsuHtBgD4EiOmoppnhRfN6slSEreGbxLTiIWExT0sQ%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; miid=192460323830451525; mt=ci=11_1; sgcookie=E4KwCPeF0TQhjz3Gubg3q; uc3=vt3=F8dCufTDBi8xalV5B1c%3D&nk2=EEotYDXV%2FehSMM9J&lg2=V32FPkk%2Fw0dUvg%3D%3D&id2=UU8Pbn6GwBWNLA%3D%3D; uc4=id4=0%40U22IA6n4HRvfaFGHVV3keYgTIYwT&nk4=0%40EpMm8%2BhBe53LYLbSCtz5GrOok%2F8%2FhXA%3D; _cc_=URm48syIZQ%3D%3D; _samesite_flag_=true; cookie2=1bb6ae459c9058df989e65182b8718ed; t=52c6a946f8cf145a406c8cd71d63580f; _tb_token_=338e10b33d06e; _m_h5_tk=eb8eafff2b9b1800b2ff0840ca35cc7b_1598025523508; _m_h5_tk_enc=b2a6a2e2279cde6d4cec2ea36c94a804; uc1=cookie14=UoTV5Or9KulYQg%3D%3D; v=0; JSESSIONID=77C6CFF1DC33DBB5367438962DB8FBE6; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; isg=BP__hzE5nAmUa5gNWkcFIUEEjtOJ5FOGN0jNx5HIt6_8oBUimbZJ1mTy4nBe-Cv-; l=eBLNYmomOa0iKNbQBO5ahurza77TPCAflsPzaNbMiInca1PG6gp2kNQq-U5eJdtjgtfjqetrq8bBLReWWe4dg2HvCbKrCyCkOc9v-; tfstk=cRjdBFbCu5VhDrJO3wUMFHADd47daMzpZ5Aq2-Q65QBu3qiZjsxFmi59Ucvx9heO.',
    # 'referer': 'https://s.taobao.com/search?q=%E6%B2%99%E5%8F%91&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306'
    'referer': 'https://detail.tmall.com/item.htm?id=570790460273&ali_refid=a3_430583_1006:1151346681:N:dnGK4I14AFrjfwZ+FPdjQw==:a86705760564041cc386f8709475b714&ali_trackid=1_a86705760564041cc386f8709475b714&spm=a230r.1.14.1'
}


def spidergoods_list():
    '''
    爬取淘宝搜索页面商品列表信息
    :return:
    '''
    '''
    定义变量
    '''
    for i in range(1, 51):
        url = 'https://s.taobao.com/search?q=python&js={}&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20190401&ie=utf8&ajax=true'.format(
            i)
        print('第{}页,url={}'.format(i, url))
        # 价格
        price_list = []
        # 付款人数
        pay_num = []
        # 名称
        name_list = []
        # 店铺名称
        shop_name = []
        # 城市
        city_list = []
        # id
        id_list = []
        # 运费
        view_fee_list = []
        res = requests.get(url, headers=headers).content.decode()
        dict_res = json.loads(res)
        data_info = dict_res['mods']['itemlist']['data']['auctions']
        for info in data_info:
            name_list.append(info['title'])
            price_list.append(info['view_price'])
            view_fee_list.append(info['view_fee'])
            pay_num.append(info['view_sales'])
            shop_name.append(info['nick'])
            city_list.append(info['item_loc'])
            id_list.append(info['nid'])
        name_list = [re.compile(r'<[^>]+>', re.S).sub('', x) for x in name_list]
        print(name_list)
        print(price_list)
        print(view_fee_list)
        print(pay_num)
        print(shop_name)
        print(city_list)
        print(id_list)
        df = pd.DataFrame({
            '名称': name_list,
            '价格': price_list,
            '运费': view_fee_list,
            '付款人数': pay_num,
            '店铺名称': shop_name,
            '城市': city_list,
            'id': id_list,

        })
        print(df)
        time.sleep(10)


def get_goods_info():
    '''
    获取每一个商品的详细信息
    @return:
    '''
    sellCount = None
    id = '570790460273'
    url = 'https://mdskip.taobao.com/core/initItemDetail.htm?itemId={}'.format(id)
    res = requests.get(url, headers=headers).text
    res = res.replace('setMdskip', '').replace('(', '').replace(')', '')
    res_json = json.loads(res)
    data_info = res_json['defaultModel']
    if data_info:
        data_info = data_info['sellCountDO']
        if data_info:
            sellCount = data_info['sellCount']
    print(sellCount)
    print(type(sellCount))
    i = 1
    all_com_list = []
    all_com_date_list = []
    while i<=20:
        com_list = []
        com_date_list = []
        com_url = 'https://rate.tmall.com/list_detail_rate.htm?itemId=570790460273&spuId=983590076&sellerId=3417036972&order=3&currentPage=3&append=0&content=1&tagId=&posi=&picture=&groupId=&ua=098%23E1hvUpvZvxGvUvCkvvvvvjiPnLcOsjEHnLMysj3mPmP9zjrERFswljlUPsch0jEhRphvCvvvvvmCvpvZz2sRJccNznsGwAafYQPwurAv7IVrvpvEvvQTFMPsCRdhdphvmpvW5I%2FkI9LJJT6CvvyvmH8P%2BdUhseptvpvhvvvvvUhCvCcYcn1gGJMwzPsSvxdAZ0eCkRSRsRUtvpvhvvvvv86CvvyvmR9UQwhhW%2B6Pvpvhvv2MMQyCvhQUCaIvCAJxfaBl5dUf8z7gF4VQRpn%2ByXZH6BoAVA1libmxdX9aWGjxs4hZ%2B3%2BKa4oQiXTOwhcy%2BneYr2E9ZRAn3w0AhjHHTWex6fItuphvmvvv92I11Gp6kphvC99vvOCzBbyCvm9vvvvvphvvvvvv9krvpv3Vvvmm86Cv2vvvvUUdphvUOQvv9krvpv3FvphvC9vhvvCvp2yCvvpvvvvviQhvCvvv9U8jvpvhvvpvvUhCvvswN8YujaMwzPsnDxurvpvoECC2F0lrCjODFfw0fpF36weH&needFold=0&_ksTS=1599639907907_4408&callback=jsonp4409'
        res_com = requests.get(com_url, headers=headers).content.decode()
        print(res_com)
        if res_com:
            # todo 匹配一直到最后一个）
            res_com = re.findall(r'[(](.*?)[)]$', res_com)[0]
            res_com_dict = json.loads(res_com)
            rate_list = res_com_dict['rateDetail']['rateList']
            for rate in rate_list:
                comment = rate['rateContent']
                comment_date = rate['rateDate']
                com_list.append(comment)
                com_date_list.append(comment_date)
            print('评论时间', com_date_list)
            all_com_date_list.extend(com_date_list)
            print('评论内容', com_list)
            all_com_list.extend(com_list)
            time.sleep(10)
            i += 1
        else:
            break

    if all_com_list and all_com_date_list:
        com_df = pd.DataFrame({
            '评论时间':all_com_date_list,
            '评论内容':all_com_list,
        })
        com_df.to_excel('./data_export/淘宝评论.xlsx',index=False)


if __name__ == '__main__':
    get_goods_info()

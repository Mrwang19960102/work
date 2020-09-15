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
    'referer': 'https://s.taobao.com/search?q=%E6%B2%99%E5%8F%91&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306'
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
    while i <= 20:
        com_list = []
        com_date_list = []
        com_url = 'https://rate.tmall.com/list_detail_rate.htm?itemId={}&spuId=983590076&sellerId=3417036972&order=3&currentPage={}&append=0&content=1&tagId=&posi=&picture=&groupId=&ua=098%23E1hvnvvZvx9vUvCkvvvvvjiPnLcOsjlbn2MhQjthPmPO6jD8RLzO0jYPRsFOzjY89phvHnQGuciVzYswMCpb7MN3zbjwOHuCdphvmpmCmm9MvUC9kOhCvvswN8xeIYMwzP1QBHurvpvEvUUxVBWv9Hmb3QhvCvmvphm5vpvhvvCCBvhCvvOvChCvvvvEvpCWvR63UBlrV4TJ%2B3%2Bu6jZ7%2Bu6wjomxfBAKDfUf8c7Q%2Bu0OV369kjVTVEe1UzMxQEysekglCwAXVoTTVjW7DcVTVEysaASxQEysWkglCfyCvm9vvhCvvvvvvvvvBBWvvUvzvvCHhQvv9pvvvhZLvvvCfvvvBBWvvvH%2BuphvmvvvpLcHVYAQkphvC9hvpyPwsvGCvvpvvPMMRphvCvvvphmrvpvEvvjSTjQv9W0%2BdphvmpmmmpZRvU2BpFyCvvpvvhCvdphvhIpmjsGsvU2XDbhSpqoxP2It%2B86Cvvyv9ci4BQmv7K4rvpvEvvjf%2FQWv9HGQRphvCvvvphv%3D&needFold=0&_ksTS=1599636798333_2922&callback=jsonp4409'.format(
            id, i)
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
            '评论时间': all_com_date_list,
            '评论内容': all_com_list,
        })
        com_df['商家ID'] = id
        com_df.to_excel('./data_export/淘宝评论.xlsx', index=False)


if __name__ == '__main__':
    get_goods_info()

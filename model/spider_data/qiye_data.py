# -*- coding: utf-8 -*-
# @File:       |   3456789.py 
# @Date:       |   2020/8/18 20:59
# @Author:     |   ThinkPad
# @Desc:       |
import time
import pandas as pd
import requests
from lxml import etree
from model.spider_data.dao import dbmanager

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}


def get_info():
    '''
    解析公司详情页基本信息
    :return:
    '''
    all_data = []
    for i in range(1, 200):
        print('第{}轮'.format(i))
        url_df = dbmanager.need_parsing_url()
        url_list = list(url_df['url'])
        for url in url_list:
            res = requests.get(url, headers=headers).content.decode()
            html = etree.HTML(res)
            name = html.xpath('.//div[@class="seller-info"]//h3[@class="title"]/text()')
            infos_key = html.xpath('.//div[@class="info-list"]//dl//dt/text()')
            infos_value = html.xpath('.//div[@class="info-list"]//dl//dd/text()')
            # 如果顺利访问
            if name and infos_key and infos_value:
                infos_value = [x.strip() for x in infos_value if x.strip() != '']
                name = name[0]
                infos_key = infos_key[1:]
                info_dict = dict(zip(infos_key, infos_value))
                info_dict['com_name'] = name
                info_dict['url'] = url
                if 'QQ号码' not in info_dict.keys():
                    info_dict['QQ号码'] = None
                if '公司类型' not in info_dict.keys():
                    info_dict['公司类型'] = None
                if '所在地区' not in info_dict.keys():
                    info_dict['所在地区'] = None
                if '联系手机' not in info_dict.keys():
                    info_dict['联系手机'] = None
                if '公司电话' not in info_dict.keys():
                    info_dict['公司电话'] = None
                every_data = []
                every_data.append(info_dict['com_name'])
                every_data.append(info_dict['url'])
                every_data.append(info_dict['公司类型'])
                every_data.append(info_dict['所在地区'])
                every_data.append(info_dict['联系手机'])
                every_data.append(info_dict['公司电话'])
                every_data.append(info_dict['QQ号码'])
                all_data.append(every_data)
                print(every_data)
                # 时间延时
                time.sleep(5)
            # 如果拒绝访问
            else:
                if all_data:
                    save_df = pd.DataFrame(all_data, columns=['com_name', 'url', 'com_type', 'area',
                                                              'telephone', 'public_telephone', 'qq'])
                    save_bo = dbmanager.save_qiye_info(save_df)
                    update_bo = dbmanager.update_data(save_df)
                    print('存储状态:{}'.format(save_bo))
                    print('更新状态:{}'.format(update_bo))
                else:
                    print('没有要存储的数据')
                return
    if all_data:
        save_df = pd.DataFrame(all_data, columns=['com_name', 'url', 'com_type', 'area',
                                                  'telephone', 'public_telephone', 'qq'])
        save_bo = dbmanager.save_qiye_info(save_df)
        update_bo = dbmanager.update_data(save_df)
        print('存储状态:{}'.format(save_bo))
        print('更新状态:{}'.format(update_bo))
    else:
        print('数据为空')


def all_company():
    '''
    获取每个公司的详情页的链接
    :return:
    '''
    df_old = pd.DataFrame(columns=['url'])
    url_list = []
    for i in range(2, 335):
        url = 'http://qiye.molbase.cn/g/p' + str(i) + '/'
        print('第{}页,url={}'.format(i, url))
        res = requests.get(url, headers=headers).content.decode()
        if '页面访问需验证' in res:
            a = input('请输入验证码后继续：')
            pass
        html = etree.HTML(res)
        all_url = html.xpath('.//div[@class="list"]//ul//li//dl//dt//a/@href')
        # 可以访问
        if all_url:
            url_list.extend(all_url)
        # 如果拒绝访问
        else:
            df_new = pd.DataFrame(url_list, columns=['url'])
            df_new.to_excel('./data_source/df_new.xlsx', index=False)
            df_old = df_old.append(df_new)
            df_old.to_excel('./data_source/df_old.xlsx', index=False)
            return df_old
        time.sleep(7)
    df_new = pd.DataFrame(url_list, columns=['url'])
    df_new.to_excel('./data_source/df_new.xlsx', index=False)
    df_old = df_old.append(df_new)
    return df_old


if __name__ == '__main__':
    pass

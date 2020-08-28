# -*- coding: utf-8 -*-
# @File:       |   3456789.py 
# @Date:       |   2020/8/18 20:59
# @Author:     |   ThinkPad
# @Desc:       |
import time
import pandas as pd
import requests
from lxml import etree
from model.machine_learning.covid_19.dao import dbmanager

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}

proxy = {'http': 'https://113.124.92.230:9999'
         # 'https': '120.236.128.201:8060'
         }


def get_info():
    for i in range(1, 200):
        print('第{}轮'.format(i))
        all_data = []
        url_df = dbmanager.need_parsing_url()
        url_list = list(url_df['url'])
        print(len(url_list))
        for url in url_list:
            res = requests.get(url, headers=headers).content.decode()

            html = etree.HTML(res)
            name = html.xpath('.//div[@class="seller-info"]//h3[@class="title"]/text()')
            infos_key = html.xpath('.//div[@class="info-list"]//dl//dt/text()')
            infos_value = html.xpath('.//div[@class="info-list"]//dl//dd/text()')
            if name and infos_key and infos_value:
                infos_value = [x.strip() for x in infos_value if x.strip() != '']
                name = name[0]
                infos_key = infos_key[1:]
                print(url)
                # print(name)
                # print(infos_key)
                # print(infos_value)
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
                time.sleep(5)
            else:
                if all_data:
                    save_df = pd.DataFrame(all_data, columns=['com_name', 'url', 'com_type',
                                                              'area', 'telephone', 'public_telephone', 'qq'])
                    dbmanager.save_qiye_info(save_df)
                    dbmanager.update_data(save_df)

                else:
                    print('数据为空')

        if all_data:
            save_df = pd.DataFrame(all_data, columns=['com_name', 'url', 'com_type',
                                                      'area', 'telephone', 'public_telephone', 'qq'])
            dbmanager.save_qiye_info(save_df)
            print('解析完毕')
            dbmanager.update_data(save_df)

        else:
            print('数据为空')


def all_company():
    df = pd.DataFrame()
    url_list = []

    for i in range(229, 335):

        url = 'http://qiye.molbase.cn/g/p' + str(i) + '/'
        print('第{}页,url={}'.format(i, url))
        res = requests.get(url, headers=headers).content.decode()
        if '页面访问需验证' in res:
            a = input('请输入验证码后继续：')
            pass
        html = etree.HTML(res)
        all_url = html.xpath('.//div[@class="list"]//ul//li//dl//dt//a/@href')
        if all_url:
            url_list.extend(all_url)
        else:
            df = pd.DataFrame(url_list, columns=['url'])
            df.to_excel('./df_new.xlsx', index=False)
            df_old = pd.read_excel('./df.xlsx')
            df_new = df_old.append(df)
            df_new.to_excel('./df.xlsx', index=False)
            return df

        print(all_url)
        print(len(url_list))
        time.sleep(7)
    df = pd.DataFrame(url_list, columns=['url'])
    df.to_excel('./df.xlsx'.format(i), index=False)
    print(df)
    return df


if __name__ == '__main__':
    save_df = get_info()

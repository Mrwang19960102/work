# -*- coding: utf-8 -*-
# @File:       |   boss.py 
# @Date:       |   2020/12/28 9:21
# @Author:     |   ThinkPad
# @Desc:       |  
import re
import requests
import pandas as pd
import numpy as np
from datetime import datetime
from lxml import etree


def position_list(pw):
    '''
    获取职位列表
    @return:
    '''
    url = 'https://www.zhipin.com/job_detail/?query={}&city=100010000&industry=&position='.format(pw)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'cookie': '_bl_uid=mpkCOd6kshm715gLhsg2zI3x366y; lastCity=101190100; __zp_seo_uuid__=e40e72eb-0ca9-4e0c-a99b-0429b9ae3060; __g=-; __l=r=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DUznGfn0ZWxGVG5Om5eLmi2izcy1A4JOThdynvYnvtzdgivYlBnSomxm0ziCOUARR%26wd%3D%26eqid%3D8ddfe478000fe17b000000045fe93155&l=%2Fwww.zhipin.com%2Fnanjing%2F&s=1&g=&s=3&friend_source=0; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1609118047; __c=1609118047; __a=16946643.1597287018.1605602347.1609118047.51.6.5.19; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1609118442; __zp_stoken__=18aebADZWBDl%2BO2wZNhFePwRxORIuTC4xbVMJWGRQJmVaXmsQJGwOMix%2BahA3AnVhPEcPbTx7H0c3axwuLU5sM1BDXQl2Wy0nez46NmJOCzcffX0gDkR7NU0kKXZ2bhxROhYFfnhbRDxIQEtNLA%3D%3D; __zp_sseed__=sRb6Nuxl51yrwAzHCscCjI7f8/2xx8q14F3BCGCWM6w=; __zp_sname__=e9ef2f1f; __zp_sts__=1609119167247; ___gtid=2030548211; __fid=adda3b07847e98659b910a9f0b90c3e8'
    }
    res = requests.get(url, headers=headers)
    if 200 == res.status_code:
        res = res.content.decode()
        html = etree.HTML(res)
        job_name_list = html.xpath('.//div[@class="job-title"]//text()')
        job_name_list = [x.replace('\n', '').replace(' ', '') for x in job_name_list]
        job_name_list = list(filter(None, job_name_list))
        print(job_name_list)


def job_info():
    '''

    @return:
    '''
    url = 'https://www.zhipin.com/job_detail/bb7dbf04b61f16090Hx92N69E1c~.html'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'cookie': '_bl_uid=mpkCOd6kshm715gLhsg2zI3x366y; lastCity=101190100; __zp_seo_uuid__=e40e72eb-0ca9-4e0c-a99b-0429b9ae3060; __g=-; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1609118047; __fid=adda3b07847e98659b910a9f0b90c3e8; __c=1609118047; __l=r=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DUznGfn0ZWxGVG5Om5eLmi2izcy1A4JOThdynvYnvtzdgivYlBnSomxm0ziCOUARR%26wd%3D%26eqid%3D8ddfe478000fe17b000000045fe93155&l=%2Fwww.zhipin.com%2Fjob_detail%2Fbb7dbf04b61f16090Hx92N69E1c~.html&s=3&g=&friend_source=0&s=3&friend_source=0; __a=16946643.1597287018.1605602347.1609118047.59.6.13.27; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1609119977; __zp_stoken__=18aebADZWBDl%2BO3B5VVtePwRxORJUQCQAbFIJWGRQJktsVRBQIWwOMix%2BCBt5XCNhPEcPbTx7H0M8Il0uOl0yAnJRN312M14ibDZORQZJCzcffX0gDhIle0ZGKXZ2bhxUOhYFfnhbRDxIQEtNLA%3D%3D'
    }
    res = requests.get(url, headers=headers)
    if 200 == res.status_code:
        res = res.content.decode()
        html = etree.HTML(res)
        desc_info = html.xpath('.//div[@class="job-sec"]//text()')
        desc_info = [x.replace('\n', '').replace(' ', '') for x in desc_info]
        desc_info = list(filter(None, desc_info))
        print(desc_info)


if __name__ == '__main__':
    job_info()

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


def position_list(pw, city):
    '''
    获取职位列表
    @param pw:
    @param city:
    @return:
    '''
    url = 'https://www.zhipin.com/c{}/?query={}&page=1'.format(city, pw)
    print(url)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'cookie': '_bl_uid=mpkCOd6kshm715gLhsg2zI3x366y; lastCity=101190100; __g=sem; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1609118047,1610543306; wt2=aPnM1xL6kh4i7iUh; __c=1610543306; __l=l=%2Fwww.zhipin.com%2Fc101110100%2F%3Fquery%3Dpython%26page%3D1&r=https%3A%2F%2Fwww.baidu.com%2Fbaidu.php%3Fsc.060000KKXYb9K48fS1q3MP1KzX4fXy4djSvpLMPg9CIC1AWhyFE3tR-xK65bDOqhTOMYs_yg4oTqM4S_il_3wQ2IzkryoP2caXKyRyATTFrNR0NdlZnAagPyONA7ZkRJUq7T4UbmHWijrR5SpW5tJrdkJW8DOEOvAw4ssyqLpSjafq8z7QeVXGlA1HwAf3f4rUZw5XKhUsgXuxr__hSKoNRbiaEZ.DY_NR2Ar5Od663rj6t8AGSPticrZA1AlaqM766WHGek3hcYlXE_sgn8mE8kstVerQKMks4OgSWS534Oqo4yunOogEOtZV_zyUr1oWC_knmx5u9qVXZutrZ1en5o_seOU9tqvZvSXZxeT5MY3IMVseqvxj4e_rOW9vN3x5ksePSZut5gKDS6k9tqSZuu9LSLj4SrZxvmxU_lqJIZ0lp4W63rjzJspMg8WW4r_nU_DY2yQLfYQS_zUM1F9CnNR2Ar5Od663rj6t8AGSPticcYlm2erphGv-5QWdQjPakbzTIMBC0.U1Yk0ZDqmhq1TsKspynqn0KY5yFETLn0pyYqnWcd0ATqUvwlnfKdpHdBmy-bIfKspyfqnHb0mv-b5HRd0AdY5HcsPH7xnH0krNtknjDLg1nknWKxnH0YP7tknjc1g1nvnjD0pvbqn0KzIjYknWf0mhbqnHR3g1csP7tznHT0UynqnW0dnNtknj0kg1D3P1fsnjDLPjPxnH0zg1Dsn-tkg100TgKGujYs0Z7Wpyfqn0KzuLw9u1Ys0A7B5HKxn0K-ThTqn0KsTjYYn1fsPj03rHR10A4vTjYsQW0snj0snj0s0AdYTjYs0AwbUL0qn0KzpWYs0Aw-IWdsmsKhIjYs0ZKC5H00ULnqn0KBI1Ykn0K8IjYs0ZPl5fK9TdqGuAnqTZnVUhC0pywW5R420Zw9ThI-IjYvndtsg1nsn0KYIgnqnHDLPHfsPjfkPH6dn1TknW6LP1f0ThNkIjYkPWDsPHf1n10srHms0ZPGujd-uWTsmHnYrj0snj0LPyRL0AP1UHYknRFjP1uDwHfLnDPjnH6s0A7W5HD0IZNY5HD0TA3qn0KkUgfqn0KkUgnqn0KbugwxmLK95H00XMfqn0KVmdqhThqV5HKxn7tsg1KxnH0YP-tsg100uA78IyF-gLK_my4GuZnqn7tsg1KxPjnknjb4PNtYn1DsrHbdg1Kxn0Ksmgwxuhk9u1Ys0AwWpyfqn0K-IA-b5iYk0A71TAPW5H00IgKGUhPW5H00Tydh5H00uhPdIjYs0A-1mvsqn0KlTAkdT1Ys0A7buhk9u1Y30Akhm1Ys0AwWmvfq0Zwzmyw-5HTvnjcsn6KBuA-b5HmLPW03rRnkPbRdrHP7rRfsfYRzwHIjPDF7wjRkfWK70AqW5HD0mMfqn0KEmgwL5H00ULfqnfKETMKY5HcWnanknanzc1nYPWD4n1D1nanknj0snanknj0sna3snj0snj0Wninzc10WnH0Wna3snjbkP16Wna34rH0snj00TNqv5H08rjuxna3sn7tsQW0sg108P1Fxna3vnNtsQWnk0AF1gLKzUvwGujYs0APzm1YYnWbYPf%26word%3D%26ck%3D5753.2.86.264.184.493.202.427%26shh%3Dwww.baidu.com%26sht%3Dbaiduhome_pg%26us%3D1.0.1.0.1.301.0%26wd%3D%26bc%3D110101&g=%2Fwww.zhipin.com%2Fsem%2F10.html%3Fsid%3Dsem%26qudao%3Dbdpc_baidu-pc-BOSS-JD02-B19KA02084%26plan%3D%25E8%25A1%258C%25E4%25B8%259A%25E5%25AE%259A%25E6%258A%2595-%25E5%2593%2581%25E7%2589%258C%26unit%3D%25E9%2580%259A%25E7%2594%25A8%26keyword%3Dwww.hugoboss.cn%26bd_vid%3D9831320416591555231%26csource%3Dboctb&s=3&friend_source=0&s=3&friend_source=0; __a=16946643.1597287018.1609118047.1610543306.72.7.10.10; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1610545493; __zp_stoken__=357fbaTViBRVCZDt8ZzFXSyVvdnBBflhyBVVtTzY5UmU1RRsgelc4UwptbCN3PDF0D3Z%2BLlwhSAkTGEkXPlBXGjESayYfFR9aGWF7ZW1NDDZ7SnRJGwMhPmM4IE1cPCQPCSd0F21fR3dsZHV0LA%3D%3D'
    }
    res = requests.get(url, headers=headers,timeout=5)
    if 200 == res.status_code:
        res = res.content.decode()
        # print(res)
        html = etree.HTML(res)
        job_name_list = html.xpath('.//div[@class="job-title"]//span//a//text()')
        job_name_list = [x.replace('\n', '').replace(' ', '') for x in job_name_list]
        job_name_list = list(filter(None, job_name_list))
        print('职位名称--->len={},{}'.format(len(job_name_list), job_name_list))


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
    pw = 'python'
    city = '101110100'
    position_list(pw, city)

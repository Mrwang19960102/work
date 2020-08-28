# -*- coding: utf-8 -*-
# @File:       |   pratice_wordcloud.py 
# @Date:       |   2020/6/23 11:45
# @Author:     |   ThinkPad
# @Desc:       |   练习词云可视化
import pandas as pd
import wordcloud

# w = wordcloud.WordCloud()
# w.generate('and that government of the people, by the people, for the people, shall not perish from the earth.')
# w.to_file('output1.png')
df = pd.read_excel('d:/work/p_work/select_medicare_drug/202005医保药品数据.xlsx')
print(df.columns)
company_list = list(df['最小包装单位'])
new_name_list = []
for name in company_list:
    new_name = name.replace('有限责任公司', '')
    new_name = new_name.replace('有限公司', '')
    new_name = new_name.replace('股份有限公司', '')
    new_name = new_name.replace('集团股份', '')
    new_name = new_name.replace('集团', '')
    new_name = new_name.replace('股份', '')
    new_name_list.append(new_name)
    print(new_name)
company_str = ', '.join(new_name_list)

w = wordcloud.WordCloud(width=1500,
                        height=800, collocations=False)
w.generate(company_str)
w.to_file('output1.png')




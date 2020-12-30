# -*- coding: utf-8 -*-
# @File:       |   lianjia_plt.py 
# @Date:       |   2020/12/29 9:13
# @Author:     |   ThinkPad
# @Desc:       |  
import jieba
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

dataDf = pd.read_excel('./二手房数据信息.xlsx')
print(dataDf.columns)
# 筛选出需要的字段数据
dataDf = dataDf[['house_name', 'house_tot', 'house_unitPrice', 'area']]
dataDf['house_tot'] = dataDf['house_tot'].apply(lambda x: x.replace('万', ''))
dataDf['house_unitPrice'] = dataDf['house_unitPrice'].apply(
    lambda x: x.replace('万', '').replace('单价', '').replace('元/平米', ''))
dataDf['house_tot'] = dataDf['house_tot'].astype(float)
dataDf['house_unitPrice'] = dataDf['house_unitPrice'].astype(float)

# 按照每个区进行分组，求每个区的房价均值做柱状图
mean_df = dataDf[['house_unitPrice', 'area']].groupby(by='area').agg({'house_unitPrice': 'mean'}).reset_index()
print(mean_df)
area_list = mean_df['area'].tolist()
num_list = mean_df['house_unitPrice'].tolist()
plt.bar(range(len(area_list)), num_list, color='rgb', tick_label=area_list)
plt.xlabel("区名称")
plt.ylabel("均价/元")
plt.title("上海市各区二手房均价柱状图")
plt.show()

# 挑选出一个区的数据  可视化该区的二手房总价的数值分布
print(dataDf.columns)
area_house_df = dataDf[dataDf['area'] == '浦东'][['area', 'house_tot']]
bins = [0, 200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800]
value = area_house_df['house_tot'].tolist()
plt.hist(value, bins)
plt.title("上海市浦东区二手房价分布")
plt.show()

# 词云可视化
wordStr = str(dataDf['house_name'].tolist()).replace('|', '').replace('[', '').replace(']', '').replace(' ', '')
cut_text = jieba.cut(wordStr)
# 必须给个符号分隔开分词结果来形成字符串,否则不能绘制词云
result = " ".join(cut_text)
print(result)
wc = WordCloud(
    # 设置字体，不指定就会出现乱码
    # 设置背景色
    background_color='white',
    # 设置背景宽
    width=500,
    # 设置背景高
    height=350,
    # 最大字体
    max_font_size=50,
    # 最小字体
    min_font_size=10,
    mode='RGBA'
    # colormap='pink'
)
# 产生词云
wc.generate(result)

# 4.显示图片
# 指定所绘图名称
plt.figure("二手房信息词云图")
# 以图片的形式显示词云
plt.imshow(wc)
# 关闭图像坐标系
plt.axis("off")
plt.show()

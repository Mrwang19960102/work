import pandas as pd

df = pd.read_excel('./风险句.xlsx')
print(df.columns)

count_df_by_name_title = df[['info_url', 'content']].groupby(by=['info_url']).count().reset_index()
count_df_by_name_title.sort_values(by='content', inplace=True)
count_df_by_name_title.rename(columns={'content': '按照url来统计风险句的个数count'}, inplace=True)

print(count_df_by_name_title)
print(count_df_by_name_title.columns)
count_df_by_name_title.to_excel('./count_by_url.xlsx', encoding='utf_8_sig', index=False)
print(len(set(df['info_url'])))
# count_df_by_name = df.groupby(by=['name']).count().reset_index()
# count_df_by_name.rename(columns = {'content':'count'},inplace=True)
# print(count_df_by_name)
# print(count_df_by_name.columns)

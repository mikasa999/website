import os
import pandas as pd

# 获取所有拆分好的表格文件名
file_names = [file for file in os.listdir() if file.endswith('_evaluation.xlsx')]

# 创建一个空的DataFrame用于存储合并后的数据
merged_df = pd.DataFrame(columns=['被评价人', '评价人', '评分'])

# 读取每个表格文件，并将数据合并到merged_df中
for file_name in file_names:
    df = pd.read_excel(file_name)
    df['被评价人'] = file_name.split('_')[0]  # 添加被评价人列
    merged_df = merged_df.append(df, ignore_index=True)

# 统计每个人最终获取的评价总分和均分
total_score = merged_df.groupby('被评价人')['评分'].sum().reset_index()
average_score = merged_df.groupby('被评价人')['评分'].mean().reset_index()

# 将评价人列进行格式调整
merged_df['评价人'] = merged_df['评价人'] + '：' + merged_df['评分'].astype(str) + '分'

# 将评价人列进行合并，以被评价人和评价人为分组，用逗号连接
merged_df = merged_df.groupby(['被评价人', '评价人'])['评分'].first().unstack().reset_index()
merged_df = merged_df.fillna('').astype(str)
merged_df['评价分总分值'] = total_score['评分']
merged_df['评价分均分值'] = average_score['评分']

# 将合并后的数据保存为Excel表格
merged_df.to_excel('final_evaluation_summary.xlsx', index=False)

import pandas as pd

# 读取Excel表格数据
df = pd.read_excel('mark.xlsx')

# 遍历每一行数据
for index, row in df.iterrows():
    evaluated_person = row[0]  # 被评价人姓名
    evaluators = row[1].split(',')  # 评价人姓名字符串拆分成列表

    # 创建一个新的DataFrame对象
    new_df = pd.DataFrame({'评价人姓名': evaluators, '评分': 0})

    # 将DataFrame对象保存为Excel表格，以被评价人姓名作为表名
    new_df.to_excel(evaluated_person + '_evaluation.xlsx', index=False)
print('全部拆分成功')

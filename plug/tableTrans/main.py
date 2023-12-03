from pandas import read_excel
from pandas import melt
from time import sleep
from os import listdir
from os.path import join
from os.path import isfile
from os.path import getmtime



# 指定目录路径
directory = './要转换的文件扔这里面/'

# 遍历目录中的文件，并获取最后修改时间
files = []
for filename in listdir(directory):
    file_path = join(directory, filename)
    if isfile(file_path):
        file_time = getmtime(file_path)
        files.append((filename, file_time))

# 按照最后修改时间排序文件名
sorted_files = sorted(files, key=lambda x: x[1], reverse=True)

# 打印排序后的文件名
filename = 1
i = 0
for file in sorted_files:
    filename = file[0]
    i += 1
    if i >= 1:
        break


table_index = input('2.输入要保留的字段名称：')
# 读取xls表
print(f'你选择保留的字段是：{table_index}')

df = read_excel(f'要转换的文件扔这里面/{filename}')

# 逆透视表
df_melt = melt(df, id_vars=[table_index])

print(df_melt)

filename = filename.split(".")[0]
df_melt.to_excel(f'生成的逆透视的文件在这里/{filename}_逆透视.xlsx', index=False)

print('逆透视表已生成，请在save文件夹中查看')

sleep(5)
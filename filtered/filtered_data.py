import pandas as pd
import numpy as np

file_path = '../spider/'  # CSV文件的路径

# 读取CSV文件
df = pd.read_csv(file_path, encoding='utf-8')

# 删除城市不是福州的数据
df = df[df['城市'] == '福州']
# 将原价列中包含关键字"已降"的数据改为NaN
df.loc[df['原价'].str.contains('已降'), '原价'] = np.nan

# 将排放标准列为"纯电动"的驱动方式行修改为燃油标号行的数值
df.loc[df['排放标准'] == '纯电动', '驱动方式'] = df.loc[df['排放标准'] == '纯电动', '燃油标号']
# 将排放标准列为"纯电动"的燃油标号那行修改为空
df.loc[df['排放标准'] == '纯电动', '燃油标号'] = ''

# 将排放标准列为"增程式"的驱动方式行修改为燃油标号行的数值
df.loc[df['排放标准'] == '增程式', '驱动方式'] = df.loc[df['排放标准'] == '增程式', '燃油标号']
# 将排放标准列为"增程式"的燃油标号那行修改为空
df.loc[df['排放标准'] == '增程式', '燃油标号'] = ''

# 将排放标准列为"插电混动"的驱动方式行修改为燃油标号行的数值
df.loc[df['排放标准'] == '插电混动', '驱动方式'] = df.loc[df['排放标准'] == '插电混动', '燃油标号']
# 将排放标准列为"增程式"的燃油标号那行修改为空
df.loc[df['排放标准'] == '插电混动', '燃油标号'] = ''

# 打印结果
print(df.head(10))

# 保存DataFrame到CSV文件
# index=False 不保存索引列
df.to_csv('filtered_che168_fuzhou.csv', index=False, encoding='utf-8')

# 打印保存成功的提示
print("数据已保存到 filtered_che168_fuzhou.csv")

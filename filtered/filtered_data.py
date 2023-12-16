import pandas as pd

file_path = '../spider/che168_fuzhou.csv'  # CSV文件的路径

# 读取CSV文件
df = pd.read_csv(file_path, encoding='utf-8')

# 删除城市不是福州的数据
df = df[df['城市'] == '福州']

# 打印结果
print(df.head(10))

# 保存DataFrame到CSV文件
# index=False 不保存索引列
df.to_csv('filtered_che168_fuzhou.csv', index=False, encoding='utf-8')


# 打印保存成功的提示
print("数据已保存到 filtered_che168_fuzhou.csv")

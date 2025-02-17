import requests
import pandas as pd
import csv 

csv_file = 'D:/vscode/2/project/python_travis.csv'
df = pd.read_csv('D:/vscode/2/project/python-csv/results1.csv')
for index, row in df.iterrows():
    new_data ={'full_name':row['full_name'],'commits':row['commits'],'forks':row['forks'],'createdAt':row['createdAt'],'pushedAt':row['pushedAt'],'updatedAt':row['updatedAt'],'lastCommit':row['lastCommit']}
    if index == 3:
        break 


    with open(csv_file, mode='a', newline='', encoding='utf-8',errors='ignore') as file:
        # 创建一个CSV写入器
        writer = csv.DictWriter(file, fieldnames=new_data.keys())

        # 如果文件是空的（或者是首次写入），就写入表头
        if file.tell() == 0:
            writer.writeheader()

        # 写入新的数据行
        writer.writerow(new_data)

    print(f'已将新数据添加到 {csv_file}')

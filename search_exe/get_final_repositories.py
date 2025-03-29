import os
import pandas as pd
import subprocess
from utils import file_operate

# 读取 CSV 文件
fo = file_operate()
csv_file = "D:/vscode/3/project/search_exe/1.csv"  
df = pd.read_csv(csv_file)
base_download_path = "D:/vscode/3/project/repositories"
for index, row in df.iterrows():
    repo_full_name = row['full_name']
    new_data ={'full_name':row['full_name'],'commits':row['commits'],'releases':row['releases'],'forks':row['forks'],'stargazers':row['stargazers'],'size':row['size'],'createdAt':row['createdAt'],'pushedAt':row['pushedAt'],'updatedAt':row['updatedAt'],'lastCommit':row['lastCommit'],'travisredate':row['travisredate'],'commit_sha':row['commit_sha'],'file_name':['file_name']}
# 指定本地存储目录

    api_url = f"https://github.com/{repo_full_name}"
    output_path = os.path.join(base_download_path, repo_full_name)
    os.makedirs(output_path, exist_ok=True)
    print(f"正在克隆仓库: {api_url} 到 {output_path}")
    result = subprocess.run(["git", "clone", api_url, output_path])
    
    if result.returncode == 0:
        csv_repositiries = 'D:/vscode/3/project/python-csv/123.csv'
        fo.write_file_in(csv_repositiries,new_data)
    else:
        csv_repositiries = 'D:/vscode/3/project/search_exe/2.csv'
        fo.write_file_in(csv_repositiries,new_data)
    
print("所有仓库克隆完成！")
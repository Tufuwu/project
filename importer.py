from search_exe import get_history,file_operate
import os
import time
import pandas as pd
from migrate_exe import add_comments,push_repositories,copy_files

# 配置
github_repo_url = "https://github.com/Tufuwu/test2.git"  # GitHub仓库URL
local_directory = "D:/vscode/1/test2/" # 本地目录，Git仓库所在的目录
csv_file_path = "D:/vscode/3/project/python-csv/repositiries.csv"  # 存放文件路径的CSV文件路径
local_file = "D:/vscode/1/test2/.travis.yml"
api_token = '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'
parent_dir = 'D:/vscode/3/project/data1'


fo =file_operate()
gh = get_history()

# 读取CSV文件，获取文件路径
count = 705

df = pd.read_csv(csv_file_path)
for index, row in df.iterrows():
    repo_full_name = row['full_name']
    base_download_path =f"D:/vscode/3/project/data1/{repo_full_name}/travis.yml"
    
    copy_files(base_download_path,local_file)
    os.chdir(local_directory)
    push_repositories('Update files from CSV')
    add_comments(api_token)
    time.sleep(90)
    
    commits = gh.get_request_commit('Tufuwu/myproject',api_token,str(count))
    data = commits.json()
    for c in data:
        output_dir = os.path.join(parent_dir, repo_full_name)
        fo.split_and_save_diffs(gh.get_commit_diff(c['url'],api_token), output_dir)
    #break
    count+=1


import os
import subprocess
import shutil
import pandas as pd
from utils import add_comments,push_repositories,copy_files

# 配置
github_repo_url = "https://github.com/Tufuwu/test2.git"  # GitHub仓库URL
local_directory = "D:/vscode/1/test2/.travis.yml" # 本地目录，Git仓库所在的目录
csv_file_path = "D:/vscode/3/project/python-csv/repositiries.csv"  # 存放文件路径的CSV文件路径

api_token = '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'
# 确保Git仓库初始化
'''

# 检查当前是否为Git仓库，如果没有则初始化
if not os.path.isdir(".git"):
    subprocess.run(["git", "init"], check=True)
    print("Initialized a new git repository.")

check_remote = subprocess.run(["git", "remote"], capture_output=True, text=True)
if "origin" in check_remote.stdout:
    print("Remote 'origin' already exists. Removing it...")
    subprocess.run(["git", "remote", "remove", "origin"], check=True)
# 设置远程仓库
subprocess.run(["git", "remote", "add", "origin", github_repo_url], check=True)
'''
# 读取CSV文件，获取文件路径

df = pd.read_csv(csv_file_path)
for index, row in df.iterrows():
    repo_full_name = row['full_name']
    base_download_path =f"D:/vscode/3/project/data1/{repo_full_name}/travis.yml"
    file_paths = os.path.join(base_download_path, repo_full_name)
    copy_files(base_download_path,local_directory)
    push_repositories('Update files from CSV')
    add_comments(api_token)
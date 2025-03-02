import os
import subprocess
import shutil
import pandas as pd
from utils import add_comments,push_repositories

# 配置
github_repo_url = "https://github.com/your-username/your-repository.git"  # GitHub仓库URL
local_directory = ""  # 本地目录，Git仓库所在的目录
csv_file_path = "D:/vscode/3/project/python-csv/repositiries.csv"  # 存放文件路径的CSV文件路径
base_download_path ="D:/vscode/3/project/repositories"
api_token = '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'
# 确保Git仓库初始化
os.chdir(local_directory)

# 检查当前是否为Git仓库，如果没有则初始化
if not os.path.isdir(".git"):
    subprocess.run(["git", "init"], check=True)
    print("Initialized a new git repository.")

# 设置远程仓库
subprocess.run(["git", "remote", "add", "origin", github_repo_url], check=True)

# 读取CSV文件，获取文件路径
df = pd.read_csv(csv_file_path)
for index, row in df.iterrows():
    repo_full_name = row['full_name']
    file_paths = os.path.join(base_download_path, repo_full_name)


# 清空当前仓库中的文件
    for root, dirs, files in os.walk(local_directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path != os.path.join(local_directory, ".git"):
                os.remove(file_path)  # 删除文件

    print("Old files removed.")

# 将CSV中列出的文件拷贝到本地仓库
    for file_path in file_paths:
        if os.path.exists(file_path):
            # 拷贝文件到本地Git仓库目录
            shutil.copy(file_path, local_directory)
            print(f"File {file_path} copied to local repository.")
        else:
            print(f"Warning: File {file_path} does not exist.")

    push_repositories('Update files from CSV')
    add_comments(api_token)
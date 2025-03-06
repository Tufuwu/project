import os
import subprocess
import shutil
import pandas as pd
from migrate_exe.utils import add_comments,push_repositories

# 配置
github_repo_url = "https://github.com/Tufuwu/experiment_running.git"  # GitHub仓库URL
local_directory = "D:/vscode/1/file-sync-cmp-master" # 本地目录，Git仓库所在的目录
csv_file_path = "D:/vscode/3/project/python-csv/repositiries.csv"  # 存放文件路径的CSV文件路径
base_download_path ="D:/vscode/repositories"
api_token = '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'
# 确保Git仓库初始化
os.chdir(local_directory)

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

# 读取CSV文件，获取文件路径


repo_full_name = 'metasys-lisbp/isocor'
file_paths = os.path.join(base_download_path, repo_full_name)

# 清空当前仓库中的文件和文件夹（保留 .git）
for item in os.listdir(local_directory):
    item_path = os.path.join(local_directory, item)

    if item == ".git":
        continue  # 保留 .git 目录

    if os.path.isdir(item_path):
        shutil.rmtree(item_path)  # 递归删除文件夹
        print(f"Deleted folder: {item_path}")
    else:
        os.remove(item_path)  # 删除文件
        print(f"Deleted file: {item_path}")

print("✅ Repository cleaned (except .git).")

for item in os.listdir(file_paths):
    item_path = os.path.join(file_paths, item)
    destination_item_path = os.path.join(local_directory, item)

    if os.path.isdir(item_path):  
        # 复制整个文件夹
        shutil.copytree(file_paths, destination_item_path, ignore=shutil.ignore_patterns('.git'), dirs_exist_ok=True)
        print(f"📁 Copied folder: {item_path} → {destination_item_path}")
    else:  
        # 复制文件
        shutil.copy(item_path, local_directory)
        print(f"📄 Copied file: {item_path} → {local_directory}")

print("✅ 所有文件和文件夹复制完成！")

push_repositories('Update files from CSV')
add_comments(api_token)

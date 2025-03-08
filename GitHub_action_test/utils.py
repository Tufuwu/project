import subprocess
import os
import shutil

def delet_file(local_directory):
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

def write_repo_in(repo_path,local_directory):
    for item in os.listdir(repo_path):
        item_path = os.path.join(repo_path, item)
        destination_item_path = os.path.join(local_directory, item)

        if os.path.isdir(item_path):  
            # 复制整个文件夹
            shutil.copytree(repo_path, destination_item_path, ignore=shutil.ignore_patterns('.git'), dirs_exist_ok=True)
            print(f"📁 Copied folder: {item_path} → {destination_item_path}")
        else:  
            # 复制文件
            shutil.copy(item_path, local_directory)
            print(f"📄 Copied file: {item_path} → {local_directory}")

    print("✅ 所有文件和文件夹复制完成！")

def write_file_in(file_path,target_directory):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    with open(target_directory, "w", encoding="utf-8") as f:
        f.writelines(lines)

def upload_repo_test(repo_full_name,base_download_path,local_directory):
    count = 0
    file_path = f"D:/vscode/3/project/data1/{repo_full_name}"
    repo_path = os.path.join(base_download_path, repo_full_name)
    delet_file(local_directory)
    write_repo_in(repo_path)
    workflow_path = os.path.join(repo_path,'.github/workflows')

    delet_file(workflow_path)
    action_file_path = os.path.join(file_path,'action.yml')
    write_file_in(action_file_path,workflow_path)
    push_repositories(f'{repo_full_name}{count}')
    count +=1

    delet_file(workflow_path)
    importer_file_path = os.path.join(file_path,'importer.yml')
    write_file_in(importer_file_path,workflow_path)
    push_repositories(f'{repo_full_name}{count}')
    count +=1

    delet_file(workflow_path)
    gpt_file_path = os.path.join(file_path,'gpt.yml')
    write_file_in(gpt_file_path,workflow_path)
    push_repositories(f'{repo_full_name}{count}')

def inital_repo(local_directory,github_repo_url):
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



def push_repositories(commit_message):

    # 添加文件到Git暂存区
    subprocess.run(["git", "add", "."], check=True)
    print("Files added to staging area.")

# 提交更改
    subprocess.run(["git", "commit", "-m", commit_message], check=True)
    print(f"Changes committed with message: {commit_message}")

# 强制推送到远程仓库（覆盖原仓库中的内容）
    subprocess.run(["git", "push", "-f", "origin", "main"], check=True)  # 如果主分支是main
    print("Changes pushed to GitHub, overwriting the remote repository.")

import subprocess
import os
import shutil
import re
import time
import requests
import csv


def delet_file(local_directory):
    # 清空当前仓库中的文件和文件夹（保留 .git）
    for item in os.listdir(local_directory):
        item_path = os.path.join(local_directory, item)

        if item == ".git" :
            continue  # 保留 .git 目录

        if os.path.isdir(item_path):
            shutil.rmtree(item_path)  # 递归删除文件夹
            print(f"Deleted folder: {item_path}")
        else:
            os.remove(item_path)  # 删除文件
            print(f"Deleted file: {item_path}")

    print("✅ Repository cleaned (except .git).")

def write_repo_in(repo_path, local_directory):
    for item in os.listdir(repo_path):
        if item == ".git":  # 明确忽略 .git 文件夹
            continue  
        item_path = os.path.join(repo_path, item)
        destination_item_path = os.path.join(local_directory, item)

        if os.path.isdir(item_path):  
            # 复制整个文件夹
            shutil.copytree(item_path, destination_item_path, ignore=shutil.ignore_patterns('.git'), dirs_exist_ok=True)
            print(f"📁 Copied folder: {item_path} → {destination_item_path}")
        else:  
            # 复制文件
            shutil.copy(item_path, destination_item_path)
            print(f"📄 Copied file: {item_path} → {destination_item_path}")

    print("✅ 所有文件和文件夹复制完成！")

def fix_action_file(lines):
    result = []
    line_index = 0
    while line_index <len(lines):

        if re.search(r'actions/upload-artifact@v\d',lines[line_index]):
            s = re.sub(r'actions/upload-artifact@v\d','actions/upload-artifact@v4',lines[line_index])
            result.append(s)
            line_index += 1
        elif re.search(r'ubuntu-\d+\.\d+',lines[line_index]):
            run = re.sub(r'ubuntu-\d+\.\d+','ubuntu-latest',lines[line_index])
            result.append(run)
            line_index += 1  
        elif re.search(r'actions/cache@v\d',lines[line_index]):
            s = re.sub(r'actions/cache@v\d','actions/cache@v4',lines[line_index])
            result.append(s)
            line_index += 1           
        elif re.search(r'master',lines[line_index]):
            temp = re.sub(r'master','main',lines[line_index])
            result.append(temp)
            line_index +=1
        elif re.search('python-version:',lines[line_index]):
            if re.search(r'\[.*\]',lines[line_index]):
                temp = re.sub(r'\[.*\]','["3.9"]',lines[line_index])
                result.append(temp)
                line_index +=1
            elif re.search(r'python-version:\n',lines[line_index]):
                temp  = re.sub(r'python-version:','python-version: ["3.9"]',lines[line_index])
                result.append(temp)
                line_index += 1
                while re.search(r'- ',lines[line_index]):
                    line_index += 1
                    if line_index >=len(lines):
                        return result            
            else:
                if re.search(r'\d.\d+\n',lines[line_index]):
                    temp = re.sub(r'\d.\d+\n','3.9\n',lines[line_index])
                else:
                    temp = re.sub(r'\d.\d+','3.9',lines[line_index])
                result.append(temp)
                line_index += 1
        elif re.search('python:',lines[line_index]):
            if re.search(r'\[.*\]',lines[line_index]):
                temp = re.sub(r'\[.*\]','["3.9"]',lines[line_index])
                result.append(temp)
                line_index +=1
            elif re.search(r'python:\n',lines[line_index]):
                temp  = re.sub(r'python:','python: ["3.9"]',lines[line_index])
                result.append(temp)
                line_index += 1
                while re.search(r'- ',lines[line_index]):
                    line_index += 1
                    if line_index >=len(lines):
                        return result            
            else:
                if re.search(r'\d.\d+\n',lines[line_index]):
                    temp = re.sub(r'\d.\d+\n','3.9\n',lines[line_index])
                else:
                    temp = re.sub(r'\d.\d+','3.9',lines[line_index])
                result.append(temp)
                line_index += 1

        else:
            result.append(lines[line_index])
            line_index += 1
    return result

def fix_gpt_file(lines):
    result = []

    for line in lines:
        if re.search("```",line):
            continue
        elif re.search(r'master',line):
            temp = re.sub(r'master','main',line)
            result.append(temp)
        else:
            result.append(line)


    return result

def fix_importer_file(lines):
    result = []
    line_index = 0
    while line_index <len(lines):
        if re.search('concurrency:',lines[line_index]):
            line_index += 1       

        elif re.search('python-version:',lines[line_index]):
            if re.search(r'\[.*\]',lines[line_index]):
                temp = re.sub(r'\[.*\]','["3.9"]',lines[line_index])
                result.append(temp)
                line_index +=1
            elif re.search(r'python-version:\n',lines[line_index]):
                temp  = re.sub(r'python-version:','python-version: ["3.9"]',lines[line_index])
                result.append(temp)
                line_index += 1
                while re.search(r'- ',lines[line_index]):
                    line_index += 1
                    if line_index >=len(lines):
                        return result            
            else:
                if re.search(r'\d.\d+\n',lines[line_index]):
                    temp = re.sub(r'\d.\d+\n','3.9\n',lines[line_index])
                else:
                    temp = re.sub(r'\d.\d+','3.9',lines[line_index])
                result.append(temp)
                line_index += 1
        elif re.search('python:',lines[line_index]):
            if re.search(r'\[.*\]',lines[line_index]):
                temp = re.sub(r'\[.*\]','["3.9"]',lines[line_index])
                result.append(temp)
                line_index +=1
            elif re.search(r'python:\n',lines[line_index]):
                temp  = re.sub(r'python:','python: ["3.9"]',lines[line_index])
                result.append(temp)
                line_index += 1
                while re.search(r'- ',lines[line_index]):
                    line_index += 1
                    if line_index >=len(lines):
                        return result            
            else:
                if re.search(r'\d.\d+\n',lines[line_index]):
                    temp = re.sub(r'\d.\d+\n','3.9\n',lines[line_index])
                else:
                    temp = re.sub(r'\d.\d+','3.9',lines[line_index])
                result.append(temp)
                line_index += 1

        else:
            result.append(lines[line_index])
            line_index += 1
    return result
          
def write_action_in(file_path,target_directory):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    temp = fix_action_file(lines)
    with open(target_directory, "w", encoding="utf-8") as f:
        f.writelines(temp)

def write_importer_in(file_path,target_directory):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    temp = fix_importer_file(lines)
    with open(target_directory, "w", encoding="utf-8") as f:
        f.writelines(temp)

def write_gpt_in(file_path,target_directory):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    temp = fix_gpt_file(lines)
    with open(target_directory, "w", encoding="utf-8") as f:
        f.writelines(temp)

def write_repo(repo_full_name,base_download_path,local_directory):
    repo_path = os.path.join(base_download_path, repo_full_name)
    delet_file(local_directory)

    write_repo_in(repo_path,local_directory)



def upload_action_test(repo_full_name,workflow_path):
    workflow_path = workflow_path
    test_file_path = f'{workflow_path}/test.yml'
    delet_file(workflow_path)
    action_file_path = f"D:/vscode/3/project/data/{repo_full_name}/action.yml"
    write_action_in(action_file_path,test_file_path)
    push_repositories(f'{repo_full_name}/action')
    time.sleep(15)

def upload_gpt4o_test(repo_full_name,workflow_path,count):
    workflow_path = workflow_path
    test_file_path = f'{workflow_path}/test.yml'
    delet_file(workflow_path)
    gpt_file_path = f"D:/vscode/3/project/data_test/{repo_full_name}/gpt-4o/gpt-4o-{count}.yml"
    write_gpt_in(gpt_file_path,test_file_path)
    push_repositories(f'{repo_full_name}/gpt-4o-{count}')
    time.sleep(15)

def upload_gpt4omini_test(repo_full_name,workflow_path):
    workflow_path = workflow_path
    test_file_path = f'{workflow_path}/test.yml'
    gpt_file_path = f"D:/vscode/3/project/data/{repo_full_name}/gpt-4o-mini.yml"
    write_gpt_in(gpt_file_path,test_file_path)
    push_repositories(f'{repo_full_name}/gpt-4o-mini')
    time.sleep(15)

def upload_gpt4omini_test(repo_full_name,workflow_path):
    workflow_path = workflow_path
    test_file_path = f'{workflow_path}/test.yml'
    gpt_file_path = f"D:/vscode/3/project/data/{repo_full_name}/gpt-4o-mini.yml"
    write_gpt_in(gpt_file_path,test_file_path)
    push_repositories(f'{repo_full_name}/gpt-4o-mini')
    time.sleep(15)

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


def get_workflow_file_history(repo_full_name, file_path, api_token,repo_name):
    """
    获取 GitHub 仓库中文件的提交历史记录
    :param repo_full_name: 仓库的完整名称（格式为 'owner/repo'）
    :param file_path: 要查询的文件路径
    :param api_token: GitHub API 的访问令牌
    :return: 提交历史记录列表
    """
    page = 1

    api_url = f"https://api.github.com/repos/{repo_full_name}/commits"
    params = {"path": file_path, "per_page": 100, "page": page}
    headers = {
        "Authorization": f"token {api_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    while True:
        response = requests.get(api_url, headers=headers, params=params)
        if response.status_code != 200:
            print("Error:", response.json())
            break
        
        commits = response.json()
        if not commits:
            break  # 没有更多数据了，结束循环
        
        for c in commits:
            b = c['commit']['message']
            get_wrong_message(api_token,repo_name,c['sha'],b)
        page += 1  # 请求下一页

    return 


def write_csv_in(csv_file,new_data):
        # 打开CSV文件并进行操作
    with open(csv_file, mode='a', newline='', encoding='utf-8',errors='ignore') as file:
        # 创建一个CSV写入器
        writer = csv.DictWriter(file, fieldnames=new_data.keys())

        # 如果文件是空的（或者是首次写入），就写入表头
        if file.tell() == 0:
            writer.writeheader()

        # 写入新的数据行
        writer.writerow(new_data)

    print(f'已将新数据添加到 {csv_file}')

def get_wrong_message(github_token,repo_name,commit_sha,repo_full_name):
    # GitHub 配置信息
    GITHUB_TOKEN = github_token  
    repo_name = repo_name
    COMMIT_SHA = commit_sha # 目标 Commit SHA

    # API 请求头
    HEADERS = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # 获取 commit 相关的 workflow runs
    runs_url = f"https://api.github.com/repos/{repo_name}/actions/runs?head_sha={COMMIT_SHA}"
    response = requests.get(runs_url, headers=HEADERS)

    if response.status_code == 200:
        runs = response.json().get("workflow_runs", [])
        if runs:
            latest_run = runs[0]  # 获取最新的 workflow 运行信息
            run_id = latest_run["id"]
            conclusion = latest_run["conclusion"]

            if conclusion != 'success':
                print(f"❌ Workflow 运行失败 (ID: {run_id})，获取日志...")
                return
                
            else:
                new_data = {'full_name':repo_full_name}
                csv_path = 'D:/vscode/3/project/GitHub_action_test/can_run_file.csv'
                write_csv_in(csv_path,new_data)
                return
        else:
            new_data = {'full_name':repo_full_name}
            csv_path = 'D:/vscode/3/project/GitHub_action_test/no_run_file.csv'
            write_csv_in(csv_path,new_data)
            return
    else:
        print(f"⚠️ 获取 Workflow 运行信息失败，HTTP 状态码: {response.status_code}")

def get_target_history(api_token):
    workflow_file_path = '.github/workflows/'
    repo_name = 'Tufuwu/action_test'
    get_workflow_file_history(repo_name, workflow_file_path, api_token,repo_name)


def write_csv_in(csv_file,new_data):
        # 打开CSV文件并进行操作
    with open(csv_file, mode='a', newline='', encoding='utf-8',errors='ignore') as file:
        # 创建一个CSV写入器
        writer = csv.DictWriter(file, fieldnames=new_data.keys())

        # 如果文件是空的（或者是首次写入），就写入表头
        if file.tell() == 0:
            writer.writeheader()

        # 写入新的数据行
        writer.writerow(new_data)



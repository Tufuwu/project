import requests
import zipfile
import io
import re

def get_workflow_file_history(repo_full_name, file_path, api_token):
    """
    获取 GitHub 仓库中文件的提交历史记录
    :param repo_full_name: 仓库的完整名称（格式为 'owner/repo'）
    :param file_path: 要查询的文件路径
    :param api_token: GitHub API 的访问令牌
    :return: 提交历史记录列表
    """
    api_url = f"https://api.github.com/repos/{repo_full_name}/commits"
    params = {"path": file_path,"per_page": 100, "page": 1}
    headers = {
        "Authorization": f"token {api_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(api_url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()  # 返回提交历史记录
    else:
        raise Exception(f"错误：{response.status_code}, {response.text}")



def get_wrong_message(github_token,repo_full_name,commit_sha):
    # GitHub 配置信息
    GITHUB_TOKEN = github_token  
    repo_full_name = repo_full_name
    COMMIT_SHA = commit_sha # 目标 Commit SHA

    # API 请求头
    HEADERS = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # 获取 commit 相关的 workflow runs
    runs_url = f"https://api.github.com/repos/{repo_full_name}/actions/runs?head_sha={COMMIT_SHA}"
    response = requests.get(runs_url, headers=HEADERS)

    if response.status_code == 200:
        runs = response.json().get("workflow_runs", [])
        if runs:
            latest_run = runs[0]  # 获取最新的 workflow 运行信息
            run_id = latest_run["id"]
            conclusion = latest_run["conclusion"]

            if conclusion != 'success':
                print(f" Workflow 运行失败 (ID: {run_id})，获取日志...")
                
                # 获取失败的日志 ZIP 文件
                logs_url = f"https://api.github.com/repos/{repo_full_name}/actions/runs/{run_id}/logs"
                log_response = requests.get(logs_url, headers=HEADERS)
                
                if log_response.status_code == 200:
                    with zipfile.ZipFile(io.BytesIO(log_response.content)) as z:
                        result_content = ''
                        for log_file in z.namelist():
                    
                            if log_file.endswith(".txt"):  # 只处理文本日志
                                with z.open(log_file) as f:
                                    lines = f.readlines()
                                    count = 0
                                    for line in lines:
                                        count += len(line)
                                    print(count) 
                                    
                                    for line in lines:
                                        decoded_line = line.decode("utf-8").strip()
                                        if "error" in decoded_line.lower() or "fail" in decoded_line.lower():
                                            result_content += decoded_line+'\n'
                        print(f"{result_content}")
                        return(result_content)
                else:
                    print(f" 获取日志失败，HTTP 状态码: {log_response.status_code}")
            else:
                print(f" Workflow 运行成功 (ID: {run_id})")
        else:
            print(" 未找到对应 commit 的 Workflow 运行记录")
    else:
        print(f" 获取 Workflow 运行信息失败，HTTP 状态码: {response.status_code}")

def get_target_history(repo_full_name,api_token,my_repo_name,count):
    workflow_file_path = '.github/workflows/'
    repo_name = 'Tufuwu/'+my_repo_name
    commits = get_workflow_file_history(repo_name, workflow_file_path, api_token)
    for c in commits:
        b = c['commit']['message']
        #print(b)
        if re.search(f"{repo_full_name}/gpt-4o/{count}",b) :
            #print('ssss')
            get_wrong_message(api_token,repo_name,c['sha'])
            break

if __name__ =='__main__':
    repo_full_name = 'ros2/ros2_documentation'
    my_repo_name = 'refixs_gpt-4o'
    api_token = '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'
    count = 0 
    get_target_history(repo_full_name,api_token,my_repo_name,count)
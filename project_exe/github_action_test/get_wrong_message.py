import requests
import zipfile
import io
import re
from project_exe.search_exe import github_token 

def get_workflow_file_history(repo_full_name, file_path, api_token):
    """
    获取 GitHub 仓库中文件的提交历史记录
    :param repo_full_name: 仓库的完整名称（格式为 'owner/repo'）
    :param file_path: 要查询的文件路径
    :param api_token: GitHub API 的访问令牌
    :return: 提交历史记录列表
    """
    page = 1
    per_page = 100
    result = []
    while True:
        url = f"https://api.github.com/repos/{repo_full_name}/commits"
        params = {
            "path": file_path,
            "per_page": per_page,
            "page": page
        }

        headers = {
            "Authorization": f"token {api_token}",
            "Accept": "application/vnd.github.v3+json"  # 如果有 token 更好，防止频率限制
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
        
            data = response.json()
            if not data:
                break 
            result += data
            page += 1
        #print(data)
        else:
            break  # 没有更多数据了

        
    return result



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
        for run in runs:
            if run['actor']['login'] =='Tufuwu':

                 # 获取最新的 workflow 运行信息
                run_id = run["id"]
                conclusion = run["conclusion"]
           
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
                                        #print(count) 
                                        
                                        for line in lines:
                                            decoded_line = line.decode("utf-8").strip()
                                            if "error" in decoded_line.lower() or "fail" in decoded_line.lower():
                                                result_content += decoded_line+'\n'
                            #print(f"{result_content}")
                            return result_content
                    else:
                        
                        return 'The workflow is not valid'
                        print(f" 获取日志失败，HTTP 状态码: {log_response.status_code}")
                else:
                    
                    return 0


    else:
        
        print(f" 获取 Workflow 运行信息失败，HTTP 状态码: {response.status_code}")

def get_target_history(repo_full_name,api_token,my_repo_name,count):
    workflow_file_path = '.github/workflows/'
    repo_name = 'Tufuwu/'+my_repo_name
    commits = get_workflow_file_history(repo_name, workflow_file_path, api_token)
    for c in commits:
        b = c['commit']['message']
        #print(b)
        if re.search(f"{repo_full_name}/gpt-4o-{count}",b) :
            #print('ssss')
            return get_wrong_message(api_token,repo_name,c['sha'])
            

if __name__ =='__main__':
    repo_full_name = 'srittau/python-asserts'
    my_repo_name = 'gpt-4o'
    count = 0 
    get_target_history(repo_full_name,'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',my_repo_name,count)
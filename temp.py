import requests
import pandas as pd
import csv 


def get_workflow_file_history(repo_full_name, file_path, api_token):
    """
    获取 GitHub 仓库中文件的提交历史记录
    :param repo_full_name: 仓库的完整名称（格式为 'owner/repo'）
    :param file_path: 要查询的文件路径
    :param api_token: GitHub API 的访问令牌
    :return: 提交历史记录列表
    """
    api_url = f"https://api.github.com/repos/{repo_full_name}/actions/runs"
    #params = {"path": file_path}
    headers = {
        "Authorization": f"token {api_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.get(api_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch runs for : {response.status_code}")
        return []
    
    data = response.json()
    for run in data.get('workflow_runs', []):
        if run['status'] == 'completed' and run['conclusion'] == 'success':
            print("222")
            break








if __name__ == "__main__":
    # 从 CSV 文件中读取仓库，并获取每个仓库的 workflow 文件提交历史
    api_token = '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'
    repo_full_name = 'jongracecox/anybadge'
    workflow_file_path = '.travis.yml'
    commits = get_workflow_file_history(repo_full_name, workflow_file_path, api_token)

    
    '''
    for run in data.get('workflow_runs', []):
        if run['status'] == 'completed' and run['conclusion'] == 'success':
            print('sss')
    '''

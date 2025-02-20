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
    api_url = f"https://api.github.com/repos/{repo_full_name}/commits"
    params = {"path": file_path}
    headers = {
        "Authorization": f"token {api_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.get(api_url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()  # 返回提交历史记录
    else:
        raise Exception(f"错误：{response.status_code}, {response.text}")







if __name__ == "__main__":
    # 从 CSV 文件中读取仓库，并获取每个仓库的 workflow 文件提交历史
    api_token = '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'
    repo_full_name = 'kovidgoyal/kitty'
    workflow_file_path = '.travis.yml'
    commits = get_workflow_file_history(repo_full_name, workflow_file_path, api_token)
    for c in commits:
        b = c['commit']['message']
        if "Migrate" in b or 'Remove' in b:
            print("sssss")
            print(b)
        #    break
        #print(b)
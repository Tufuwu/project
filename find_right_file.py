import requests
import pandas as pd
import re
import os
from utils import pross_git_file,pross_travis_file

def split_and_save_diffs(diff_content, output_dir):
    # 使用正则表达式来匹配每个 diff 文件的开头
    diff_pattern = re.compile(r'(diff --git a/[\S]+ b/[\S]+)')
    
    # 根据匹配到的 diff 开头分割 diff 内容
    diffs = diff_pattern.split(diff_content)
    
    # diffs[0] 会是空字符串，因为它是第一个 'diff --git' 之前的部分，所以可以忽略
    diffs = diffs[1:]
    
    # diff 文件的文件名计数
    file_count = 1

    for i in range(0, len(diffs), 2):
        # 提取出文件名，确保文件名唯一
        file_identifier = diffs[i].split()[2].replace('b/', '').replace('/', '_')
        if 'git' in file_identifier or 'travis' in file_identifier:
            file_name = f"{file_count}_{file_identifier}.diff"
            file_count += 1
            
            # 获取完整的 diff 内容
            diff_data = diffs[i] + diffs[i + 1]
            if 'git' in file_identifier:
                diff_data = pross_git_file(diff_data)
            else:
                diff_data = pross_travis_file(diff_data)
            # 将每个 diff 文件写入到单独的文件
            output_path = os.path.join(output_dir, file_name)
            with open(output_path, 'w') as f:
                f.write(diff_data)
            print(f"Saved diff to {output_path}")


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


def process_repos_from_csv(csv_file, api_token):
    """
    读取 CSV 文件中的 GitHub 仓库，并获取每个仓库中 workflow 文件的提交历史
    :param csv_file: 包含 GitHub 仓库信息的 CSV 文件
    :param api_token: GitHub API 的访问令牌
    """
    parent_dir = 'D:/vscode/2/project/data1'
    df = pd.read_csv(csv_file)
    for index, row in df.iterrows():
        repo_full_name = row['full_name']
        print(index)
        try:
            # 假设 workflow 文件在 `.github/workflows/` 下
            workflow_file_path = '.github/workflows/'
            print(f"正在获取仓库 {repo_full_name} 的 workflow 文件历史...")
            
            # 获取文件历史
            commits = get_workflow_file_history(repo_full_name, workflow_file_path, api_token)
            
            for c in commits:
                b = c['commit']['message']
                if 'Travis' in b and 'Github' in b :
                    output_dir = os.path.join(parent_dir, repo_full_name)
                    os.makedirs(output_dir, exist_ok=True)
                    split_and_save_diffs(get_commit_diff(c['url'],api_token), output_dir)
        except Exception as e:
            print(f"无法获取 {repo_full_name} 的 workflow 文件历史: {e}")


def get_commit_diff(target_url, api_token):
    # GitHub API 提交的 URL
    url = target_url

    # 设置请求头，指定接受 diff 文件
    headers = {
        "Authorization": f"token {api_token}",
        "Accept": "application/vnd.github.v3.diff"  # 指定接受 diff 文件
    }

    # 发送 GET 请求
    response = requests.get(url, headers=headers)

    # 检查请求是否成功
    if response.status_code == 200:
        return response.text  # 返回 diff 内容
    else:
        raise Exception(f"请求失败: {response.status_code}, {response.text}")

if __name__ == "__main__":
    # 从 CSV 文件中读取仓库，并获取每个仓库的 workflow 文件提交历史
    api_token = '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'
    csv_file = 'python-repos.csv'  # 假设这个CSV文件有 'full_name' 列
    process_repos_from_csv(csv_file, api_token)


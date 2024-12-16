import requests
import json
from utils import get_commit_diff,split_and_save_diffs
import os
import time



# 配置你的 GitHub Token 和搜索关键字
GITHUB_TOKEN = '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'  # 用你自己的 GitHub Personal Access Token 替换
QUERY = 'replace+Travis+GitHub'
REPO = 'username/repo'  # 用你自己的仓库名替换
parent_dir = 'D:/mytxt/project/data3'

# GitHub API URL
API_URL = f"https://api.github.com/search/commits?q={QUERY}"

# 请求头，使用 GitHub API 预览版本
headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.cloak-preview',
}

# 定义获取提交记录的函数
def get_commits(url):
    page = 1002
    per_page = 1  # 每次只获取一条记录
    while True:
        print(f"Fetching page {page}...")

        response = requests.get(url, headers=headers, params={'page': page, 'per_page': per_page})
        data = response.json()

        if response.status_code == 200:
            data = response.json()
            if 'items' not in data or len(data['items']) == 0:
                print("No more commits found.")
                break
            
            # 逐条处理返回的提交记录
            for commit in data['items']:
                yield {
                    'url': commit['url'],
                    'date': commit["commit"]['author']['date'],
                    'repository': commit['repository']['full_name']
                }
            
            # 如果返回的结果少于每页的条数，说明没有更多结果了
            if len(data['items']) < per_page:
                break
            page += 1
        else:
            print(f"Error fetching data: {response.status_code}")
            break

# 获取提交记录并逐条打印
for commit in get_commits(API_URL):
    diff_content=get_commit_diff(commit['url'],GITHUB_TOKEN)

    output_dir = os.path.join(parent_dir, commit['repository']+commit['date'][:10])
    os.makedirs(output_dir, exist_ok=True)
    split_and_save_diffs(diff_content,output_dir)





import requests
import json
from utils import get_commit_diff

# 配置你的 GitHub Token 和搜索关键字
GITHUB_TOKEN = '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'  # 用你自己的 GitHub Personal Access Token 替换
QUERY = 'Travis GitHub in:message'
REPO = 'username/repo'  # 用你自己的仓库名替换

# GitHub API URL
API_URL = f"https://api.github.com/search/commits?q={QUERY}"

# 请求头，使用 GitHub API 预览版本
headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.cloak-preview',
}

# 定义获取提交记录的函数
def get_commits(url):
    commits = []
    page = 1
    per_page = 100  # 每页最多返回100条记录
    while True:
        print(f"Fetching page {page}...")
        response = requests.get(url, headers=headers, params={'page': page, 'per_page': per_page})
        
        if response.status_code == 200:
            data = response.json()
            if 'items' not in data:
                print("No more commits found.")
                break
            
            # 添加返回的提交记录到列表
            commits.extend(data['items'])
            
            # 如果返回的结果少于每页的条数，说明没有更多结果了
            if len(data['items']) < per_page:
                break
            page += 1
        else:
            print(f"Error fetching data: {response.status_code}")
            break
    return commits

# 获取前1000条提交记录
commits = get_commits(API_URL)

# 输出前1000条提交记录
print(f"Total commits fetched: {len(commits)}")

# 打印提交信息
for commit in commits[:1000]:  # 只取前1000条记录
    print(f"Commit SHA: {commit['sha']}")
    print(f"Message: {commit['commit']['message']}")
    print(f"Repository: {commit['repository']['full_name']}")
    print('-' * 50)

# 如果你想将结果保存到文件中
with open('commits.json', 'w') as f:
    json.dump(commits[:1000], f, indent=2)
    print("Saved commits to commits.json")

if __name__ == "__main__":

    response = requests.get(API_URL, headers=headers)
    print(response)
import requests
import subprocess
import os



def add_comments(api_token):
    # GitHub 个人访问令牌 (PAT)
    GITHUB_TOKEN = api_token

    # GitHub 仓库信息
    OWNER = "Tufuwu"
    REPO = "test"
    ISSUE_NUMBER = 2  # Issue ID

    # GitHub API 地址
    GITHUB_API_URL = f"https://api.github.com/repos/{OWNER}/{REPO}/issues/{ISSUE_NUMBER}/comments"

    # 需要提交的评论内容
    comment_body = "/migrate --repository test2 --target-url https://github.com/Tufuwu/myproject"

    # 发送请求的 Headers
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # 发送的 JSON 数据
    data = {
        "body": comment_body
    }

    # 发送 POST 请求
    response = requests.post(GITHUB_API_URL, json=data, headers=headers)

    # 检查是否成功
    if response.status_code == 201:
        print("✅ 评论成功提交到 GitHub Issue #2")
    else:
        print(f"❌ 提交失败: {response.status_code}, {response.text}")


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





def copy_files(source_dir, target_dir):
        source_file = source_dir
        target_file = target_dir
    
        with open(source_file, 'r', encoding='utf-8') as sf, open(target_file, 'w', encoding='utf-8') as tf:
            tf.write(sf.read())
        print(f"已复制  到 {target_dir}")




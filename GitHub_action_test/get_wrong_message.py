import requests
import zipfile
import io
import os

# GitHub 配置信息
GITHUB_TOKEN = "your_personal_access_token"  # 请替换为你的 GitHub Token
OWNER = "your_github_owner"  # 仓库所有者
REPO = "your_repository_name"  # 仓库名称
RUN_ID = "your_run_id"  # 运行 ID，失败的 Workflow Run ID

# API 请求头
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# 获取失败的日志 ZIP 文件
logs_url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs/{RUN_ID}/logs"
response = requests.get(logs_url, headers=HEADERS)

if response.status_code == 200:
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        for log_file in z.namelist():
            if log_file.endswith(".txt"):  # 只处理文本日志
                with z.open(log_file) as f:
                    lines = f.readlines()
                    for line in lines:
                        decoded_line = line.decode("utf-8").strip()
                        if "error" in decoded_line.lower() or "fail" in decoded_line.lower():
                            print(f"❌ 发现错误: {decoded_line}")
else:
    print(f"⚠️ 获取日志失败，HTTP 状态码: {response.status_code}")

import os
import pandas as pd
import subprocess

# 读取 CSV 文件


# 指定本地存储目录
base_download_path = "D:/vscode/3/project/repositories"


# 遍历 CSV 中的仓库名称

repo_full_name ='2gis/k8s-handle'

    # 提取仓库名
api_url = f"https://github.com/{repo_full_name}"

output_path = os.path.join(base_download_path, repo_full_name)
    # 如果仓库已存在，则跳过
os.makedirs(output_path, exist_ok=True)

# 克隆 GitHub 仓库
print(f"正在克隆仓库: {api_url} 到 {output_path}")
result =subprocess.run(["git", "clone", api_url, output_path])
if result.returncode == 0:
    print('ssss')

print("所有仓库克隆完成！")
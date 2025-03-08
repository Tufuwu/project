
import pandas as pd
from utils import upload_repo_test,inital_repo




# 配置
github_repo_url = "https://github.com/Tufuwu/experiment_running.git"  # GitHub仓库URL
local_directory = "D:/vscode/1/file-sync-cmp-master" # 本地目录，Git仓库所在的目录
csv_file_path = "D:/vscode/3/project/python-csv/repositiries.csv"  # 存放文件路径的CSV文件路径
base_repo_path ="D:/vscode/repositories"

api_token = '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'

# 读取CSV文件，获取文件路径
df = pd.read_csv(csv_file_path)
for index, row in df.iterrows():
    repo_full_name = row['full_name']
    inital_repo(local_directory,github_repo_url)
    upload_repo_test(repo_full_name,base_repo_path,local_directory)

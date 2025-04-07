import pandas as pd
from utils import write_repo,inital_repo, upload_gpt4o_test,write_file_in
from get_wrong_message import get_target_history


my_repo_name = 'test3'
# 配置
github_repo_url = f"https://github.com/Tufuwu/{my_repo_name}.git"  # GitHub仓库URL
local_directory = f"D:/vscode/1/{my_repo_name}"                    # 本地目录，Git仓库所在的目录
workflow_path = f"D:/vscode/1/{my_repo_name}/.github/workflows"
csv_file_path = "D:/vscode/3/project/GitHub_action_test/csv_file/success.csv"  # 存放文件路径的CSV文件路径
base_repo_path ="d:/vscode/repo"
api_token = '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'

# 读取CSV文件，获取文件路径
df = pd.read_csv(csv_file_path)

for index, row in df.iterrows():
    repo_full_name = row['full_name']
    count = 0
    try:
        inital_repo(local_directory,github_repo_url)
        write_repo(repo_full_name,base_repo_path,local_directory)
        upload_gpt4o_test(repo_full_name,workflow_path,count)
        #get_target_history(repo_full_name,api_token)

    except:

        csv_file = 'D:/vscode/3/project/GitHub_action_test/errors_files.csv'
        new_data ={'full_name':row['full_name']}
        write_file_in(csv_file,new_data)

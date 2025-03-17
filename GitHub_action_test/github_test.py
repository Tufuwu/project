
import pandas as pd
from utils import upload_repo_test,inital_repo, get_target_history
import csv
import pandas as pd

def write_file_in(csv_file,new_data):
        # 打开CSV文件并进行操作
    with open(csv_file, mode='a', newline='', encoding='utf-8',errors='ignore') as file:
        # 创建一个CSV写入器
        writer = csv.DictWriter(file, fieldnames=new_data.keys())

        # 如果文件是空的（或者是首次写入），就写入表头
        if file.tell() == 0:
            writer.writeheader()

        # 写入新的数据行
        writer.writerow(new_data)

# 配置
github_repo_url = "https://github.com/Tufuwu/action_test.git"  # GitHub仓库URL
local_directory = "D:/vscode/1/action_test"                    # 本地目录，Git仓库所在的目录
workflow_path = f"D:/vscode/1/action_test/.github/workflows"
csv_file_path = "D:/vscode/3/project/repositories/fix_time_2.csv"  # 存放文件路径的CSV文件路径
base_repo_path ="D:/vscode/repositories"

api_token = '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'

# 读取CSV文件，获取文件路径
df = pd.read_csv(csv_file_path)
'''
for index, row in df.iterrows():
    repo_full_name = row['full_name']

    try:
        inital_repo(local_directory,github_repo_url)
        upload_repo_test(repo_full_name,base_repo_path,local_directory,workflow_path)
    except:
        csv_file = 'D:/vscode/3/project/GitHub_action_test/1.csv'
        new_data ={'full_name':row['full_name']}
        write_file_in(csv_file,new_data)
'''


get_target_history(api_token)


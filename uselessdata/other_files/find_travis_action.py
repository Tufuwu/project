import requests
import pandas as pd
import csv 
from utils import get_history,file_operate



def process_repos_from_csv(csv_file, api_token):
    """
    读取 CSV 文件中的 GitHub 仓库，并获取每个仓库中 workflow 文件的提交历史
    :param csv_file: 包含 GitHub 仓库信息的 CSV 文件
    :param api_token: GitHub API 的访问令牌
    """
    df = pd.read_csv(csv_file)
    for index, row in df.iterrows():
        repo_full_name = row['full_name']
        new_data ={'full_name':row['full_name'],'commits':row['commits'],'releases':row['releases'],'forks':row['forks'],'stargazers':row['stargazers'],'size':row['size'],'createdAt':row['createdAt'],'pushedAt':row['pushedAt'],'updatedAt':row['updatedAt'],'lastCommit':row['lastCommit']}
        print(index)
        try:
            # 假设 workflow 文件在 `.github/workflows/` 下
            workflow_file_path = '.github/workflows/'
            travis_file_path = '.travis.yml'
            print(f"正在获取仓库 {repo_full_name} 的 workflow 文件历史...")

            gh = get_history()
            fo = file_operate()
            # 获取文件历史
            action_commits = gh.get_workflow_file_history(repo_full_name, workflow_file_path, api_token)
            travis_commit =  gh.get_workflow_file_history(repo_full_name, travis_file_path, api_token)
            

            if len(action_commits) > 0:
                if len(travis_commit) > 0:

                    # 你要操作的CSV文件路径
                    csv_file = 'D:/vscode/2/project/python_travis.csv'

                    # 新的数据行

                    fo.write_file_in(csv_file,new_data)

                
        except Exception as e:
            print(f"无法获取 {repo_full_name} 的 workflow 文件历史: {e}")




if __name__ == "__main__":
    # 从 CSV 文件中读取仓库，并获取每个仓库的 workflow 文件提交历史
    api_token = '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'
    csv_file = 'D:/vscode/2/project/python-csv/results4.csv'  # 假设这个CSV文件有 'full_name' 列
    process_repos_from_csv(csv_file, api_token)

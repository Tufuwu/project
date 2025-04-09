import pandas as pd
from utils import get_history,file_operate,github_token



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
            print(f"正在获取仓库 {repo_full_name} 的 workflow 文件历史...")
            
            # 获取文件历史
            gh = get_history()
            response = gh.get_workflow_run_history(repo_full_name, workflow_file_path, api_token)
            data = response.json()
            for run in data.get('workflow_runs', []):
                if run['status'] == 'completed' and run['conclusion'] == 'success':
                    # 你要操作的CSV文件路径
                    csv_file = 'D:/vscode/3/project/python-csv/final.csv'

                    # 新的数据行
                    fo = file_operate()
                    fo.write_file_in(csv_file,new_data)
                    break

                    
        except Exception as e:
            print(f"无法获取 {repo_full_name} 的 workflow 文件历史: {e}")




if __name__ == "__main__":
    # 从 CSV 文件中读取仓库，并获取每个仓库的 workflow 文件提交历史
    csv_file = 'D:/vscode/3/project/python-csv/target.csv'  # 假设这个CSV文件有 'full_name' 列
    process_repos_from_csv(csv_file, github_token())

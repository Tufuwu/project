import requests
import pandas as pd
import csv 


def get_workflow_file_history(repo_full_name, file_path, api_token):
    """
    获取 GitHub 仓库中文件的提交历史记录
    :param repo_full_name: 仓库的完整名称（格式为 'owner/repo'）
    :param file_path: 要查询的文件路径
    :param api_token: GitHub API 的访问令牌
    :return: 提交历史记录列表
    """
    api_url = f"https://api.github.com/repos/{repo_full_name}/actions/runs"
    #params = {"path": file_path}
    headers = {
        "Authorization": f"token {api_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.get(api_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch runs for : {response.status_code}")
        return []
    return response


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
            response = get_workflow_file_history(repo_full_name, workflow_file_path, api_token)
            data = response.json()
            for run in data.get('workflow_runs', []):
                if run['status'] == 'completed' and run['conclusion'] == 'success':
                    # 你要操作的CSV文件路径
                    csv_file = 'D:/vscode/2/project/python-csv/active_action.csv'

                    # 新的数据行


                    # 打开CSV文件并进行操作
                    with open(csv_file, mode='a', newline='', encoding='utf-8',errors='ignore') as file:
                        # 创建一个CSV写入器
                        writer = csv.DictWriter(file, fieldnames=new_data.keys())

                        # 如果文件是空的（或者是首次写入），就写入表头
                        if file.tell() == 0:
                            writer.writeheader()

                        # 写入新的数据行
                        writer.writerow(new_data)

                    print(f'已将新数据添加到 {csv_file}')
                    break

                    
        except Exception as e:
            print(f"无法获取 {repo_full_name} 的 workflow 文件历史: {e}")




if __name__ == "__main__":
    # 从 CSV 文件中读取仓库，并获取每个仓库的 workflow 文件提交历史
    api_token = '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'
    csv_file = 'D:/vscode/3/project/python-csv/remove_travis_and_action.csv'  # 假设这个CSV文件有 'full_name' 列
    process_repos_from_csv(csv_file, api_token)

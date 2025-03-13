import requests
import pandas as pd
from utils import file_operate

def get_travis_build_results(owner,repo,api_token):
    """
    获取 Travis CI 上指定公开仓库的构建状态。
    
    :param repo_full_name: GitHub 组织或用户名
    :param api_token: 仓库名
    :return: 构建状态列表
    """
    url = f"https://api.travis-ci.com/repo/{owner}%2F{repo}/builds"

    #headers = {"Travis-API-Version": "3"} 

    headers = {
        'Authorization': f'token {api_token}'
    }


    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        builds = response.json().get('builds', [])
        results = []
        
        for build in builds:
            build_info = {
                "id": build["id"],
                "number": build["number"],
                "state": build["state"],
                "started_at": build["started_at"],
                "finished_at": build["finished_at"]
            }
            results.append(build_info)

        return results
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

api_token = 'RM5yL5KSqUspxHi5tN7MnA'
csv_file = 'D:/vscode/3/project/python-csv/travis_and_action.csv' 
df = pd.read_csv(csv_file)
for index, row in df.iterrows():
    repo_full_name = row['full_name']
    new_data ={'full_name':row['full_name'],'commits':row['commits'],'releases':row['releases'],'forks':row['forks'],'stargazers':row['stargazers'],'size':row['size'],'createdAt':row['createdAt'],'pushedAt':row['pushedAt'],'updatedAt':row['updatedAt'],'lastCommit':row['lastCommit'],'traviscommit':row['traviscommit']}
    repo_full_name = 'joanbm/full-offline-backup-for-todoist'
    owner,repo= repo_full_name.split('/')
    build_results = get_travis_build_results(owner,repo,api_token)
    if build_results:
        for build in build_results:
            if build['state'] =='passed':
                csv_file = 'D:/vscode/3/project/python-csv/active_travis.csv'

                # 新的数据行
                fo = file_operate()
                fo.write_file_in(csv_file,new_data)
                break


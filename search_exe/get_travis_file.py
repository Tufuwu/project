import pandas as pd
from pathlib import Path
from search_exe.utils import file_operate,get_history,github_token

def run_get_travis_file():
    base_dir = Path(__file__).parent.parent

def get_travis_file(base_dir):
    """
    读取 CSV 文件中的 GitHub 仓库，并获取每个仓库中 workflow 文件的提交历史
    :param csv_file: 包含 GitHub 仓库信息的 CSV 文件
    :param api_token: GitHub API 的访问令牌
    """

    csv_file_path = base_dir/"python_csv"/"target3.csv"
    api_token = github_token()

    df = pd.read_csv(csv_file_path)
    for index, row in df.iterrows():
        repo_full_name = row['full_name']
        commit_date = row['travisredate']
        new_data ={'full_name':row['full_name'],'commits':row['commits'],'releases':row['releases'],'forks':row['forks'],'stargazers':row['stargazers'],'size':row['size'],'createdAt':row['createdAt'],'pushedAt':row['pushedAt'],'updatedAt':row['updatedAt'],'lastCommit':row['lastCommit'],'travisredate':row['travisredate'],'commit_sha':0,'file_name':0}
        print(index)

        try:
            # 假设 workflow 文件在 `.github/workflows/` 下
            workflow_file_path = '.github/workflows/'
            print(f"正在获取仓库 {repo_full_name} 的 workflow 文件历史...")

            # 获取文件历史
            gh = get_history()
            fo = file_operate()
            commits = gh.get_workflow_file_history(repo_full_name, workflow_file_path, api_token)

            for c in commits:
                b = c['commit']['message']
                if (fo.re_match("Migrate.*travis",b) or fo.re_match('Move.*travis',b) or fo.re_match('Replace.*travis',b) or fo.re_match('switch.*travis',b)) and commit_date == c['commit']['author']["date"]:
                    output_dir = base_dir/"data"/repo_full_name
                    action_name = fo.split_and_save_diffs(gh.get_commit_diff(c['url'],api_token), output_dir)
                    if action_name:
                        new_data['commit_sha'] = c['sha']
                        new_data['file_name'] = action_name
                        new_data['travisredate'] = c['commit']['author']['date']
                        new_csv_path = base_dir/"python_csv"/"final_csv"/"repo.csv"
                        fo.write_file_in(new_csv_path,new_data)

        except Exception as e:
            file_path =base_dir/"search_exe"/"errer_file.csv"
            fo.write_file_in(file_path,new_data)

 

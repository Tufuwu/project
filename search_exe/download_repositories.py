import os
import subprocess
import pandas as pd
from pathlib import Path
from search_exe.utils import file_operate


def run_download_repo_action():
    base_dir = Path(__file__).parent.parent
    download_repo_action(base_dir)

def download_repo_action(base_dir):
    # 读取 CSV 文件
    fo = file_operate()
    csv_file = base_dir/"python_csv"/"temp.csv"  
    df = pd.read_csv(csv_file)
    base_download_path = base_dir/"repositories"
    for index, row in df.iterrows():
        repo_full_name = row['full_name']
        new_data ={'full_name':row['full_name'],'commits':row['commits'],'releases':row['releases'],'forks':row['forks'],'stargazers':row['stargazers'],'size':row['size'],'createdAt':row['createdAt'],'pushedAt':row['pushedAt'],'updatedAt':row['updatedAt'],'lastCommit':row['lastCommit'],'travisredate':row['travisredate'],'commit_sha':row['commit_sha'],'file_name':row['file_name']}
        file_name = row['file_name']
        version = row['new_commits_sha']

    # 指定本地存储目录

        api_url = f"https://github.com/{repo_full_name}"
        output_path = os.path.join(base_download_path, repo_full_name)
        os.makedirs(output_path, exist_ok=True)
        print(f"正在克隆仓库: {api_url} 到 {output_path}")
        result = subprocess.run(["git", "clone", api_url, output_path])
        
        if result.returncode == 0:
            csv_repositiries = base_dir/"python_csv"/"123.csv"
            fo.write_file_in(csv_repositiries,new_data)
            repo_path = f'D:/vscode/repos/{repo_full_name}'

            subprocess.run(["git", "-C", repo_path, "fetch", "--all"], check=True)
            
            # 切换到指定版本
            subprocess.run(["git", "-C", repo_path, "checkout", version], check=True)
            
            
            print(f"Successfully switched to {version}")
            file_path = f'D:/vscode/repos/{repo_full_name}/.github/workflows/{file_name}'
            target_directory = base_dir/"data"/repo_full_name/"action.yml"
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            with open(target_directory, "w", encoding="utf-8") as f:
                f.writelines(lines)

        else:
            errer_csv_path = base_dir/"search_exe"/"errer_file.csv"
            fo.write_file_in(errer_csv_path,new_data)
        
    print("所有仓库克隆完成！")
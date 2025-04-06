import pandas as pd
import subprocess
from utils import file_operate,get_history


csv_file = 'D:/vscode/3/project/python_csv/final_csv/fix_time.csv'
df = pd.read_csv(csv_file)
fo = file_operate()
for index, row in df.iterrows():
    repo_full_name = row['full_name']
    new_data ={'full_name':row['full_name'],'travisredate':row['travisredate'],'file_name':row['file_name'],'commit_sha':row['commit_sha'],'new_commits_sha':row['new_commits_sha'],'commits_times':row['commits_times']}
    file_name = row['file_name']
    version = row['new_commits_sha']
    try:
        
        repo_path = f'D:/vscode/repos/{repo_full_name}'
        subprocess.run(["git", "-C", repo_path, "fetch", "--all"], check=True)
        
        # 切换到指定版本
        subprocess.run(["git", "-C", repo_path, "checkout", version], check=True)
        
        
        print(f"Successfully switched to {version}")
        file_path = f'D:/vscode/repos/{repo_full_name}/.github/workflows/{file_name}'
        target_directory = f'D:/vscode/3/project/data/{repo_full_name}/action.yml'
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open(target_directory, "w", encoding="utf-8") as f:
            f.writelines(lines)
 
    except Exception as e:
        file_path = "D:/vscode/3/project/search_exe/errer_file.csv"
        fo.write_file_in(file_path,new_data)








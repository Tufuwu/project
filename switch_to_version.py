import subprocess
import sys
import pandas as pd
from search_exe import get_history,file_operate

def switch_git_version(repo_path, version):
    try:
        # 确保路径是一个 Git 仓库
        subprocess.run(["git", "-C", repo_path, "fetch", "--all"], check=True)
        
        # 切换到指定版本
        subprocess.run(["git", "-C", repo_path, "checkout", version], check=True)
        
        
        print(f"Successfully switched to {version}")
    except subprocess.CalledProcessError as e:
        print(f"Error switching to {version}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    csv_file = 'D:/vscode/3/project/python_csv/final_csv/fix_time.csv'
    df = pd.read_csv(csv_file)
    fo = file_operate()
    for index, row in df.iterrows():
        try:
            repo_full_name = row['full_name']
            print(repo_full_name)
            new_data ={'full_name':row['full_name'],'travisredate':row['travisredate'],'file_name':row['file_name'],'commit_sha':row['commit_sha'],'new_commits_sha':row['new_commits_sha'],'commits_times':row['commits_times']}
            version = row['new_commits_sha']
            repo_path = f'D:/vscode/repos/{repo_full_name}'
            
            switch_git_version(repo_path, version)
        except:
            csv_repositiries = 'D:/vscode/3/project/search_exe/errer_file.csv'
            fo.write_file_in(csv_repositiries,new_data)

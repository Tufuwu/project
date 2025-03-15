import subprocess
import sys
import pandas as pd

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
    csv_file = 'D:/vscode/3/project/repositories/fix_time_3.csv'
    df = pd.read_csv(csv_file)
    for index, row in df.iterrows():
        repo_full_name = row['full_name']
        version = row['new_commits_sha']
        repo_path = f'D:/vscode/repositories/{repo_full_name}'
        switch_git_version(repo_path, version)

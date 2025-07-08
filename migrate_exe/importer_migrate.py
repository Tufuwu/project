import os
import time
import pandas as pd
from pathlib import Path
from search_exe import github_token
from search_exe.utils import get_history,file_operate
from migrate_exe.utils import add_comments,push_repositories,copy_files


def run_importer():

    base_dir = Path(__file__).parent.parent

    # 配置
    github_repo_url = "https://github.com/Tufuwu/test2.git"  # GitHub仓库URL
    local_directory = "D:/vscode/1/test2/" # 本地目录，Git仓库所在的目录
    csv_file_path = base_dir/"python_csv"/"final_csv"/"fix_time.csv"  # 存放文件路径的CSV文件路径
    travis_file_path = "D:/vscode/1/test2/.travis.yml"
    parent_dir = 'D:/vscode/3/project/data1'

def importer(base_dir,csv_file_path,local_directory,travis_file_path,parent_dir):
    fo =file_operate()
    gh = get_history()
    api_token = github_token()
    # 确保Git仓库初始化
    '''

    # 检查当前是否为Git仓库，如果没有则初始化
    if not os.path.isdir(".git"):
        subprocess.run(["git", "init"], check=True)
        print("Initialized a new git repository.")

    check_remote = subprocess.run(["git", "remote"], capture_output=True, text=True)
    if "origin" in check_remote.stdout:
        print("Remote 'origin' already exists. Removing it...")
        subprocess.run(["git", "remote", "remove", "origin"], check=True)
    # 设置远程仓库
    subprocess.run(["git", "remote", "add", "origin", github_repo_url], check=True)
    '''
    # 读取CSV文件，获取文件路径
    count = 3

    df = pd.read_csv(csv_file_path)
    for index, row in df.iterrows():
        repo_full_name = row['full_name']
        base_download_path =base_dir/"data"/repo_full_name/"travis.yml"
        copy_files(base_download_path,travis_file_path)
        os.chdir(local_directory)
        push_repositories('Update files from CSV')
        add_comments(api_token)
        time.sleep(90)
        commits = gh.get_request_commit('Tufuwu/myproject',api_token,str(count))
        data = commits.json()
        for c in data:
            output_dir = os.path.join(parent_dir, repo_full_name)
            fo.split_and_save_diffs(gh.get_commit_diff(c['url'],api_token), output_dir)
        count += 1


if __name__ == "__main__":
    pass

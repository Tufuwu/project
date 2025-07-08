from search_exe import get_history,file_operate
import pandas as pd
import os

def process_repos_from_csv(csv_file, api_token):
    """
    读取 CSV 文件中的 GitHub 仓库，并获取每个仓库中 workflow 文件的提交历史
    :param csv_file: 包含 GitHub 仓库信息的 CSV 文件
    :param api_token: GitHub API 的访问令牌
    """
    df = pd.read_csv(csv_file)
    for index, row in df.iterrows():
        repo_full_name = row['full_name']
        new_data ={'full_name':row['full_name'],'commits_date':0,'file_name':0,'commit_sha':0}
        print(index)

        try:
            # 假设 workflow 文件在 `.github/workflows/` 下
            workflow_file_path = '.github/workflows/'
            print(f"正在获取仓库 {repo_full_name} 的 workflow 文件历史...")
            
            # 获取文件历史
            gh = get_history()
            fo = file_operate()
            commits = gh.get_workflow_file_history(repo_full_name, workflow_file_path, api_token)
            commits.reverse() 
            for c in commits:
                b = c['commit']['message']
                if (fo.re_match("Migrate",b) or fo.re_match('Move',b) or fo.re_match('Replace',b) ) and fo.re_match('Travis',b) :
                    new_data['commits_date'] = c['commit']['author']['date']
                    new_data['commit_sha'] = c['sha']
                    s = gh.get_commit_diff(c['url'],api_token)
                    new_data['file_name'] = fo.split_diffs(s)
                    file_path = "D:/vscode/3/project/repositories/fix_time.csv"
                    fo.write_file_in(file_path,new_data)
                    break
                                        
        except Exception as e:
            print(f"无法获取 {repo_full_name} 的 workflow 文件历史: {e}")



if __name__ =="__main__":

    api_token = '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'
    csv_file = 'D:/vscode/3/project/repositories/temp.csv' 
    
    process_repos_from_csv(csv_file,api_token)
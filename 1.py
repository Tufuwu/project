from search_exe import get_history,file_operate
import pandas as pd
from datetime import datetime, timedelta
import re


def process_repos_from_csv(csv_file, api_token):
    """
    读取 CSV 文件中的 GitHub 仓库，并获取每个仓库中 workflow 文件的提交历史
    :param csv_file: 包含 GitHub 仓库信息的 CSV 文件
    :param api_token: GitHub API 的访问令牌
    """
    df = pd.read_csv(csv_file)
    for index, row in df.iterrows():
        repo_full_name = row['full_name']
        file_name = row['file_name']
        file_commit_date = row['commits_date']
        new_data ={'full_name':row['full_name'],'commits_date':row['commits_date'],'file_name':row['file_name'],'commit_sha':row['commit_sha'],'new_commits_sha':0,'commits_times':0}
        print(index)

        try:
            # 假设 workflow 文件在 `.github/workflows/` 下
            workflow_file_path = f'.github/workflows/'
            print(f"正在获取仓库 {workflow_file_path} 的 workflow 文件历史...")
            
            # 获取文件历史
            gh = get_history()
            fo = file_operate()
            commits = gh.get_workflow_file_history(repo_full_name, workflow_file_path, api_token)
            commits.reverse() 
            count = 0
            for c in commits:
                now_date = c['commit']['author']['date']

   
                date_format = "%Y-%m-%dT%H:%M:%SZ"
                date1 = datetime.strptime(file_commit_date, date_format)
                date2 = datetime.strptime(now_date, date_format)
                seven_days_ago = date1 + timedelta(days=7)
                if date2 <= seven_days_ago:
                    diff_content = gh.get_commit_diff(c['url'],api_token)
                    diff_pattern = re.compile(r'(diff --git a/[\S]+ b/[\S]+)')
                    
                    # 根据匹配到的 diff 开头分割 diff 内容
                    diffs = diff_pattern.split(diff_content)
                    diffs = diffs[1:]

                    for file in diffs:
                        if re.search(file_name,file):
                            count += 1
                            file_name = fo.split_new_diffs(diff_content,file_name)
                            row['file_name'] = file_name
                            new_data['new_commits_sha'] = c['sha']
                            break
                else:
                    break
            #break
            new_data['commits_times'] = count -1
            file_path = "D:/vscode/3/project/repositories/fix_time_2.csv"
            fo.write_file_in(file_path,new_data)



                                    
        except Exception as e:
            print(f"无法获取 {repo_full_name} 的 workflow 文件历史: {e}")



if __name__ =="__main__":

    api_token = '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'
    csv_file = 'D:/vscode/3/project/repositories/fix_time.csv' 
    
    process_repos_from_csv(csv_file,api_token)
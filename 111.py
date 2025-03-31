import pandas as pd
import os
from search_exe import get_history,file_operate

csv_file = "D:/vscode/3/project/python-csv/final_csv/repo1.csv"  
df = pd.read_csv(csv_file)
fo = file_operate()
for index, row in df.iterrows():
    repo_full_name = row['full_name']
    new_data ={'full_name':row['full_name'],'commits':row['commits'],'releases':row['releases'],'forks':row['forks'],'stargazers':row['stargazers'],'size':row['size'],'createdAt':row['createdAt'],'pushedAt':row['pushedAt'],'updatedAt':row['updatedAt'],'lastCommit':row['lastCommit'],'travisredate':row['travisredate'],'commit_sha':row['commit_sha'],'file_name':row['file_name']}

    repo_path = f'd:/vscode/repo/{repo_full_name}'
    if os.path.exists(repo_path):
        pass
    else:
        file_path = 'D:/vscode/3/project/python-csv/target3.csv'
        fo.write_file_in(file_path,new_data)
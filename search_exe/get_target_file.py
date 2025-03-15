import pandas as pd
import os
from utils import file_operate,get_history


csv_file = 'D:/vscode/3/project/repositories/fix_time_2.csv'
df = pd.read_csv(csv_file)
for index, row in df.iterrows():
    repo_full_name = row['full_name']
    new_data =row['file_name']

    try:
        file_path = f'D:/vscode/repositories/{repo_full_name}/.github/workflows/{new_data}'
        target_directory = f'D:/vscode/3/project/data1/{repo_full_name}/action.yml'
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open(target_directory, "w", encoding="utf-8") as f:
            f.writelines(lines)
 
    except Exception as e:
        print(f"无法获取 {repo_full_name} 的 workflow 文件历史: {e}")







import pandas as pd
import os

def write_file_in(file_path,target_directory):
    os.makedirs(os.path.dirname(target_directory), exist_ok=True)
    file_name1 = 'action.yml'
    file_name2 = 'action.yml'
    file_path +=file_name1
    target_directory += file_name2
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    with open(target_directory, "w", encoding="utf-8") as f:
        f.writelines(lines)

if __name__ =='__main__':
    csv_file_path = "D:/vscode/3/pr/project_exe/python_csv/final_csv/now_can_run.csv"
    df = pd.read_csv(csv_file_path)

    for index, row in df.iterrows():
        repo_full_name = row['full_name']
        file_path = f'D:/vscode/3/pr/data/{repo_full_name}/'
        target_directory = f'D:/vscode/3/pr/data1/{repo_full_name}/'
        write_file_in(file_path,target_directory)
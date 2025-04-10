import pandas as pd
from project_exe.migrate_exe import  prompt_constructor,read_file,create_gpt_model,creat_deepseek_model,gpt_token,save_file_in 
from project_exe.search_exe import github_token 
from project_exe.github_action_test.get_wrong_message import get_target_history
from project_exe.github_action_test.utils import write_repo,inital_repo, upload_gpt4o_test,write_csv_in
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # 指到项目根目录


my_repo_name = 'gpt-4o'

# 配置
github_repo_url = f"https://github.com/Tufuwu/{my_repo_name}.git"  # GitHub仓库URL
local_directory = f"D:/vscode/1/{my_repo_name}"                    # 本地目录，Git仓库所在的目录
workflow_path = f"D:/vscode/1/{my_repo_name}/.github/workflows"
csv_file_path = "D:/vscode/3/project/project_exe/python_csv/final_csv/now_can_run.csv"  # 存放文件路径的CSV文件路径
base_repo_path ="d:/vscode/repos"
prompt_path = BASE_DIR / 'project_exe' / 'github_action_test' / 'prompt'

# 读取CSV文件，获取文件路径
df = pd.read_csv(csv_file_path)

for index, row in df.iterrows():
    count = 1
    repo_full_name = row['full_name']
 
    file_name = f'gpt-4o-{count}.yml'
    base_path = f'D:/vscode/3/project/data_test'
    #print(repo_full_name)
    error_message = get_target_history(repo_full_name,'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',my_repo_name,count)
    if error_message:
        
        #print(error_message)
        action_path = base_path + f'/{repo_full_name}/gpt-4o/{file_name}'
        s1 = read_file(action_path)
        write_migration_template = prompt_constructor(prompt_path,'1','2')
        prompt =  write_migration_template.format(error_message = error_message,sourcefile_content =s1)
        reponse = create_gpt_model("gpt-4o",gpt_token(),prompt)
        save_file_name = f'gpt-4o-{count+1}.yml'
        save_file_in(base_path,repo_full_name,reponse,save_file_name)
        
        csv_path = 'D:/vscode/3/project/project_exe/python_csv/fix_file_csv/fix_time_1.csv'
        new_data = {'full_name':row['full_name']}
        write_csv_in(csv_path,new_data)
    else:
        csv_path = 'D:/vscode/3/project/project_exe/python_csv/result/fix_result.csv'
        new_data = {'full_name':row['full_name'],'gpt-4o':count+1}

        write_csv_in(csv_path,new_data)
    continue
    try:
        '''
        inital_repo(local_directory,github_repo_url)
        write_repo(repo_full_name,base_repo_path,local_directory)
        upload_gpt4o_test(repo_full_name,workflow_path,count)
        '''
        error_message = get_target_history(repo_full_name,github_token())
        action_path = f'D:/vscode/3/project/data/{repo_full_name}/{file_name}'
        s1 = read_file(action_path)
        write_migration_template = prompt_constructor(prompt_path,'1','2')
        prompt =  write_migration_template.format(error_message = error_message,sourcefile_content =s1)
        reponse = create_gpt_model("gpt-4o-mini",github_token(),prompt)
        print(reponse)
        #write_file_in(repo_full_name,reponse,'gpt-4o-mini.yml')
    except:

        csv_file = 'D:/vscode/3/project/project_exe/GitHub_action_test/errors_files.csv'
        new_data ={'full_name':row['full_name']}
        write_csv_in(csv_file,new_data)

import pandas as pd
from project_exe.migrate_exe import  prompt_constructor,read_file,create_gpt_model,creat_deepseek_model,gpt_token 
from project_exe.search_exe import github_token 
from project_exe.github_action_test.get_wrong_message import get_target_history
from project_exe.github_action_test.utils import write_repo,inital_repo, upload_gpt4o_test,write_file_in


my_repo_name = 'refixs_gpt-4o'
# 配置
github_repo_url = f"https://github.com/Tufuwu/{my_repo_name}.git"  # GitHub仓库URL
local_directory = f"D:/vscode/1/{my_repo_name}"                    # 本地目录，Git仓库所在的目录
workflow_path = f"D:/vscode/1/{my_repo_name}/.github/workflows"
csv_file_path = "D:/vscode/3/project/project_exe/python_csv/final_csv/now_can_run.csv"  # 存放文件路径的CSV文件路径
base_repo_path ="d:/vscode/repos"
prompt_path = 'D:/vscode/3/project/project_exe/github_action_test/prompt'

# 读取CSV文件，获取文件路径
df = pd.read_csv(csv_file_path)

for index, row in df.iterrows():
    repo_full_name = row['full_name']
    file_name = 'gpt-4o.yml'
    my_repo_name = 'refixs_gpt-4o'
    count = 0
    error_message = get_target_history(repo_full_name,github_token(),my_repo_name,count)
    action_path = f'D:/vscode/3/project/data/{repo_full_name}/{file_name}'
    s1 = read_file(action_path)
    write_migration_template = prompt_constructor(prompt_path,'1','2')
    prompt =  write_migration_template.format(error_message = error_message,sourcefile_content =s1)
    reponse = create_gpt_model("gpt-4o-mini",gpt_token(),prompt)
    print(reponse)
    break
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
        write_file_in(csv_file,new_data)

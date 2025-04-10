import pandas as pd
from model import create_gpt_model,read_file,prompt_constructor,save_file_in,creat_deepseek_model
from utils import deepseek_token,gpt_token

csv_file = "D:/vscode/3/project/project_exe/python_csv/final_csv/now_can_run.csv"
base_path = "D:/vscode/3/project/data"
df =pd.read_csv(csv_file)
for index,row in df.iterrows():
    repo_full_name = row['full_name']
    file_path = f"D:/vscode/3/project/data/{repo_full_name}/travis.yml"
    prompt_path = 'D:/vscode/3/project/project_exe/migrate_exe/prompt'
    s1 = read_file(file_path)
    write_migration_template = prompt_constructor(prompt_path,'1','2','3')


    prompt =  write_migration_template.format(sourcelang = 'Travis CI',targetlang = 'Github Action',sourcefile_content =s1 )
    #reponse = creat_deepseek_model(deepseek_token(),prompt) 
    #reponse = create_gpt_model("gpt-4o",gpt_token(),prompt)
    reponse = create_gpt_model("gpt-4o",gpt_token(),prompt)
    print(reponse)
    save_file_in(base_path,repo_full_name,reponse,'gpt-4o.yml')




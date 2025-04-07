import pandas as pd
from model import create_gpt_model,read_file,prompt_constructor,write_file_in,creat_deepseek_model
import time

gpt_api_token="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"
csv_file = "D:/vscode/3/project/project_exe/python_csv/final_csv/now_can_run.csv"
dp_api_token = 'sk-92fdd67f916e40f68b35547955d260ff'
df =pd.read_csv(csv_file)
for index,row in df.iterrows():
    repo_full_name = row['full_name']
    file_path = f"D:/vscode/3/project/data/{repo_full_name}/travis.yml"
    s1 = read_file(file_path)
    write_migration_template = prompt_constructor('1','2','3')


    prompt =  write_migration_template.format(sourcelang = 'Travis CI',targetlang = 'Github Action',sourcefile_content =s1 )
    #reponse = creat_deepseek_model(dp_api_token,prompt) 
    #reponse = create_gpt_model("gpt-4o",gpt_api_token,prompt)
    reponse = create_gpt_model("gpt-4o-mini",gpt_api_token,prompt)
    #print(reponse)
    write_file_in(repo_full_name,reponse,'gpt-4o-mini.yml')



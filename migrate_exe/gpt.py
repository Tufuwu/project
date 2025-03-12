import pandas as pd
from model import create_gpt_model,read_file,prompt_constructor,write_file_in
import time

gpt_api_token="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"
csv_file = "D:/vscode/3/project/GitHub_action_test/success_repo_result.csv"

df =pd.read_csv(csv_file)
for index,row in df.iterrows():
    repo_full_name = row['full_name']
    file_path = f"D:/vscode/3/project/data1/{repo_full_name}/travis.yml"
    s1 = read_file(file_path)
    write_migration_template = prompt_constructor('1','2','3')


    prompt =  write_migration_template.format(sourcelang = 'Travis CI',targetlang = 'Github Action',sourcefile_content =s1 )

    reponse = create_gpt_model("gpt-3.5-turbo",gpt_api_token,prompt)
    print(reponse)
    write_file_in(repo_full_name,reponse)
    time.sleep(10)
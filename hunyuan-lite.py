from openai import OpenAI
from utils import prompt_constructor
import os
import pandas as pd

api_key = "sk-pD0ToEy2oNONeewKSIoWMYAEteBN6QCQ0mGTwIoLPCLL97ws"

client = OpenAI(
    api_key=api_key, # 混元 APIKey
    base_url="https://api.hunyuan.cloud.tencent.com/v1", # 混元 endpoint
)

def read_file(file_path):
    try:
        with open(file_path,"r",encoding= 'utf-8') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")




csv_file = "D:/vscode/3/project/python-csv/temp.csv"
df =pd.read_csv(csv_file)
for index,row in df.iterrows():
    repo_full_name = row['full_name']
    file_path = f"D:/vscode/3/project/data1/{repo_full_name}/travis.yml"
    s1 = read_file(file_path)
    write_migration_template = prompt_constructor('1','2','3')
    prompt =  write_migration_template.format(sourcelang = 'Travis CI',targetlang = 'Github Action',sourcefile_content =s1 )



    completion = client.chat.completions.create(
        model="hunyuan-pro",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
        extra_body={
            "enable_enhancement": False, # <- 自定义参数
        },
    )




    reponse = completion.choices[0].message.content

    file_name = f"gpt.yml"
    output_dir = f"D:/vscode/3/project/data1/{repo_full_name}"
    output_path = os.path.join(output_dir, file_name)
    with open(output_path, 'w') as f:
        f.write(reponse)
    print(f"Saved diff to {output_dir}")
    
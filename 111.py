import pandas as pd
import re

csv_file = 'D:/vscode/3/project/result/1.csv'
def fix_gpt_file(lines):
    result = []

    for line in lines:
        if re.search("```",line):
            continue

        else:
            result.append(line)


    return result

df = pd.read_csv(csv_file)
for index, row in df.iterrows():
    repo_full_name = row['full_name']

    file_path = f'D:/vscode/3/project/data1/{repo_full_name}/gpt.yml'
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    temp = fix_gpt_file(lines)
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(temp)
    break
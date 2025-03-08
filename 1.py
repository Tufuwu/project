import pandas as pd


csv_file = "D:/vscode/3/project/python-csv/temp.csv"
df =pd.read_csv(csv_file)
for index,row in df.iterrows():
    repo_full_name = row['full_name']
    file_path = f"D:/vscode/3/project/data1/{repo_full_name}/gpt.yml"

    # 读取文件内容
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    print(lines)
    break
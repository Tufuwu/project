import requests
import pandas as pd

def get_forks(repo_full_name, token=None):
    url = f"https://api.github.com/repos/{repo_full_name}/forks"
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
    
    forks = []
    page = 1
    while True:
        response = requests.get(url, headers=headers, params={"per_page": 100, "page": page,"sort": "stargazers"})
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.json().get('message', 'Unknown error')}")
            break
        data = response.json()
        for fork in data:
            if fork['stargazers_count'] >=10:
                forks.append(fork['full_name'])
            else:
                return forks
            
        page += 1
    
    return forks



def remove_name_from_csv(file_path, name_to_remove):
    # 读取CSV文件
    df = pd.read_csv(file_path)
    
    # 删除full_name列中匹配指定名称的行
    df_filtered = df[df['full_name'] != name_to_remove]
    
    # 保存修改后的数据回原文件
    df_filtered.to_csv(file_path, index=False)
    
    print(f"已删除包含 '{name_to_remove}' 的行，并保存到 {file_path}")




if __name__ == "__main__":
    csv_file = 'D:/vscode/3/project/python-csv/final_csv/repo.csv' 
    token = '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' # 可选: GitHub 个人访问令牌
    df = pd.read_csv(csv_file)
    for index, row in df.iterrows():
        repo_full_name = row['full_name']
        print(repo_full_name)
        forks = get_forks(repo_full_name, token)
        for fork in forks:
            print(fork,repo_full_name)
            file_path = 'D:/vscode/3/project/python-csv/repo.csv' 
            remove_name_from_csv(file_path, fork)

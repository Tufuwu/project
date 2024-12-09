import requests
import pandas as pd
from dateutil import parser
from github import Github

def search_repo(start_date, out_file, api_token, stars=5, forks=5, lang='Java', verbose=False):
    # 定义 GitHub API 搜索 URL
    api_url = "https://api.github.com/search/repositories" 
    
    # 构建搜索查询
    query = f"language:{lang} stars:>={stars} forks:>={forks} pushed:>={start_date}"
    
    headers = {
        "Authorization": f"token {api_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    params = {
    "q": query,
    "sort": "stars",
    "order": "desc",
    "per_page": 100,  # 每页返回 100 个结果，最大值
    "page": 1  # 从第一页开始
    }
    num_i = 0
    repo_list = []
    while True:
        # 向 GitHub API 发送请求
        response = requests.get(api_url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"错误：{response.status_code}, {response.text}")

        data = response.json()
        repos = data.get('items', [])

        if not repos:
            break  # 如果没有更多数据，跳出循环
        if num_i >890:
            break

        for repo in repos:
            repo_info = {
                'name': repo['name'],
                'full_name': repo['full_name'],
                'url': repo['html_url'],
                'stars': repo['stargazers_count'],
                'forks': repo['forks_count'],
                'pushed_at': repo['pushed_at']
            }
            repo_list.append(repo_info)

            if verbose:
                print(f"发现仓库：{repo_info['name']} 有 {repo_info['stars']} 星和 {repo_info['forks']} 叉子",num_i)
            num_i += 1

        # 准备请求下一页的数据
        params['page'] += 1

    # 将仓库信息保存到 CSV 文件中
    df = pd.DataFrame(repo_list).drop_duplicates(subset='full_name')  # 按 full_name 去重
    df.to_csv(out_file, index=False)
    print(f"已保存 {len(df)} 个仓库到 {out_file}")


    
if __name__ == "__main__":
    date_year = parser.parse("2017-12-31")
    search_repo(start_date=date_year.date(),
                out_file='repos-min-5-forks-.csv',
                api_token='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',
                stars=4,
                lang='Python',
                verbose=True)
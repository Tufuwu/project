import requests

url = 'https://api.github.com/rate_limit'
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    core_limit = data['resources']['core']
    print(f"剩余请求次数: {core_limit['remaining']}")
    print(f"速率限制重置时间: {core_limit['reset']}")
else:
    print(f"获取速率限制状态失败，错误代码: {response.status_code}")
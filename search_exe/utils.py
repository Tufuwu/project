import os
import requests
import re
import csv 


def prompt_constructor(*args):
    prompt = ""
    for arg in args:
        with open(os.path.abspath(f'prompt/{arg}'), 'r') as file:
            prompt += file.read().strip()
    return prompt

class diff_operate():
    
    def __init__(self):
        pass


    def pross_github_file(self,diff_content):
        lines = diff_content.split('\n')

        # 找到name行的下标
        name_index = None
        for i, line in enumerate(lines):
            if line.strip().startswith('@@'):
                name_index = i+1
                break

        # 提取name后的所有行
        updated_lines = lines[name_index :]

        # 去掉每行开头的'+'号
        updated_lines = [line[1:] if line.startswith('+') else line for line in updated_lines]

        # 将提取的行合并成一个字符串
        updated_content = '\n'.join(updated_lines)

        return updated_content
    

    def pross_travis_file(self,diff_content):
        lines = diff_content.split('\n')

        # 找到name行的下标
        name_index = None
        for i, line in enumerate(lines):
            if line.strip().startswith('@@'):
                name_index = i+1
                break

        # 提取name后的所有行
        updated_lines = lines[name_index :]

        # 去掉每行开头的'+'号
        updated_lines = [line[1:] if line.startswith('-') else line for line in updated_lines]

        # 将提取的行合并成一个字符串
        updated_content = '\n'.join(updated_lines)

        return updated_content
    





class file_operate(diff_operate):
    def __init__(self):
        pass


    def re_match(self,tagert,string):
        return re.search(tagert,string,re.I)
    

    def write_file_in(self,csv_file,new_data):
            # 打开CSV文件并进行操作
        with open(csv_file, mode='a', newline='', encoding='utf-8',errors='ignore') as file:
            # 创建一个CSV写入器
            writer = csv.DictWriter(file, fieldnames=new_data.keys())

            # 如果文件是空的（或者是首次写入），就写入表头
            if file.tell() == 0:
                writer.writeheader()

            # 写入新的数据行
            writer.writerow(new_data)

        print(f'已将新数据添加到 {csv_file}')


    def split_and_save_diffs(self,diff_content, output_dir):
        # 使用正则表达式来匹配每个 diff 文件的开头
        diff_pattern = re.compile(r'(diff --git a/[\S]+ b/[\S]+)')
        
        # 根据匹配到的 diff 开头分割 diff 内容
        diffs = diff_pattern.split(diff_content)
        
        # diffs[0] 会是空字符串，因为它是第一个 'diff --git' 之前的部分，所以可以忽略
        diffs = diffs[1:]
        temp = []
        # diff 文件的文件名计数
        file_count = 1

        for i in range(0, len(diffs), 2):
            # 提取出文件名，确保文件名唯一
            file_identifier = diffs[i].split()[2].replace('b/', '').replace('/', '_')
            if 'git' in file_identifier or 'travis' in file_identifier:
                file_name = f"{file_count}_{file_identifier}.diff"

                
                # 获取完整的 diff 内容
                diff_data = diffs[i] + diffs[i + 1]

                if self.re_match('git',file_identifier):
                    diff_data = self.pross_github_file(diff_data)
                    temp.append(diff_data)
                elif self.re_match('travis',file_identifier):
                    diff_data = self.pross_travis_file(diff_data)
                    temp.append(diff_data)
                # 将每个 diff 文件写入到单独的文件
                output_path = os.path.join(output_dir, file_name)
                with open(output_path, 'w') as f:
                    f.write(diff_data)
                print(f"Saved diff to {output_path}")



class get_history():

    def __init__(self):
        pass


    def get_workflow_file_history(self,repo_full_name, file_path, api_token):
        """
        获取 GitHub 仓库中文件的提交历史记录
        :param repo_full_name: 仓库的完整名称（格式为 'owner/repo'）
        :param file_path: 要查询的文件路径
        :param api_token: GitHub API 的访问令牌
        :return: 提交历史记录列表
        """
        api_url = f"https://api.github.com/repos/{repo_full_name}/commits"
        params = {"path": file_path}
        headers = {
            "Authorization": f"token {api_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        response = requests.get(api_url, headers=headers, params=params)
        
        if response.status_code == 200:
            return response.json()  # 返回提交历史记录
        else:
            raise Exception(f"错误：{response.status_code}, {response.text}")
    

    def get_workflow_run_history(self,repo_full_name, file_path, api_token):
        """
        获取 GitHub 仓库中文件的提交历史记录
        :param repo_full_name: 仓库的完整名称（格式为 'owner/repo'）
        :param file_path: 要查询的文件路径
        :param api_token: GitHub API 的访问令牌
        :return: 提交历史记录列表
        """
        api_url = f"https://api.github.com/repos/{repo_full_name}/actions/runs"
        #params = {"path": file_path}
        headers = {
            "Authorization": f"token {api_token}",
            "Accept": "application/vnd.github.v3+json"
        }

        response = requests.get(api_url, headers=headers)
        
        if response.status_code != 200:
            print(f"Failed to fetch runs for : {response.status_code}")
            return []
        return response

    def get_commit_diff(target_url, api_token):
        # GitHub API 提交的 URL
        url = target_url

        # 设置请求头，指定接受 diff 文件
        headers = {
            "Authorization": f"token {api_token}",
            "Accept": "application/vnd.github.v3.diff"  # 指定接受 diff 文件
        }

        # 发送 GET 请求
        response = requests.get(url, headers=headers)

        # 检查请求是否成功
        if response.status_code == 200:
            return response.text  # 返回 diff 内容
        else:
            raise Exception(f"请求失败: {response.status_code}, {response.text}")
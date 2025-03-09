import os

def check_path_exists(path):
    """判断本地路径是否存在"""
    if os.path.exists(path):
        print(f"路径 '{path}' 存在。")
        return True
    else:
        print(f"路径 '{path}' 不存在。")
        return False
check_path_exists('D:/vscode/1/experiment_running/.github/workflow')
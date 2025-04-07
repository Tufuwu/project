import yaml
import ast
import pandas as pd
from itertools import chain
import re

# 解析 YAML 为 Python 对象
def parse_yaml(yaml_content):
    return yaml.safe_load(yaml_content)

# 转换 Python 对象为 AST
def obj_to_ast(obj):
    if isinstance(obj, dict):
        return ast.Dict(keys=[ast.Constant(k) for k in obj.keys()],
                        values=[obj_to_ast(v) for v in obj.values()])
    elif isinstance(obj, list):
        return ast.List(elts=[obj_to_ast(v) for v in obj], ctx=ast.Load())
    elif isinstance(obj, str):
        return ast.Constant(obj)
    elif isinstance(obj, int):
        return ast.Constant(obj)
    elif isinstance(obj, float):
        return ast.Constant(obj)
    elif obj is None:
        return ast.Constant(None)
    else:
        raise TypeError(f"Unsupported type: {type(obj)}")

def pad_sequence(
    sequence,
    n,
    pad_left=False,
    pad_right=False,
    left_pad_symbol=None,
    right_pad_symbol=None,
):
    sequence = iter(sequence)
    if pad_left:
        sequence = chain((left_pad_symbol,) * (n - 1), sequence)
    if pad_right:
        sequence = chain(sequence, (right_pad_symbol,) * (n - 1))
    return sequence

def ngrams(
    sequence,
    n,
    pad_left=False,
    pad_right=False,
    left_pad_symbol=None,
    right_pad_symbol=None,
):
    
    sequence = pad_sequence(sequence, n, pad_left, pad_right, left_pad_symbol, right_pad_symbol)

    history = []
    while n > 1:
        # PEP 479, prevent RuntimeError from being raised when StopIteration bubbles out of generator
        try:
            next_item = next(sequence)
        except StopIteration:
            # no more data, terminate the generator
            return
        history.append(next_item)
        n -= 1
    for item in sequence:
        history.append(item)
        yield tuple(history)
        del history[0]

def remove_comments_and_docstrings(source):
    result = []
    for i in source:
        h = i.find('#')
        if h == -1:
            result.append(i)
        else:
            if h ==0:
                continue
            else:
                for k in range(0,h):
                    if i[k] != '':
                        temp = i[:h]
                        temp += '\n'
                        result.append(temp)
                        break
    return result

def write_file_in(csv_path, full_name, new_data):
    # 读取 CSV 文件
    df = pd.read_csv(csv_path)
    
    # 检查 'full_name' 列是否存在
    if 'full_name' not in df.columns:
        print("Error: 'full_name' column is missing.")
        return
    
    # 遍历 new_data 并更新相应的列
    for key, value in new_data.items():
        if key not in df.columns:
            df[key] = None  # 如果列不存在，就创建该列并初始化为 None
        
        # 仅更新符合 full_name 的行，而不影响其他数据
        df.loc[df['full_name'] == full_name, key] = value
    
    # 仅在所有更新完成后写入原 CSV 文件
    df.to_csv(csv_path, index=False)
    
    print(f'数据已更新，并写入到原文件: {csv_path}')

def fix_file(file_lines):
    result = []
    for line in file_lines:
        if re.search(r'\S',line):
            if re.search('name:',line):
                fix_line = re.sub(r'name:.*\n','name: CI\n',line)
                result.append(fix_line)
            elif re.search('```',line):
                continue
            elif re.search('#',line):
                temp = re.sub(r'#.*\n','\n',line)
                if re.search(r'\S',temp):
                    result.append(temp)
            else:
                result.append(line)
        
    return ''.join(result)

if __name__ == "__main__":
    references_path = "D:/vscode/3/project/data1/20c/rdap/action.yml" 
    with open(references_path, "r", encoding="utf-8") as f:
        references = f.readlines()
        references = fix_file(references)
    print(references)
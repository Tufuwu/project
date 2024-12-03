import os

def prompt_constructor(*args):
    prompt = ""
    for arg in args:
        with open(os.path.abspath(f'prompt/{arg}'), 'r') as file:
            prompt += file.read().strip()
    return prompt


def pross_git_file(diff_content):
    lines = diff_content.split('\n')

    # 找到name行的下标
    name_index = None
    for i, line in enumerate(lines):
        if line.strip().startswith('+name:'):
            name_index = i
            break

    # 提取name后的所有行
    updated_lines = lines[name_index :]

    # 去掉每行开头的'+'号
    updated_lines = [line[1:] if line.startswith('+') else line for line in updated_lines]

    # 将提取的行合并成一个字符串
    updated_content = '\n'.join(updated_lines)

    return updated_content

def pross_travis_file(diff_content):
    lines = diff_content.split('\n')

    # 找到name行的下标
    name_index = None
    for i, line in enumerate(lines):
        if line.strip().startswith('-language:'):
            name_index = i
            break

    # 提取name后的所有行
    updated_lines = lines[name_index :]

    # 去掉每行开头的'+'号
    updated_lines = [line[1:] if line.startswith('-') else line for line in updated_lines]

    # 将提取的行合并成一个字符串
    updated_content = '\n'.join(updated_lines)

    return updated_content
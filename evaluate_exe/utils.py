import yaml
import ast
import json

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

# 读取 YAML 文件
def read_yaml_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

# 主函数
def main():
    yaml_content = """
    name: CI
    on: [push, pull_request]

    jobs:
      build:
        runs-on: ubuntu-latest

        strategy:
          matrix:
            python-version: [3.9, 3.10]

        steps:
        - uses: actions/checkout@v2
        - name: Set up Python ${{ matrix.python-version }}
          uses: actions/setup-python@v2
          with:
            python-version: ${{ matrix.python-version }}
        - name: Install dependencies
          run: |
            python -m pip install --upgrade pip
            pip install pipenv
            pipenv install --dev --system
        - name: Lint with flake8
          run: |
            flake8 .
            flake8 . --exit-zero --select=C,E,F,W
        - name: Test with pytest
          run: pytest
    """
    
    yaml_obj = parse_yaml(yaml_content)
    ast_tree = obj_to_ast(yaml_obj)
    
    print(ast.dump(ast_tree, indent=2))

if __name__ == "__main__":
    main()

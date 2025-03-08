import yaml
import ast
import json
from itertools import chain

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
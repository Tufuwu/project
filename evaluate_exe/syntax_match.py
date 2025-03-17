import yaml
from utils import remove_comments_and_docstrings

class TreeNode:
    def __init__(self, name, children=None):
        self.name = name
        self.children = children if children else []

    def __str__(self):
        """将子树转换成 S-表达式"""
        if not self.children:
            return self.name
        return f"({self.name} {' '.join(str(child) for child in self.children)})"
    
def yaml_to_tree(data, name="root"):
    """递归解析 YAML 数据，构建语法树"""
    if isinstance(data, dict):
        children = [yaml_to_tree(v, k) for k, v in data.items()]
        return TreeNode(name, children)
    elif isinstance(data, list):
        children = [yaml_to_tree(v, f"list_item_{i}") for i, v in enumerate(data)]
        return TreeNode(name, children)
    else:
        return TreeNode(f"{name}: {str(data)}")
    


def calc_syntax_match(references, candidate):
    return corpus_syntax_match([references], [candidate])


def corpus_syntax_match(references_path, candidates_path):

    with open(references_path, "r") as f:
        references = yaml.safe_load(f)
    with open(candidates_path, "r") as f:
        candidates = yaml.safe_load(f)

    #tree = parser.parse(yaml_code.encode("utf8"))
    match_count = 0
    match_count_candidate_to_reference = 0
    total_count = 0


    candidate_tree = yaml_to_tree(candidates)


    reference_tree = yaml_to_tree(references)
    print(candidate_tree)
    print(reference_tree)
    def get_all_sub_trees(root_node):
        node_stack = [(root_node, 1)]  # (节点, 深度)
        sub_tree_sexp_list = []

        while node_stack:
            cur_node, cur_depth = node_stack.pop()
            sub_tree_sexp_list.append((str(cur_node), cur_depth))

            for child_node in cur_node.children:
                node_stack.append((child_node, cur_depth + 1))

        return sub_tree_sexp_list

    cand_sexps = [x[0] for x in get_all_sub_trees(candidate_tree)]
    ref_sexps = [x[0] for x in get_all_sub_trees(reference_tree)]

# TODO: fix, now we count number of reference subtrees matching candidate,
#       but we should count number of candidate subtrees matching reference
#       See (4) in "3.2 Syntactic AST Match" of https://arxiv.org/pdf/2009.10297.pdf

    for sub_tree in ref_sexps:
        if sub_tree in cand_sexps:
            match_count += 1

    for sub_tree in cand_sexps:
        if sub_tree in ref_sexps:
            match_count_candidate_to_reference += 1

    total_count += len(ref_sexps)
    score = match_count / total_count

 #
    return score
    
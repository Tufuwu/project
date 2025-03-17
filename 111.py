from tree_sitter import Parser
from tree_sitter_languages import get_language


file_path = 'D:/vscode/3/project/data1/ariebovenberg/snug/gpt.yml'
parser = Parser()
parser.set_language(get_language("yaml"))
with open(file_path, "r", encoding="utf-8") as f:
    references = f.read()

reference = references





reference_tree = parser.parse(bytes(reference, "utf8")).root_node
#print(reference_tree.sexp()) 
#print(candidate_tree)
#print(reference_tree)
def get_all_sub_trees(root_node):
    node_stack = []
    sub_tree_sexp_list = []
    depth = 1
    node_stack.append([root_node, depth])
    while len(node_stack) != 0:
        cur_node, cur_depth = node_stack.pop()
        sub_tree_sexp_list.append([str(cur_node), cur_depth])
        for child_node in cur_node.children:
            if len(child_node.children) != 0:
                depth = cur_depth + 1
                node_stack.append([child_node, depth])
    return sub_tree_sexp_list

ref_sexps = [x[0] for x in get_all_sub_trees(reference_tree)]
for sub_tree in ref_sexps:
    print(sub_tree)
    break
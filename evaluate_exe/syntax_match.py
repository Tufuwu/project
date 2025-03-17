import yaml
from tree_sitter import Parser
from tree_sitter_languages import get_language
from utils import remove_comments_and_docstrings


def calc_syntax_match(references, candidate):
    return corpus_syntax_match([references], [candidate])


def corpus_syntax_match(references, candidates):
    parser = Parser()
    parser.set_language(get_language("yaml"))

    #tree = parser.parse(yaml_code.encode("utf8"))
    match_count = 0
    match_count_candidate_to_reference = 0
    total_count = 0


    reference = references[0]
    candidate = candidates[0]


    candidate_tree = parser.parse(bytes(candidate, "utf8")).root_node

    reference_tree = parser.parse(bytes(reference, "utf8")).root_node
    #print(candidate_tree.sexp()) 
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
    
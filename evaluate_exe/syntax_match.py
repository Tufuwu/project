from tree_sitter import Language, Parser

Language.build_library("build/my-languages.so", ["tree-sitter-yaml"])
YAML_LANGUAGE = Language("build/my-languages.so", "yaml")

def calc_syntax_match(references, candidate):
    return corpus_syntax_match(references, candidate)


def corpus_syntax_match(reference, candidate):

    #with open(".github/workflows/ci.yml", "r") as f:
    #    yaml_code = f.read()

    parser = Parser()
    parser.set_language(YAML_LANGUAGE)
    #tree = parser.parse(yaml_code.encode("utf8"))
    match_count = 0
    match_count_candidate_to_reference = 0
    total_count = 0




    candidate_tree = parser.parse(bytes(candidate, "utf8")).root_node

    reference_tree = parser.parse(bytes(reference, "utf8")).root_node

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
    # print(f'match_count       {match_count} / {total_count}')
    # print(f'match_count_fixed {match_count_candidate_to_reference} / {total_count}')
    score = match_count / total_count
    return score
    
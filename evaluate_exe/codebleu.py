from bleu import corpus_bleu
from syntax_match import corpus_syntax_match
from weighted_ngram_match import corpus_bleu_1
import os

def calc_codebleu(
    references:list[str],
    keywords_dir: str,
    predictions: list[str],
    weights: tuple[float, float, float, float] = (0.2, 0.2, 0.6),

) -> dict[str, float]:
    

    references = [x.strip() for x in references]
    hypothesis = [x.strip() for x in predictions]



    def tokenizer(s):
        return s.split()

    tokenized_hyps = [tokenizer(x) for x in hypothesis]
    tokenized_refs = [tokenizer(x) for x in references] 
    #ngram_match_score = corpus_bleu(tokenized_refs, tokenized_hyps)

    with open(keywords_dir, "r", encoding="utf-8") as f:
        keywords = [x.strip() for x in f.readlines()]
    def make_weights(reference_tokens, key_word_list):
        return {token: 1 if token in key_word_list else 0.2 for token in reference_tokens}
    
    
    tokenized_refs_with_weights = [
        [[reference_tokens, make_weights(reference_tokens, keywords)] for reference_tokens in reference]
        for reference in tokenized_refs
    ]
    weighted_ngram_match_score = corpus_bleu_1(tokenized_refs_with_weights, tokenized_hyps)
    
    syntax_match_score = corpus_syntax_match(
        references, hypothesis
    )



    alpha, beta, gamma = weights
    code_bleu_score = (
        alpha * ngram_match_score
        + beta * weighted_ngram_match_score
        + gamma * syntax_match_score

    )

    return {
        "codebleu": code_bleu_score,
        "ngram_match_score": ngram_match_score,
        "weighted_ngram_match_score": weighted_ngram_match_score,
        "syntax_match_score": syntax_match_score,

    }

repo_full_name = '3yourmind/django-migration-linter'
file_path = f"D:/vscode/3/project/data1/{repo_full_name}"
references_path = os.path.join(file_path, 'action.yml')
hypothesis_path = os.path.join(file_path, 'gpt.yml')
with open(references_path, "r", encoding="utf-8") as f:
    references = f.readlines()
with open(hypothesis_path, "r", encoding="utf-8") as f:
    hypothesis = f.readlines()

calc_codebleu(references,"D:/vscode/3/project/evaluate_exe/action.txt",hypothesis)
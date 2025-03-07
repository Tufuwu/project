from . import bleu, dataflow_match, syntax_match, weighted_ngram_match

def calc_codebleu(
    references,
    keywords_dir: str,
    predictions: list[str],
    weights: tuple[float, float, float, float] = (0.1, 0.1, 0.4, 0.4),

) -> dict[str, float]:
    

    references = [[x.strip() for x in ref] if isinstance(ref, list) else [ref.strip()] for ref in references]
    hypothesis = [x.strip() for x in predictions]

    if tokenizer is None:

        def tokenizer(s):
            return s.split()
    
    tokenized_hyps = [tokenizer(x) for x in hypothesis]
    tokenized_refs = [tokenizer(x) for x in references] 

    ngram_match_score = bleu.corpus_bleu(tokenized_refs, tokenized_hyps)

    with open(keywords_dir, "r", encoding="utf-8") as f:
        keywords = [x.strip() for x in f.readlines()]
    def make_weights(reference_tokens, key_word_list):
        return {token: 1 if token in key_word_list else 0.2 for token in reference_tokens}
    
    
    tokenized_refs_with_weights = [
        [[reference_tokens, make_weights(reference_tokens, keywords)] for reference_tokens in reference]
        for reference in tokenized_refs
    ]
    weighted_ngram_match_score = weighted_ngram_match.corpus_bleu(tokenized_refs_with_weights, tokenized_hyps)
    
    syntax_match_score = syntax_match.corpus_syntax_match(
        references, hypothesis
    )

    dataflow_match_score = dataflow_match.corpus_dataflow_match(
        references, hypothesis
    )

    alpha, beta, gamma, theta = weights
    code_bleu_score = (
        alpha * ngram_match_score
        + beta * weighted_ngram_match_score
        + gamma * syntax_match_score
        + theta * (dataflow_match_score or 1)
    )

    return {
        "codebleu": code_bleu_score,
        "ngram_match_score": ngram_match_score,
        "weighted_ngram_match_score": weighted_ngram_match_score,
        "syntax_match_score": syntax_match_score,
        "dataflow_match_score": dataflow_match_score,
    }

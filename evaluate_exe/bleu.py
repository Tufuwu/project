import math
from collections import Counter
from utils import ngrams

def sentence_bleu(
    references,
    hypothesis,
    weights=(0.25, 0.25, 0.25, 0.25),
    smoothing_function=None,
    auto_reweigh=False,
):
     return corpus_bleu([references], [hypothesis], weights, smoothing_function, auto_reweigh)

def corpus_bleu(
    list_of_references,
    hypotheses,
    weights=(0.25, 0.25, 0.25, 0.25),
    smoothing_function=None,
    auto_reweigh=False,
):
    p_numerators = Counter()  # Key = ngram order, and value = no. of ngram matches.
    p_denominators = Counter()  # Key = ngram order, and value = no. of ngram in ref.
    hyp_lengths, ref_lengths = 0, 0

    for references, hypothesis in zip(list_of_references, hypotheses):
        for i, _ in enumerate(weights, start=1):
            #print(references)
            #print(hypothesis)
            #break
            p_i_numerator, p_i_denominator = modified_precision(references, hypothesis, i)
            p_numerators[i] += p_i_numerator
            p_denominators[i] += p_i_denominator
            
        hyp_len = len(hypothesis)
        hyp_lengths += hyp_len
        ref_lengths += closest_ref_length(references, hyp_len)

    bp = brevity_penalty(ref_lengths, hyp_lengths)

    if auto_reweigh:
        if hyp_lengths < 4 and weights == (0.25, 0.25, 0.25, 0.25):
            weights = (1 / hyp_lengths,) * hyp_lengths


    p_n = [(p_numerators[i], p_denominators[i]) for i, _ in enumerate(weights, start=1)]

    if p_numerators[1] == 0:
        return 0

    
    if not smoothing_function:
        smoothing_function = SmoothingFunction().method1
    
    p_n = smoothing_function(p_n, references=references, hypothesis=hypothesis, hyp_len=hyp_lengths)
    s = (w_i * math.log(p_i[0] / p_i[1]) for w_i, p_i in zip(weights, p_n))
    s = bp * math.exp(math.fsum(s))
    return s

def modified_precision(references, hypothesis, n):
    counts = Counter(ngrams(hypothesis, n)) if len(hypothesis) >= n else Counter()

    max_counts = {}
    for reference in references:
        reference_counts = Counter(ngrams(reference, n)) if len(reference) >= n else Counter()
        for ngram in counts:
            max_counts[ngram] = max(max_counts.get(ngram, 0), reference_counts[ngram])

    clipped_counts = {ngram: min(count, max_counts[ngram]) for ngram, count in counts.items()}

    numerator = sum(clipped_counts.values())

    denominator = max(1, sum(counts.values()))

    return numerator, denominator

def closest_ref_length(references, hyp_len):
    ref_lens = (len(reference) for reference in references)
    closest_ref_len = min(ref_lens, key=lambda ref_len: (abs(ref_len - hyp_len), ref_len))
    return closest_ref_len

def brevity_penalty(closest_ref_len, hyp_len):
    if hyp_len > closest_ref_len:
        return 1
    # If hypothesis is empty, brevity penalty = 0 should result in BLEU = 0.0
    elif hyp_len == 0:
        return 0
    else:
        return math.exp(1 - closest_ref_len / hyp_len)


class SmoothingFunction:

    def __init__(self, epsilon=0.1, alpha=5, k=5):
        self.epsilon = epsilon
        self.alpha = alpha
        self.k = k
    def method1(self, p_n, *args, **kwargs):
         return [((p_i[0] + self.epsilon), p_i[1]) if p_i[0] == 0 else p_i for p_i in p_n]
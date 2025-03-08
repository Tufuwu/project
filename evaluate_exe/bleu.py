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
     return corpus_bleu(references, hypothesis, weights, smoothing_function, auto_reweigh)

def corpus_bleu(
    references,
    hypotheses,
    weights=(0.25, 0.25, 0.25, 0.25),
    smoothing_function=None,
    auto_reweigh=False,
):
    p_numerators = Counter()  # Key = ngram order, and value = no. of ngram matches.
    p_denominators = Counter()  # Key = ngram order, and value = no. of ngram in ref.
    hyp_lengths, ref_lengths = 0, 0
    for i, _ in enumerate(weights, start=1):
        p_i_numerator, p_i_denominator = modified_precision(references, hypotheses, i)
        p_numerators[i] += p_i_numerator
        p_denominators[i] += p_i_denominator

    hyp_lengths = len(hypotheses)
    ref_lengths = len(references)

    bp = brevity_penalty(ref_lengths, hyp_lengths)

    if auto_reweigh:
        if hyp_lengths < 4 and weights == (0.25, 0.25, 0.25, 0.25):
            weights = (1 / hyp_lengths,) * hyp_lengths

    p_n = [(p_numerators[i], p_denominators[i]) for i, _ in enumerate(weights, start=1)]

    if p_numerators[1] == 0:
        return 0
    
    if not smoothing_function:
        smoothing_function = SmoothingFunction().method1
    
    p_n = smoothing_function(p_n, references=references, hypothesis=hypotheses, hyp_len=hyp_lengths)
    s = (w_i * math.log(p_i[0] / p_i[1]) for w_i, p_i in zip(weights, p_n))
    s = bp * math.exp(math.fsum(s))
    return s

def modified_precision(references, hypotheses, n):
    counts = Counter(ngrams(hypotheses, n)) if len(hypotheses) >= n else Counter()
    # Extract a union of references' counts.
    # max_counts = reduce(or_, [Counter(ngrams(ref, n)) for ref in references])
    max_counts = {}
    for reference in references:
        reference_counts = Counter(ngrams(reference, n)) if len(reference) >= n else Counter()
        for ngram in counts:
            max_counts[ngram] = max(max_counts.get(ngram, 0), reference_counts[ngram])

    # Assigns the intersection between hypothesis and references' counts.
    clipped_counts = {ngram: min(count, max_counts[ngram]) for ngram, count in counts.items()}

    numerator = sum(clipped_counts.values())
    # Ensures that denominator is minimum 1 to avoid ZeroDivisionError.
    # Usually this happens when the ngram order is > len(reference).
    denominator = max(1, sum(counts.values()))

    # return Fraction(numerator, denominator, _normalize=False)
    return numerator, denominator



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
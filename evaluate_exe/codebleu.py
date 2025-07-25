from bleu import corpus_bleu
from syntax_match import corpus_syntax_match
from weighted_ngram_match import corpus_bleu_1
import pandas as pd
from utils import write_file_in,fix_file


def calc_codebleu(
    references:list[str],
    predictions: list[str],
    keywords_dir: str,
    weights: tuple[float, float, float, float] = (0.4, 0.4, 0.2),

) -> dict[str, float]:


    references = [x.strip() for x in references]
    hypothesis = [x.strip() for x in predictions]



    def tokenizer(s):
        return s.split()
    
    tokenized_hyps = []
    tokenized_refs = []
    for x in hypothesis:
        temp = tokenizer(x) 
        for i in temp:
            tokenized_hyps.append(i)
    for x in references:
        temp = tokenizer(x) 
        for i in temp:
            tokenized_refs.append(i)
    tokenized_refs = [[tokenized_refs]]
    tokenized_hyps = [tokenized_hyps]

    ngram_match_score = corpus_bleu(tokenized_refs, tokenized_hyps)
    print(ngram_match_score)

    with open(keywords_dir, "r", encoding="utf-8") as f:
        keywords = [x.strip() for x in f.readlines()]
    def make_weights(reference_tokens, key_word_list):
        return {token: 1 if token in key_word_list else 0.2 for token in reference_tokens}
    
    
    tokenized_refs_with_weights = [
        [[reference_tokens, make_weights(reference_tokens, keywords)] for reference_tokens in reference]
        for reference in tokenized_refs
    ]
    weighted_ngram_match_score = corpus_bleu_1(tokenized_refs_with_weights, tokenized_hyps)
    print(weighted_ngram_match_score)


    syntax_match_score = corpus_syntax_match(
        references, predictions
    )

    print(syntax_match_score)

    alpha, beta, gamma = weights
    code_bleu_score = (
        alpha * ngram_match_score
        + beta * weighted_ngram_match_score
        + gamma * syntax_match_score

    )

    return code_bleu_score,ngram_match_score,weighted_ngram_match_score,syntax_match_score


if __name__ == "__main__":
    csv_file = "D:/vscode/3/project/result/codebleu.csv"
    file_names = ['importer','gpt-3.5','gpt-4o','deepseek']


    for file_name in file_names:
        df = pd.read_csv(csv_file)
        count = 0
        for index, row in df.iterrows():
            repo_full_name = row['full_name']
            references_path = f"D:/vscode/3/project/data1/{repo_full_name}/action.yml"
            hypothesis_path  = f"D:/vscode/3/project/data1/{repo_full_name}/{file_name}.yml"
            with open(references_path, "r", encoding="utf-8") as f:
                references = f.readlines()
                references = [fix_file(references)]
            with open(hypothesis_path, "r", encoding="utf-8") as f:
                predictions = f.readlines()
                predictions = [fix_file(predictions)]
            try:
                rs1,rs2,rs3,rs4 = calc_codebleu(references,predictions,"D:/vscode/3/project/evaluate_exe/action.txt")

                new_data = {file_name: rs1}
                #print(new_data,repo_full_name)
                write_file_in(csv_file,repo_full_name,new_data)
                count += 1
            
            except:
                
                pass

        print(count)
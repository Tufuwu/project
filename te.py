import yaml
'''
file_path = 'D:/vscode/3/project/data1/3yourmind/django-migration-linter/action.yml'
predictions = [x.strip() for x in open(file_path, "r", encoding="utf-8").readlines()]
print(len(predictions))
hypothesis = [x.strip() for x in predictions]
def tokenizer(s):
    return s.split()
tokenized_hyps = [tokenizer(x) for x in hypothesis]
#print(tokenized_hyps)
'''
def tokenizer(s):
    return s.split()
predictions = ["This is a test.", "Another test."]
pre_references = [
    ["This is a reference.", "Another reference."],
    ["This is another reference.", "Yet another reference."]
]

references = []

for i in range(len(predictions)):
    ref_for_instance = []
    for j in range(len(pre_references)):
        ref_for_instance.append(pre_references[j][i])
    references.append(ref_for_instance)
references = [[x.strip() for x in ref] if isinstance(ref, list) else [ref.strip()] for ref in references]
hypothesis = [x.strip() for x in predictions]
def tokenizer(s):
    return s.split()

tokenized_hyps = [tokenizer(x) for x in hypothesis]
tokenized_refs = [[tokenizer(x) for x in reference] for reference in references]

print(tokenized_refs)
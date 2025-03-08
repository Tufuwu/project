from pathlib import Path
from . import calc_codebleu
PACKAGE_DIR = Path(__file__).parent
import os






repo_full_name = '3yourmind\django-migration-linter'
file_path = f"D:/vscode/3/project/data1/{repo_full_name}"
references_path = os.path.join(file_path, 'action.yml')
hypothesis_path = os.path.join(file_path, 'gpt.yml')
with open(references_path, "r", encoding="utf-8") as f:
    references = f.readlines()
with open(hypothesis_path, "r", encoding="utf-8") as f:
    hypothesis = f.readlines

calc_codebleu(references,"D:/vscode/3/project/evaluate_exe/action.txt",h)
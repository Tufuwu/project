from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from utils import write_file_in,fix_file

file_names = ['importer','gpt-3.5','gpt-4o','deepseek']
csv_file = f'D:/vscode/3/project/result/cosine.csv'

for file_name in file_names:

    df = pd.read_csv(csv_file)
    # 读取文件内容
    for index, row in df.iterrows():

        repo_full_name = row['full_name']
        file1_path = f'D:/vscode/3/project/data1/{repo_full_name}/action.yml'
        with open(file1_path, 'r', encoding='utf-8') as f:
            text1 = f.readlines()
            text1 =fix_file(text1)

        file2_path = f'D:/vscode/3/project/data1/{repo_full_name}/{file_name}.yml'
        with open(file2_path, 'r', encoding='utf-8') as f:
            text2 = f.readlines()
            text2 =fix_file(text2)

        # 初始化 TF-IDF 向量器
        vectorizer = TfidfVectorizer()

        # 转换文本为TF-IDF矩阵
        tfidf_matrix = vectorizer.fit_transform([text1, text2])

        # 计算余弦相似度
        cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        new_data = {file_name:cosine_sim[0][0]}
        #print(cosine_sim[0][0])

        write_file_in(csv_file,repo_full_name,new_data)


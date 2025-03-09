from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import os
from search_exe import file_operate

csv_file = f'D:/vscode/3/project/result/1.csv'
df = pd.read_csv(csv_file)
# 读取文件内容
for index, row in df.iterrows():

    repo_full_name = row['full_name']
    new_data ={'full_name':row['full_name'],'gpt_result':0,'importer_result':row['importer_result']}

    file1_path = f'D:/vscode/3/project/data1/{repo_full_name}/action.yml'
    with open(file1_path, 'r', encoding='utf-8') as f1:
        text1 = f1.read()
    file2_path = f'D:/vscode/3/project/data1/{repo_full_name}/gpt.yml'
    with open(file2_path, 'r', encoding='utf-8') as f2:
        text2 = f2.read()

    # 初始化 TF-IDF 向量器
    vectorizer = TfidfVectorizer()

    # 转换文本为TF-IDF矩阵
    tfidf_matrix = vectorizer.fit_transform([text1, text2])

    # 计算余弦相似度
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    new_data['gpt_result'] = cosine_sim[0][0]
    #print(cosine_sim[0][0])

    fo = file_operate()
    csv_repositiries = 'D:/vscode/3/project/result/cosine_similarity.csv'
    fo.write_file_in(csv_repositiries,new_data)


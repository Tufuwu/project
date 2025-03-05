from search_exe import file_operate
import os
import pandas as pd




if __name__ == "__main__":
    
    csv_file = "D:/vscode/3/project/python-csv/target.csv"
    
    df = pd.read_csv(csv_file)

    for index, row in df.iterrows():
        repo_full_name = row['full_name']
        new_data ={'full_name':row['full_name'],'commits':row['commits'],'releases':row['releases'],'forks':row['forks'],'stargazers':row['stargazers'],'size':row['size'],'createdAt':row['createdAt'],'pushedAt':row['pushedAt'],'updatedAt':row['updatedAt'],'lastCommit':row['lastCommit'],'travisredate':row['travisredate']}
        file_path = f"D:/vscode/3/project/data1/{repo_full_name}/importer.yml"
        if os.path.exists(file_path):
            fo = file_operate()
            csv_repositiries = 'D:/vscode/3/project/python-csv/temp.csv'
            fo.write_file_in(csv_repositiries,new_data)










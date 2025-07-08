import pandas as pd
from pathlib import Path
from search_exe import file_operate
from migrate_exe.utils import prompt_constructor,save_file_in,read_file
from migrate_exe.model_create import create_gpt_model,creat_deepseek_model,deepseek_token,gpt_token


def run_migrate(model_name):

    base_dir = Path(__file__).parent.parent
    csv_file_path = base_dir/"python_csv"/"final_csv"/"fix_time.csv"
    save_path = base_dir/"data"
    migrate(base_dir,csv_file_path,save_path,model_name)


def migrate(base_dir,csv_file_path,save_path,model_name):

    df =pd.read_csv(csv_file_path)

    for index,row in df.iterrows():
        repo_full_name = row['full_name']
        new_data = {'full_name':repo_full_name}
        travis_file_path = base_dir/"data"/repo_full_name/"travis.yml"
        prompt_path = base_dir/"migrate_exe"/"prompt"


        travis_file = read_file(travis_file_path)
        write_migration_template = prompt_constructor(prompt_path,'1','3')
        prompt =  write_migration_template.format(sourcelang = 'Travis CI',targetlang = 'Github Action',sourcefile_content =travis_file )
        fo = file_operate()

        try:

            if model_name == 'gpt-4o':
            #reponse = create_gpt_model("gpt-4o",gpt_token(),prompt)
                reponse = create_gpt_model("gpt-4o",gpt_token(),prompt)
                save_file_in(save_path,repo_full_name,reponse,'gpt-4o.yml')

            elif model_name == 'gpt-4o-mini':

                reponse = create_gpt_model("gpt-4o-mini",gpt_token(),prompt)
                save_file_in(save_path,repo_full_name,reponse,'gpt-4o-mini.yml')
                print(reponse)


        except:

            errer_file_path = base_dir/"migrate_exe"/"errer_file.csv"
            fo.write_file_in(errer_file_path,new_data)






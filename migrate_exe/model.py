from openai import OpenAI
import os



def create_gpt_model(model_tag, api_token, prompt):
    client = OpenAI(api_key=api_token)

    completion = client.chat.completions.create(
        model=model_tag,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return completion.choices[0].message.content 



def creat_deepseek_model(api_token,prompt):
    client = OpenAI(api_key=api_token, base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content":prompt},
        ],

        temperature=0,

        stream=False
        
    )

    return response.choices[0].message.content

def read_file(file_path):
    try:
        with open(file_path,"r",encoding= 'utf-8') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def write_file_in(repo_full_name,reponse,file_name):

    file_name = file_name
    output_dir = f"D:/vscode/3/project/data1/{repo_full_name}"
    output_path = os.path.join(output_dir, file_name)
    with open(output_path, 'w') as f:
        f.write(reponse)
    print(f"Saved diff to {output_dir}")
    
def prompt_constructor(*args):
    prompt = ""
    prompt_path = 'D:/vscode/3/project/migrate_exe/prompt'
    for arg in args:
        with open(os.path.abspath(f'{prompt_path}/{arg}'), 'r') as file:
            prompt += file.read().strip()
    return prompt
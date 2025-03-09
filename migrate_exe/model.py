from openai import OpenAI
import os



def create_model(model_tag,api_token,prompt):
    client = OpenAI(
    api_key=api_token
    )

    completion = client.chat.completions.create(
    model=model_tag,
    store=True,
    messages=[
        {"role": "user", "content": prompt}
    ]
    )

    return completion.choices[0].message


def read_file(file_path):
    try:
        with open(file_path,"r",encoding= 'utf-8') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def write_file_in(file_name,repo_full_name,reponse):

    file_name = f"gpt.yml"
    output_dir = f"D:/vscode/3/project/data1/{repo_full_name}"
    output_path = os.path.join(output_dir, file_name)
    with open(output_path, 'w') as f:
        f.write(reponse)
    print(f"Saved diff to {output_dir}")
    
def prompt_constructor(*args):
    prompt = ""
    for arg in args:
        with open(os.path.abspath(f'prompt/{arg}'), 'r') as file:
            prompt += file.read().strip()
    return prompt
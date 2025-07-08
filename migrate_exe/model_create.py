from openai import OpenAI
from dotenv import load_dotenv
import os



def create_gpt_model(model_tag, api_token, prompt):

    client = OpenAI(api_key=api_token)

    completion = client.chat.completions.create(
        model=model_tag,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
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


def gpt_token():

    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    return api_key

def deepseek_token():
    
    load_dotenv()
    api_key = os.getenv("DEEPSEEK_API_KEY")
    return api_key


from openai import OpenAI
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

    return "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"

def deepseek_token():
    
    return "sk-92fdd67f916e40f68b35547955d260ff"


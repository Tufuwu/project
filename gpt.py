from openai import OpenAI
from utils import prompt_constructor

api_key = "sk-pD0ToEy2oNONeewKSIoWMYAEteBN6QCQ0mGTwIoLPCLL97ws"

client = OpenAI(
    api_key=api_key, # 混元 APIKey
    base_url="https://api.hunyuan.cloud.tencent.com/v1", # 混元 endpoint
)

s1 = '''language: java
sudo: false
install: true

jdk:
  - openjdk8
  - openjdk11
  - openjdk12
  #  - openjdk13
  - openjdk-ea
  #  - oraclejdk8
  - oraclejdk11

matrix:
  allow_failures:
    - jdk: openjdk-ea

env:
  - AWS_TEST_BUCKET=s3-tests.s3-eu-west-1.amazonaws.com
  - AWS_TEST_BUCKET=s3.eu-central-1.amazonaws.com/s3-tests-2
  - AWS_TEST_BUCKET=s3.amazonaws.com/s3-tests-3

after_success:
  - mvn -V -B -e jacoco:report
  - bash <(curl -s https://codecov.io/bash)


'''
write_migration_template = prompt_constructor('h1','h2','h3','h6','h5')
prompt =  write_migration_template.format(sourcelang = 'Travis CI',targetlang = 'Github Action',sourcefile = '1',sourcefile_content =s1 ,guidelines=None)



completion = client.chat.completions.create(
    model="hunyuan-pro",
    messages=[
        {
            "role": "user",
            "content": prompt,
        },
    ],
    extra_body={
        "enable_enhancement": False, # <- 自定义参数
    },
)




reponse = completion.choices[0].message.content
print(reponse)
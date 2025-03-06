from openai import OpenAI

client = OpenAI(
  api_key="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"
)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

print(completion.choices[0].message)

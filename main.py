# Please install OpenAI SDK first: `pip3 install openai`
# sk-4b65eccd8f66448eb9dd1fcc57d66241
import os
from openai import OpenAI

#调用模型和接口
client = OpenAI(
    api_key="sk-4b65eccd8f66448eb9dd1fcc57d66241",
    base_url="https://api.deepseek.com"
)

#创建回复
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"}
    ]
)

print(response.choices[0].message.content)
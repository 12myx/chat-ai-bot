# Please install OpenAI SDK first: `pip3 install openai`
import os
from openai import OpenAI

# 从环境变量获取API密钥
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    raise ValueError("请设置环境变量 DEEPSEEK_API_KEY")

#调用模型和接口
client = OpenAI(
    api_key=api_key,
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
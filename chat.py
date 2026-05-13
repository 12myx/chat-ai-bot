from openai import OpenAI
import json

client = OpenAI(
    api_key="sk-4b65eccd8f66448eb9dd1fcc57d66241",
    base_url="https://api.deepseek.com"
)

# 聊天记录
try:
    with open("messages.json", "r", encoding="utf-8") as f:
        messages = json.load(f)

except (FileNotFoundError, json.JSONDecodeError):
    messages = [
        {
            "role": "system",
            "content": "你是一个AI英语陪练"
        }
    ]

print("AI聊天开始，输入 quit 退出")

#连续聊天机制：输入->读取->保存->请求AI->输出->保存
while True:
    # 用户输入
    user_input = input("陈文坚：")

    # 退出
    if user_input.lower() == "quit":
        print("聊天结束")
        break

    # 保存用户消息
    messages.append({
        "role": "user",
        "content": user_input
    })
    with open("messages.json", "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)

    # 请求AI
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        stream=True
    )

    # 获取AI回复
    print("陈文坚助手：", end="")

    ai_reply = ""

    for chunk in response:
        content = chunk.choices[0].delta.content

        if content:
            print(content, end="", flush=True)
            ai_reply += content

    print()

    # 保存AI回复
    messages.append({
        "role": "assistant",
        "content": ai_reply
    })
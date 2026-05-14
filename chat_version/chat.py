import os
from openai import OpenAI
import json

# 尝试从 .env 文件加载环境变量
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# 从环境变量获取API密钥
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    raise ValueError("请设置环境变量 DEEPSEEK_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

#定义人格
system_prompt = "你是一个AI英语陪练"

# 聊天记录（异常捕捉）
try:
    with open("messages.json", "r", encoding="utf-8") as f:
        messages = json.load(f)

#讲用户记录保存为JSON文件，json文件为空或者不存在时，初始化聊天记录
except (FileNotFoundError, json.JSONDecodeError):
    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

print("AI聊天开始，输入 quit 退出")


#连续聊天机制：输入->读取->保存->请求AI->输出->保存
while True:
    # 用户输入
    user_input = input("陈文坚：")
    # 清空记忆
    if user_input == "/clear":

      messages = [
         {
            "role": "system",
            "content": system_prompt
         }
      ]

      with open("messages.json", "w", encoding="utf-8") as f:
          json.dump(messages, f, ensure_ascii=False, indent=4)

      print("记忆已清空")
      continue


#切换人格
    if user_input == "/interview":

      system_prompt = "你是一个严厉的互联网大厂面试官"

      messages = [
          {
            "role": "system",
            "content": system_prompt
          }
      ]

      print("已切换为面试官模式")
      continue


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
     # 限制聊天记录长度，保留系统提示和最近20条消息
    if len(messages) >21:
        messages=[messages[0]]+messages[-20:]

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse
import json
import os

load_dotenv()
app = FastAPI()

# DeepSeek客户端
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    raise ValueError("请设置环境变量 DEEPSEEK_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

#打开聊天记录文件
try:

    with open("messages.json", "r", encoding="utf-8") as f:

        messages = json.load(f)

except (FileNotFoundError, json.JSONDecodeError):

    messages = [
        {
            "role": "system",
            "content": "你是一个AI助手"
        }
    ]
# 打开网页
@app.get("/")
def home():
    with open("web_version/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

# 定义请求数据格式
class ChatRequest(BaseModel):
    message: str

# AI聊天接口
@app.post("/chat")
def chat(request: ChatRequest):
    # 用户输入添加到消息列表
    messages.append({
        "role": "user",
        "content": request.message
    })
    #保存聊天记录
    with open("messages.json", "w", encoding="utf-8") as f:

        json.dump(
            messages,
            f,
            ensure_ascii=False,
            indent=4
        )

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        stream=True
    )

    # 流式响应（核心为循环）
    def generate():

        ai_reply = ""

        for chunk in response:

            content = chunk.choices[0].delta.content

            if content is not None:

                ai_reply += content

                yield content

        messages.append({
            "role": "assistant",
            "content": ai_reply
        })

        #保存AI回复
        with open("messages.json", "w", encoding="utf-8") as f:
            json.dump(
                messages,
                f,
                ensure_ascii=False,
                indent=4
            )
# 返回流式响应
    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )
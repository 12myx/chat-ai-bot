from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
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

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": "你是一个AI助手"
            },
            {
                "role": "user",
                "content": request.message
            }
        ]
    )

    ai_reply = response.choices[0].message.content

    return {
        "reply": ai_reply
    }
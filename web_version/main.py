from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse
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
        ],
        #流式输出
        stream=True
    )
# 流式响应（核心为循环）
    def generate():

        for chunk in response:

            content = chunk.choices[0].delta.content

            if content:
                yield content

    return StreamingResponse(generate(), media_type="text/plain")
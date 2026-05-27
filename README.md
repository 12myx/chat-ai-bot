# Chat AI Bot 🤖

一个基于 DeepSeek API 的 AI 聊天应用，支持命令行和网页两种使用方式。

## 功能特性

- **双版本支持**：命令行版 + 网页版
- **流式输出**：AI 回复逐字显示，体验更流畅
- **多轮对话**：支持上下文记忆（保留最近20条）
- **人格切换**：支持切换为英语陪练、面试官等不同角色
- **聊天记录持久化**：自动保存对话到 JSON 文件
- **Markdown 渲染**：支持代码高亮和富文本格式
- **回车发送**：网页版支持按 Enter 键快速发送消息

## 项目结构

```
chat-ai-bot/
├── chat_version/
│   └── chat.py          # 命令行版聊天
├── web_version/
│   ├── main.py          # FastAPI 后端
│   └── index.html       # 前端页面
├── requirements.txt     # 依赖列表
└── .gitignore          # Git 忽略文件
```

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/12myx/chat-ai-bot.git
cd chat-ai-bot
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 API Key

创建 `.env` 文件，添加你的 DeepSeek API Key：

```env
DEEPSEEK_API_KEY=your_api_key_here
```

> 获取 API Key：[DeepSeek 开放平台](https://platform.deepseek.com/)

### 4. 运行

#### 命令行版

```bash
python chat_version/chat.py
```

**支持的命令：**
- 直接输入文字 → 与 AI 对话
- `/clear` → 清空聊天记录
- `/interview` → 切换为面试官模式
- `quit` → 退出程序

#### 网页版

```bash
cd web_version
uvicorn main:app --reload
```

然后打开浏览器访问：`http://localhost:8000`

**网页版特性：**
- 支持 Markdown 格式和代码高亮
- 多轮对话上下文记忆
- 聊天记录自动保存
- 按 Enter 快速发送

## 技术栈

- **后端**：FastAPI + OpenAI SDK
- **前端**：原生 HTML/CSS/JavaScript + Markdown 渲染库
- **AI 模型**：DeepSeek Chat

## 待改进项

- [x] 网页版添加多轮对话记忆 ✅
- [x] 支持 Markdown 渲染 ✅
- [x] 添加回车发送功能 ✅
- [ ] 网页版支持人格切换

## 更新日志

### 2025-05-25
- ✅ 网页版新增 Markdown 渲染和代码高亮
- ✅ 网页版支持多轮上下文对话
- ✅ 网页版聊天记录持久化
- ✅ 支持回车键发送消息

## 许可证

MIT License

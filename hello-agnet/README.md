# 🚀 hello-agnet

基于《Hello Agents》的 Agent 开发实战项目，按天推进，从基础 LLM 客户端封装到多 Agent 协作全栈应用。

## 📂 目录结构

```
hello-agnet/
├── .env                      # 环境变量（OPENAI_API_KEY / LLM_* / AMAP_MAPS_API_KEY 等）
├── .gitignore
├── README.md
├── day001/                   # Day 1：Agent 基础模式
│   ├── HelloAgentsLLM.py     #   LLM 客户端基类（流式调用）
│   ├── Reflection/           #   Reflection 反思模式：生成 → 评审 → 优化
│   ├── ReAct/                #   ReAct 推理+行动模式：Thought → Action → Observation
│   ├── PlanAndSolve/         #   先规划后执行：Planner → Executor
│   └── AutoGen/              #   AutoGen 多智能体对话框架
├── day002/                   # Day 2：Agent 框架与工具链
│   ├── AgentScope/           #   阿里 AgentScope 多 Agent 框架（含 phases 昼夜循环）
│   ├── CAMEL/                #   CAMEL 角色扮演对话框架
│   ├── ContextEngineering/   #   上下文工程（代码库维护助手）
│   ├── LangGraph/            #   LangGraph 图状态机 Agent
│   ├── Memory/               #   记忆机制实践
│   ├── helloAgent/           #   简易 Agent 封装
│   └── rag/                  #   RAG 检索增强生成（PDF 学习助手）
└── day003/                   # Day 3：多 Agent 全栈应用 —— tripAgent 旅行规划系统
    └── tripAgent/
        ├── baken/            #   FastAPI 后端
        │   ├── agent/        #     TripPlannerAgent + 4 个角色 Agent（景点/天气/酒店/规划）
        │   ├── Entity/       #     Pydantic 数据模型（TripPlan/DayPlan/Attraction...）
        │   ├── Service/      #     UnsplashService 图片搜索
        │   ├── api/          #     路由
        │   ├── controller/   #     FastAPI 入口（uvicorn 启动）
        │   ├── dto/          #     请求模型
        │   └── config.py     #     pydantic-settings 配置
        └── frontend/         #   Vue3 + Vite + ant-design-vue 前端
```

## 🧠 学习路线

| Day | 主题 | 产出 |
|-----|------|------|
| Day 1 | Agent 基础模式 | Reflection / ReAct / Plan & Solve 三种模式的代码实现 |
| Day 2 | 框架与工具链 | AgentScope、CAMEL、LangGraph、RAG、记忆机制 |
| Day 3 | 多 Agent 全栈实践 | tripAgent 旅行规划系统（4 Agent 协作 + 高德 MCP + FastAPI + Vue3） |

## ⚙️ 环境配置

复制 `.env.example` 为 `.env` 并填写密钥（`.env` 已被 gitignore，不会提交）：

```
# LLM（OpenAI 兼容接口）
OPENAI_API_KEY=sk-xxx
OPENAI_BASE_URL=https://api.openai.com/v1
MODEL_NAME=gpt-4o-mini

# day003 tripAgent 专用（也可复用上面的 LLM_* 变量）
LLM_MODEL_ID=your-model
LLM_API_KEY=sk-xxx
LLM_BASE_URL=https://api.openai.com/v1

# day003 外部服务
AMAP_MAPS_API_KEY=你的高德 Web 服务 Key     # 高德地图 MCP
UNSPLASH_ACCESS_KEY=你的 Unsplash Key      # 景点配图
```

> ⚠️ `load_dotenv()` 默认不覆盖已有环境变量，若 shell 中已存在同名变量需加 `override=True`。

## 🚀 运行

### day003 tripAgent（完整项目）

```bash
# 后端（项目根目录）
cd hello-agnet
python -m day003.tripAgent.baken.controller.main
# 或 uvicorn 直接启动
uvicorn day003.tripAgent.baken.controller.create_trip_plan:app --port 8000

# 前端
cd day003/tripAgent/frontend
npm install
npm run dev   # 默认 http://localhost:5173
```

### day001 / day002 示例

```bash
python -m day001.Reflection.ReflectionAgent
python -m day002.LangGraph.main
```

## 🛠️ 技术栈

- Python 3.x + venv
- `hello_agents` 库（HelloAgentsLLM / SimpleAgent / MCPTool）
- 高德地图 MCP（`@amap/amap-maps-mcp-server`）
- FastAPI + Pydantic v2
- Vue3 + Vite + TypeScript + ant-design-vue

## 📝 学习笔记

对应每日学习总结（Obsidian）：2026-08-07 / 2026-08-09 / 2026-08-10

---

Made by 小陈 🧑‍💻 — 记录每一天的 Agent 学习进度

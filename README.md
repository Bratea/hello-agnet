# AgentStudy — AI Agent 开发实战学习仓库

> 基于 **《Hello Agents》** 课程体系的 Agent 开发实战项目，从基础 LLM 客户端封装到多 Agent 协作全栈应用，**按天推进、逐步进阶**。

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white) ![Godot](https://img.shields.io/badge/Godot-4.x-478CBF?logo=godotengine&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-backend-009688?logo=fastapi&logoColor=white) ![Vue](https://img.shields.io/badge/Vue-3.x-42b883?logo=vuedotjs&logoColor=white)

---

## 📖 这是什么

一个 **AI Agent（智能体）从零到全栈实战**的学习仓库，包含两大模块：

| 模块 | 内容 | 定位 |
|------|------|------|
| `AgentGuide/` | LangChain / FastAPI 基础 | 前置地基，Agent 开发前的能力储备 |
| `hello-agnet/` | 《Hello Agents》三阶段实战 | 主线：封装 → 多 Agent → 全栈应用 |

学习路径：**AgentGuide 打底 → day001 封装 → day002 框架 → day003 综合实战**，每一步都有可运行的代码。

---

## 🗂️ 目录结构

```
AgentStudy/
├── AgentGuide/                    # 前置基础（day001 课程配套）
│   └── day001/
│       ├── LangChain/             # LangChain 基础：链、工具调用、模型封装
│       │   ├── quickStart.py      # 快速上手
│       │   └── toolTest/          # 工具调用实战（自定义工具 + 多工具路由）
│       └── fastApi/               # FastAPI 后端
│           ├── singleController/  # 单控制器示例
│           └── moreController/    # 多控制器 + 路由拆分 + Pydantic 模型
│
└── hello-agnet/                   # 《Hello Agents》主线实战
    ├── day001/                    # 🚀 从零封装 LLM 客户端
    │   ├── HelloAgentsLLM.py      # 自研 LLM 封装（OpenAI 协议）
    │   └── helloAgent/            # 最小可用 Agent
    │
    ├── day002/                    # 🤝 多 Agent 框架全家桶
    │   ├── AgentScope/            # 阿里多智能体框架：角色扮演游戏（昼夜双阶段）
    │   ├── CAMEL/                 # 角色扮演式双 Agent（assistant + user）
    │   ├── AutoGen/               # 微软 AutoGen 多 Agent 协作
    │   ├── LangGraph/             # LangChain 图工作流
    │   ├── ContextEngineering/    # 上下文工程：知识库构建 + 代码库维护助手
    │   ├── Memory/                # 记忆系统
    │   ├── rag/                   # 检索增强生成（RAG）
    │   ├── ReAct/                 # ReAct 推理-行动范式
    │   ├── Reflection/            # 自我反思范式
    │   ├── PlanAndSolve/          # 规划-求解范式
    │   └── helloAgent/            # 升级版 Agent
    │
    └── day003/                    # 🏗️ 综合实战（三个完整项目）
        ├── CyberTown/             # 🎮 AI NPC 小镇（Godot 3D 可视化）
        │   ├── baken/             #    FastAPI 后端：NPC Agent、好感度、对话
        │   └── fronted/           #    Godot 前端：3D 场景、NPC 互动、音效
        │
        ├── DeepResearchAssistant/ # 🔬 AI 深度研究助手
        │   ├── baken/             #    研究后端：检索、聚合、生成报告
        │   └── fronted/           #    Vue3 前端界面
        │
        └── tripAgent/             # ✈️ 多 Agent 旅行规划全栈应用
            └── frontend/          #    Vue3 + Ant Design Vue 前端
```

---

## 🚀 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+（day003 前端）
- Godot 4.x（CyberTown 前端，可选）

### 1. AgentGuide 基础

```bash
cd AgentGuide/day001/LangChain
pip install langchain langchain-openai
python quickStart.py
```

### 2. hello-agnet day001（LLM 封装）

```bash
cd hello-agnet/day001
# 配置环境变量（OPENAI_API_KEY 或兼容 API）
python HelloAgentsLLM.py
```

### 3. day002 多 Agent 框架

```bash
cd hello-agnet/day002/CAMEL
pip install -r requirements.txt
python main.py            # CAMEL 角色扮演双 Agent
```

### 4. day003 综合实战

```bash
# CyberTown — AI NPC 小镇
cd hello-agnet/day003/CyberTown/baken
pip install -r requirements.txt
python main.py            # 启动 FastAPI 后端
# 然后用 Godot 打开 fronted/ 运行 3D 前端

# DeepResearchAssistant — 深度研究助手
cd hello-agnet/day003/DeepResearchAssistant/baken
python main.py            # 研究后端
# 前端: cd fronted && npm install && npm run dev

# tripAgent — 旅行规划
cd hello-agnet/day003/tripAgent/frontend
npm install && npm run dev
```

---

## 🧠 学习路线详解

### 阶段 0：AgentGuide — 地基

- **LangChain**：理解 LLM 应用开发的基本抽象（模型、链、工具）。`toolTest/` 演示了自定义工具与模型路由，是理解"Agent 为什么需要工具"的关键。
- **FastAPI**：掌握异步后端与 API 设计（Pydantic 模型、路由拆分），为 day003 的完整应用打基础。

### 阶段 1：day001 — 自己动手封装 LLM

不依赖任何框架，手写 LLM 客户端封装（`HelloAgentsLLM.py`），理解：

- Chat Completions 协议与流式响应
- 消息历史管理
- 最小 Agent 循环（prompt → 模型 → 输出）

> 💡 自己封装一遍，比直接用框架更懂 Agent 的工作原理。

### 阶段 2：day002 — 主流多 Agent 框架

一天跑通 **6 种范式/框架**，横向对比它们的核心思想：

| 框架/范式 | 核心思想 | 亮点 |
| ----------- | --------- | ------ |
| **CAMEL** | 角色扮演：assistant 与 user 两个 Agent 互相对话完成任务 | 简单直观，入门首选 |
| **AgentScope** | 多智能体 + 角色/阶段/工具管理 | 内置昼夜双阶段游戏模拟，可玩性高 |
| **AutoGen** | 多 Agent 对话编排（微软） | 对话驱动任务分解 |
| **LangGraph** | 图结构工作流（节点 + 边） | 显式控制流程，适合生产 |
| **ReAct** | 推理 → 行动 → 观察 循环 | Agent 的经典决策范式 |
| **Reflection** | 生成 → 自我批判 → 改进 | 提升输出质量的关键技巧 |
| **PlanAndSolve** | 先规划再执行 | 复杂任务分解策略 |
| **ContextEngineering** | 上下文工程：知识库 + 代码库维护助手 | 让 Agent 用对信息 |
| **Memory / RAG** | 记忆系统与检索增强 | 长对话与领域知识接入 |

### 阶段 3：day003 — 综合实战（三个完整项目）

#### 🎮 CyberTown — AI NPC 小镇

FastAPI 后端 + Godot 3D 前端，构建一个可交互的赛博小镇：

- **NPC Agent**：每个 NPC 有独立人格 prompt（张三/李四/王五）、对话生成
- **关系系统**：好感度管理（`relationship_manager.py`）——你和 NPC 的关系会随对话变化
- **状态管理**：NPC 状态持久化（`state_manager.py`）
- **3D 交互**：Godot 场景、玩家移动、NPC 碰撞互动、环境音效

#### 🔬 DeepResearchAssistant — 深度研究助手

研究后端（`baken/`）+ Vue3 前端（`fronted/`），输入主题自动生成深度研究报告。

#### ✈️ tripAgent — 多 Agent 旅行规划应用

Vue3 + Ant Design Vue 全栈应用，多 Agent 协作完成旅行规划（路线、景点、预算）。

---

## 🛠️ 技术栈

| 层 | 技术 |
| ---- | ------ |
| 语言 | Python 3.10+、TypeScript、GDScript |
| LLM | OpenAI 协议兼容 API（OPENAI_API_KEY） |
| Agent 框架 | CAMEL、AgentScope、AutoGen、LangGraph、LangChain |
| 后端 | FastAPI、Pydantic |
| 前端 | Vue 3、Ant Design Vue、Godot 4 |
| 范式 | ReAct、Reflection、PlanAndSolve、RAG、Memory |

---

## 📌 说明

- 密钥文件（`.env`）、虚拟环境（`.venv/`、`AGenv/`）、依赖（`node_modules/`）与运行时数据均**不入库**，见根目录 `.gitignore`
- 各项目需要的 API Key 请自行配置环境变量
- 项目按学习进度持续更新中

---

## 📄 License

学习用途，代码仅供个人学习参考。

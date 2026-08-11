#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2026/8/8 16:08
# @Author  : 小陈
# @File    : fastTest.py
# @Software: PyCharm
"""
import os
from pathlib import Path

from dotenv import load_dotenv

# 显式加载项目根目录的 .env，避免从当前目录加载到空的 .env
# 不使用 override，让已经存在的环境变量优先（方便外部传入真实 Qdrant/Neo4j 配置）
ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")

# 修复 dashscope SDK 在 import 后才读取环境变量的问题：
# 必须在导入 hello_agents 的 memory 模块前设置 DASHSCOPE_API_KEY
embed_api_key = os.getenv("EMBED_API_KEY")
if embed_api_key:
    os.environ["DASHSCOPE_API_KEY"] = embed_api_key

from hello_agents import SimpleAgent, HelloAgentsLLM, ToolRegistry
from hello_agents.tools import MemoryTool

# 创建LLM实例
llm = HelloAgentsLLM(
    model=os.getenv("LLM_MODEL_ID"),
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL"),
    temperature=0.7
)

agent = SimpleAgent(name="记忆助手", llm=llm)

# 创建记忆工具：使用默认记忆类型（working + episodic + semantic）
# 依赖 .env 中配置的 Qdrant 和 Neo4j 服务
tool_registry = ToolRegistry()
memory_tool = MemoryTool(user_id="user123")
tool_registry.register_tool(memory_tool)
agent.tool_registry = tool_registry

# 体验记忆功能
print("=== 添加多个记忆 ===")

# 添加第一个记忆
result1 = memory_tool.run({
    "action": "add",
    "content": "用户张三是一名Python开发者，专注于机器学习和数据分析",
    "memory_type": "semantic",
    "importance": 0.8
})
print(f"记忆1: {result1}")

# 添加第二个记忆
result2 = memory_tool.run({
    "action": "add",
    "content": "李四是前端工程师，擅长React和Vue.js开发",
    "memory_type": "semantic",
    "importance": 0.7
})
print(f"记忆2: {result2}")

# 添加第三个记忆
result3 = memory_tool.run({
    "action": "add",
    "content": "王五是产品经理，负责用户体验设计和需求分析",
    "memory_type": "semantic",
    "importance": 0.6
})
print(f"记忆3: {result3}")

print("\n=== 搜索特定记忆 ===")
# 搜索前端相关的记忆
print("🔍 搜索 '前端工程师':")
result = memory_tool.run({
    "action": "search",
    "query": "前端工程师",
    "limit": 3
})
print(result)

print("\n=== 记忆摘要 ===")
result = memory_tool.run({"action": "summary"})
print(result)

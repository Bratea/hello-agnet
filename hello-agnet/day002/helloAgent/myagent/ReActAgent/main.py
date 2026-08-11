#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2026/8/8 14:34
# @Author  : 小陈
# @File    : main.py
# @Software: PyCharm
"""
import os
from dotenv import load_dotenv
from hello_agents import HelloAgentsLLM, ToolRegistry
from hello_agents.tools import CalculatorTool   # day002 已验证可用的工具
from my_react_agent import MyReActAgent

load_dotenv(override=True)

# 1. LLM
llm = HelloAgentsLLM(
    model=os.getenv("LLM_MODEL_ID"),
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL"),
    temperature=0.7
)

# 2. 工具注册表,注册工具
tool_registry = ToolRegistry()
tool_registry.register_tool(CalculatorTool())

# 3. 实例化 MyReActAgent
agent = MyReActAgent(
    name="ReAct助手",
    llm=llm,
    tool_registry=tool_registry,
    max_steps=5
)

# 4. 运行
answer = agent.run("帮我计算 (15 * 8 + 32) 是多少")
print(answer)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2026/8/11 15:43
# @Author  : 小陈
# @File    : quickStart.py
# @Software: PyCharm
"""
import os

# 安装
# pip install -U langchain

# pip install -qU "langchain[anthropic]" 调用模型 因为LangChain 本身不内置 大模型 的支持，它是一个插件体系：
"""
LLM API 协议说明：

目前主流大语言模型 API 主要分为几类：
1. OpenAI API 协议：目前应用最广的标准，许多模型供应商（如 DeepSeek、Qwen、Moonshot、Ollama 等）
   都提供 OpenAI Compatible 接口，可以通过统一的 Chat Completions 格式接入。
2. Anthropic Messages API：Claude 系列模型使用的原生协议，与 OpenAI 在消息结构、System Prompt
   等方面存在差异。
3. 其他厂商自定义协议：例如 Google Gemini API 等，有自己的请求和响应格式。

在实际开发中，通常通过 Provider Adapter（供应商适配层）统一不同协议：
将不同厂商的 API 格式转换为应用内部统一接口，从而实现灵活切换模型供应商。
"""

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv(override=True)   #override=True 代码当前的 .env会覆盖本机的 如果flase就默认拉取openai的本机key

def get_weather(city: str) -> str:
    """获取指定城市的天气"""
    return f"{city} 天气总是晴朗！"


# 改这里：用 OpenAI 的模型 原生
model = ChatOpenAI(
    model="gpt-4o-mini",  # 模型名
    api_key="sk-xxxxxxxxxxxx",  # 你的 OpenAI API Key
)

# 如果你用的是第三方（兼容 OpenAI 的）
model = ChatOpenAI(
    model=os.getenv("LLM_MODEL"),
    base_url=os.getenv("LLM_BASE_URL"),  # 第三方地址
    api_key=os.getenv("LLM_API_KEY"),
)

agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt="你是一个乐于助人的助手",
)

# 执行代理
result = agent.invoke(
    {"messages": [{"role": "user", "content": "旧金山天气如何？"}]}
)
print(result)
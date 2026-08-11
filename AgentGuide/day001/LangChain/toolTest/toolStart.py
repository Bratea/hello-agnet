#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2026/8/11 20:29
# @Author  : 小陈
# @File    : toolStart.py
# @Software: PyCharm
"""
import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from AgentGuide.day001.LangChain.toolTest.models.models import Context, ResponseFormat
from AgentGuide.day001.LangChain.toolTest.promote import SYSTEM_PROMPT
from AgentGuide.day001.LangChain.toolTest.tools.get_user_location import get_user_location, get_weather_for_location

load_dotenv(override=True)

model = ChatOpenAI(
    model=os.getenv("LLM_MODEL"),
    base_url=os.getenv("LLM_BASE_URL"),  # 第三方地址
    api_key=os.getenv("LLM_API_KEY"),
)

# 添加记忆 向代理添加记忆，以在多次交互中保持状态。这允许代理记住之前的对话和上下文。
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()

agent = create_agent(
    system_prompt=SYSTEM_PROMPT,
    model=model,
    tools=[get_user_location, get_weather_for_location],
    context_schema=Context,
    response_format=ResponseFormat,
    checkpointer=checkpointer
)

# `thread_id` 是给定对话的唯一标识符。
config = {"configurable": {"thread_id": "1"}}

response = agent.invoke(
    {"messages": [{"role": "user", "content": "我是小陈？"}]},
    config=config,
    context=Context(user_id="1")
)

print(response['structured_response'])

# 查看 thread "1" 里实际存的消息历史
checkpoint = checkpointer.get({"configurable": {"thread_id": "1"}})
for m in checkpoint["channel_values"]["messages"]:
    print(type(m).__name__, "|", getattr(m, "content", ""))

# 注意，我们可以使用相同的 `thread_id` 继续对话。
response = agent.invoke(
    {"messages": [{"role": "user", "content": "你好我是谁！"}]},
    config=config,
    context=Context(user_id="1")
)

print(response['structured_response'])


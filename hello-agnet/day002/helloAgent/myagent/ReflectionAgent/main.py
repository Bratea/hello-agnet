#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2026/8/8 14:44
# @Author  : 小陈
# @File    : main.py
# @Software: PyCharm
"""

import os

# test_reflection_agent.py
from dotenv import load_dotenv
from hello_agents import HelloAgentsLLM
from custom_prompts import DEFAULT_PROMPTS as code_prompts
from my_reflection_agent import MyReflectionAgent

load_dotenv(override=True)
llm = HelloAgentsLLM(
    model=os.getenv("LLM_MODEL_ID"),
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL"),
    temperature=0.7
)

# 使用默认通用提示词
general_agent = MyReflectionAgent(name="我的反思助手", llm=llm)

# 使用自定义代码生成提示词（类似第四章）

code_agent = MyReflectionAgent(
    name="我的代码生成助手",
    llm=llm,
    custom_prompts=code_prompts
)

# 测试使用
result = general_agent.run("写一篇关于人工智能发展历程的简短文章")
print(f"最终结果: {result}")

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2026/8/8 14:58
# @Author  : 小陈
# @File    : MyPlanAndSolveAgent.py
# @Software: PyCharm
"""

import os
from dotenv import load_dotenv
from hello_agents import HelloAgentsLLM
from my_plan_solve_agent import MyPlanAndSolveAgent
from custom_prompts import math_prompts

load_dotenv(override=True)

# 创建 LLM 实例
llm = HelloAgentsLLM(
    model=os.getenv("LLM_MODEL_ID"),
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL"),
    temperature=0.7
)

# 1. 使用默认提示词
agent = MyPlanAndSolveAgent(
    name="我的规划执行助手",
    llm=llm
)

question = "一个水果店周一卖出了15个苹果。周二卖出的苹果数量是周一的两倍。周三卖出的数量比周二少了5个。请问这三天总共卖出了多少个苹果？"
#
# result = agent.run(question)
# print(f"\n最终结果: {result}")
# print(f"对话历史: {len(agent.get_history())} 条消息")

# 2. 使用自定义数学提示词
math_agent = MyPlanAndSolveAgent(
    name="数学规划助手",
    llm=llm,
    custom_prompts=math_prompts
)

math_result = math_agent.run(question)

print(f"\n数学助手最终结果: {math_result}")

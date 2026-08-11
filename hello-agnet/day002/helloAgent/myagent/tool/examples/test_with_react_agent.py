#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试将 my_calculate 工具接入 MyReActAgent
"""

import os
import sys

# 把项目根目录加入 Python 路径，方便跨文件夹导入
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from dotenv import load_dotenv
from hello_agents import HelloAgentsLLM
from day002.helloAgent.myagent.ReActAgent.my_react_agent import MyReActAgent
from day002.helloAgent.myagent.tool.tools.my_calculate import create_calculator_registry

load_dotenv(override=True)

# 1. 创建 LLM
llm = HelloAgentsLLM(
    model=os.getenv("LLM_MODEL_ID"),
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL"),
    temperature=0.7
)

# 2. 创建工具注册表（包含自定义计算器）
tool_registry = create_calculator_registry()

# 3. 创建 ReAct Agent，传入工具
agent = MyReActAgent(
    name="计算器助手",
    llm=llm,
    tool_registry=tool_registry,
    max_steps=5
)

# 4. 提问
question = "帮我计算 (15 * 8 + 32) 是多少"
answer = agent.run(question)
print(f"\n最终答案: {answer}")

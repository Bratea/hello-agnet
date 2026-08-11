#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2026/8/8 09:58
# @Author  : 小陈
# @File    : RoundRobinGroupChat.py
# @Software: PyCharm
"""
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from day001.AutoGen.CodeReviewer import create_code_reviewer
from day001.AutoGen.Engineer import create_engineer
from day001.AutoGen.ProductManager import create_product_manager
from day001.AutoGen.UserProxy import create_user_proxy
from day001.AutoGen.create_openai_model_client import create_openai_model_client

# 创建模型客户端（调用你已有的函数）
model_client = create_openai_model_client()

# 定义团队聊天和协作规则
team_chat = RoundRobinGroupChat(
    participants=[
        create_product_manager(model_client),
        create_engineer(model_client),
        create_code_reviewer(model_client),
    ],
    termination_condition=TextMentionTermination("TERMINATE"),
    max_turns=20,
)
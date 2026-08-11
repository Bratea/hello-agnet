#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2026/8/8 10:40
# @Author  : 小陈
# @File    : RolePlaying.py
# @Software: PyCharm
"""

from colorama import Fore
from camel.societies import RolePlaying
from day002.CAMEL.taskPrompt import task_prompt
from day002.CAMEL.taskPrompt import model

# 初始化角色扮演会话
# AI 作家作为 "user"，负责提出写作结构和要求
# AI 心理学家作为 "assistant"，负责提供专业知识和内容
role_play_session = RolePlaying(
    assistant_role_name="心理学家",
    user_role_name="作家",
    task_prompt=task_prompt,
    model=model,
    with_task_specify=False, # 在本例中，我们直接使用给定的task_prompt
)

print(Fore.CYAN + f"具体任务描述:\n{role_play_session.task_prompt}\n")
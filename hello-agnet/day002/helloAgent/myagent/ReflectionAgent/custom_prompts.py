#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2026/8/8 14:44
# @Author  : 小陈
# @File    : custom_prompts.py
# @Software: PyCharm
"""

DEFAULT_PROMPTS = {
    "initial": "你是Python专家，请编写函数:{task}",
    "reflect": "请审查代码的算法效率:\n任务:{task}\n代码:{content}",
    "refine": "请根据反馈优化代码:\n任务:{task}\n上一轮代码:\n{last_attempt}\n反馈:{feedback}"
}

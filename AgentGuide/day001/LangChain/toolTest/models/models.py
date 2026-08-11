#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2026/8/11 20:51
# @Author  : 小陈
# @File    : models.py
# @Software: PyCharm
"""

from dataclasses import dataclass

@dataclass
class Context:
    """自定义运行时上下文模式。"""
    user_id: str

# 这里使用 dataclass，但也支持 Pydantic 模型。
@dataclass
class ResponseFormat:
    """代理的响应模式。"""
    # 带双关语的回应（始终必需）
    punny_response: str
    # 天气的任何有趣信息（如果有）
    weather_conditions: str | None = None
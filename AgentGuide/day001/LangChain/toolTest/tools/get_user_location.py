#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2026/8/11 20:49
# @Author  : 小陈
# @File    : get_user_location.py
# @Software: PyCharm
"""

from langchain.tools import tool, ToolRuntime

from AgentGuide.day001.LangChain.toolTest.models.models import Context


# 自定义工具
@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """根据用户 ID 获取用户信息。"""
    user_id = runtime.context.user_id
    return "Florida" if user_id == "1" else "SF"

@tool
def get_weather_for_location(city: str) -> str:
    """获取指定城市的天气。"""
    return f"{city}总是阳光明媚！"


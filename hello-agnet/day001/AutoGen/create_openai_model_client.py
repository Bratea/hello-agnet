#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2026/8/8 09:33
# @Author  : 小陈
# @File    : create_openai_model_client.py
# @Software: PyCharm
"""
import os

from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv(override=True)

def create_openai_model_client():
    """创建并配置 OpenAI 模型客户端"""
    return OpenAIChatCompletionClient(
        model= os.getenv("LLM_MODEL_ID"),
        api_key=os.getenv("LLM_API_KEY"),
        base_url=os.getenv("LLM_BASE_URL"),
        model_info={
            "vision": False,  # 是否支持图像
            "function_calling": True,  # 是否支持工具调用
            "json_output": False,  # 是否支持 JSON 输出
            "family": "openai",  # 模型家族，按你实际填
            "structured_output": False,
        },
    )

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2026/8/8 15:12
# @Author  : 小陈
# @File    : main.py
# @Software: PyCharm
"""
# test_my_calculator.py
import os
import sys

# 把 tool 目录加入 Python 路径，方便导入 tools 包
_tool_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _tool_dir not in sys.path:
    sys.path.insert(0, _tool_dir)

from dotenv import load_dotenv
from tools.my_calculate import create_calculator_registry

# 加载环境变量
load_dotenv(override=True)


def test_calculator_tool():
    """测试自定义计算器工具"""

    # 创建包含计算器的注册表
    registry = create_calculator_registry()

    print("🧪 测试自定义计算器工具\n")

    # 简单测试用例
    test_cases = [
        "2 + 3",  # 基本加法
        "10 - 4",  # 基本减法
        "5 * 6",  # 基本乘法
        "15 / 3",  # 基本除法
        "sqrt(16)",  # 平方根
    ]

    for i, expression in enumerate(test_cases, 1):
        print(f"测试 {i}: {expression}")
        result = registry.execute_tool("my_calculator", expression)
        print(f"结果: {result}\n")


def test_with_simple_agent():
    """测试与SimpleAgent的集成"""
    from hello_agents import HelloAgentsLLM

    # 创建LLM客户端
    llm = HelloAgentsLLM(
        model=os.getenv("LLM_MODEL_ID"),
        api_key=os.getenv("LLM_API_KEY"),
        base_url=os.getenv("LLM_BASE_URL"),
        temperature=0.7
    )

    # 创建包含计算器的注册表
    registry = create_calculator_registry()

    print("🤖 与SimpleAgent集成测试:")

    # 模拟SimpleAgent使用工具的场景
    user_question = "请帮我计算 sqrt(16) + 2 * 3"

    print(f"用户问题: {user_question}")

    # 使用工具计算
    calc_result = registry.execute_tool("my_calculator", "sqrt(16) + 2 * 3")
    print(f"计算结果: {calc_result}")

    # 构建最终回答
    final_messages = [
        {"role": "user", "content": f"计算结果是 {calc_result}，请用自然语言回答用户的问题:{user_question}"}
    ]

    print("\n🎯 SimpleAgent的回答:")
    response = llm.think(final_messages)
    for chunk in response:
        print(chunk, end="", flush=True)
    print("\n")


if __name__ == "__main__":
    test_calculator_tool()
    test_with_simple_agent()

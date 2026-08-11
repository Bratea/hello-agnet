#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2026/8/8 10:55
# @Author  : 小陈
# @File    : main.py
# @Software: PyCharm
"""

from langchain_core.messages import HumanMessage

from day002.LangGraph.createSearchAssistant import create_search_assistant


def main():
    app = create_search_assistant()

    # 配置线程 ID（用于 memory checkpointer）
    config = {"configurable": {"thread_id": "user-1"}}

    # 用户问题
    query = "2025 年 AI 大模型领域有哪些重要进展？"

    # 运行工作流
    result = app.invoke(
        {"messages": [HumanMessage(content=query)]},
        config=config,
    )

    # 打印最终回答
    print("\n最终回答：")
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
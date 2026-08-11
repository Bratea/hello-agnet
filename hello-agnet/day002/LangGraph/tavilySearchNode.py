#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2026/8/8 10:53
# @Author  : 小陈
# @File    : tavilySearchNode.py
# @Software: PyCharm
"""
from langchain_core.messages import AIMessage

from day002.LangGraph.Client import tavily_client
from day002.LangGraph.SearchState import SearchState


def tavily_search_node(state: SearchState) -> dict:
    """步骤2：使用Tavily API进行真实搜索"""
    search_query = state["search_query"]
    try:
        print(f"🔍 正在搜索: {search_query}")
        response = tavily_client.search(
            query=search_query, search_depth="basic", max_results=5, include_answer=True
        )

        # 格式化搜索结果为字符串
        lines = []
        if response.get("answer"):
            lines.append(f"Tavily 简明答案：{response['answer']}\n")

        for idx, result in enumerate(response.get("results", []), start=1):
            title = result.get("title", "无标题")
            url = result.get("url", "")
            content = result.get("content", "")
            lines.append(f"[{idx}] {title}\nURL: {url}\n内容：{content}\n")

        search_results = "\n".join(lines) if lines else "未找到有效搜索结果。"

        return {
            "search_results": search_results,
            "step": "searched",
            "messages": [AIMessage(content="✅ 搜索完成！正在整理答案...")]
        }
    except Exception as e:
        return {
            "search_results": f"搜索失败：{e}",
            "step": "search_failed",
            "messages": [AIMessage(content="❌ 搜索遇到问题...")]
        }

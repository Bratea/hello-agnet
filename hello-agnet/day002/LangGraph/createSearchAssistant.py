#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2026/8/8 10:54
# @Author  : 小陈
# @File    : createSearchAssistant.py
# @Software: PyCharm
"""

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

from day002.LangGraph.SearchState import SearchState
from day002.LangGraph.generateAnswerNode import generate_answer_node
from day002.LangGraph.tavilySearchNode import tavily_search_node
from day002.LangGraph.understandQueryNode import understand_query_node


def create_search_assistant():
    workflow = StateGraph(SearchState)

    # 添加节点
    workflow.add_node("understand", understand_query_node)
    workflow.add_node("search", tavily_search_node)
    workflow.add_node("answer", generate_answer_node)

    # 设置线性流程
    workflow.add_edge(START, "understand")
    workflow.add_edge("understand", "search")
    workflow.add_edge("search", "answer")
    workflow.add_edge("answer", END)

    # 编译图
    memory = InMemorySaver()
    app = workflow.compile(checkpointer=memory)
    return app

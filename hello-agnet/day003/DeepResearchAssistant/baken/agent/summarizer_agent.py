#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
总结 Agent — 对每个子任务的搜索结果进行总结
"""
from typing import List, Callable, Optional, Tuple

from hello_agents import HelloAgentsLLM

from agent.base import ToolAwareSimpleAgent
from agent.prompts.summarizing import task_summarizer_instructions
from model.entity.todo_item import TodoItem


class SummarizerAgent:
    """总结 Agent — 对每个子任务的搜索结果进行总结"""

    def __init__(
        self,
        llm: HelloAgentsLLM,
        tool_call_listener: Optional[Callable] = None
    ):
        self._llm = llm
        self._agent = ToolAwareSimpleAgent(
            name="Task Summarizer",
            system_prompt="你是一个任务总结专家，擅长从搜索结果中提取关键信息。",
            llm=llm,
            tool_call_listener=tool_call_listener
        )

    def summarize_task(
        self,
        task: TodoItem,
        search_results: List[dict]
    ) -> Tuple[str, List[str]]:
        """总结任务"""
        formatted_sources = self._format_sources(search_results)

        prompt = task_summarizer_instructions.format(
            task_title=task.title,
            task_intent=task.intent,
            task_query=task.query,
            search_results=formatted_sources,
        )

        summary = self._agent.run(prompt)
        source_urls = [r["url"] for r in search_results if r.get("url")]

        return summary, source_urls

    def _format_sources(self, search_results: List[dict]) -> str:
        """格式化搜索结果"""
        parts = []
        for idx, result in enumerate(search_results, start=1):
            title = result.get("title", "无标题")
            snippet = result.get("snippet", "")
            url = result.get("url", "")
            parts.append(
                f"[{idx}] {title}\n"
                f"    来源：{url}\n"
                f"    摘要：{snippet}\n"
            )
        return "\n".join(parts)
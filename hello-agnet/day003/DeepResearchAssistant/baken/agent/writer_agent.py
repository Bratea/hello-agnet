#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
报告 Agent — 整合所有子任务总结，生成最终报告
"""
from typing import List, Callable, Optional, Tuple

from hello_agents import HelloAgentsLLM

from agent.base import ToolAwareSimpleAgent
from agent.prompts.reporting import report_writer_instructions
from model.entity.todo_item import TodoItem


class WriterAgent:
    """报告 Agent — 整合所有子任务总结，生成最终报告"""

    def __init__(
        self,
        llm: HelloAgentsLLM,
        tool_call_listener: Optional[Callable] = None
    ):
        self._llm = llm
        self._agent = ToolAwareSimpleAgent(
            name="Report Writer",
            system_prompt="你是一个报告撰写专家，擅长整合信息并生成结构化的报告。",
            llm=llm,
            tool_call_listener=tool_call_listener
        )

    def generate_report(
        self,
        research_topic: str,
        task_summaries: List[Tuple[TodoItem, str, List[str]]]
    ) -> str:
        """生成最终报告"""
        formatted_summaries = self._format_summaries(task_summaries)

        prompt = report_writer_instructions.format(
            research_topic=research_topic,
            task_summaries=formatted_summaries,
        )

        return self._agent.run(prompt)

    def _format_summaries(
        self,
        task_summaries: List[Tuple[TodoItem, str, List[str]]]
    ) -> str:
        """格式化子任务总结"""
        formatted = []
        for idx, (task, summary, source_urls) in enumerate(task_summaries, start=1):
            formatted.append(
                f"## 任务{idx}：{task.title}\n\n"
                f"**意图**：{task.intent}\n\n"
                f"{summary}\n\n"
                f"**来源**：\n"
            )
            for url in source_urls:
                formatted.append(f"- {url}\n")
            formatted.append("\n")
        return "".join(formatted)
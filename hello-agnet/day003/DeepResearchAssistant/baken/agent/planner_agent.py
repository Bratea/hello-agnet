#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
规划 Agent — 将研究主题分解为子任务
"""
import re
import json
from typing import List, Callable, Optional
from datetime import datetime

from hello_agents import HelloAgentsLLM

from agent.base import ToolAwareSimpleAgent
from agent.prompts.planning import todo_planner_instructions
from model.entity.todo_item import TodoItem
from model.entity.summary_state import SummaryState


class PlannerAgent:
    """规划 Agent — 将研究主题分解为子任务"""

    def __init__(
        self,
        llm: HelloAgentsLLM,
        tool_call_listener: Optional[Callable] = None
    ):
        self._llm = llm
        self._agent = ToolAwareSimpleAgent(
            name="TODO Planner",
            system_prompt="你是一个研究规划专家，擅长将复杂的研究主题分解为清晰的子任务。",
            llm=llm,
            tool_call_listener=tool_call_listener
        )

    def plan_todo_list(self, state: SummaryState) -> List[TodoItem]:
        """规划 TODO 列表"""
        prompt = todo_planner_instructions.format(
            current_date=self._get_current_date(),
            research_topic=state.research_topic,
        )

        response = self._agent.run(prompt)
        tasks_payload = self._extract_tasks(response)

        todo_items = []
        for idx, item in enumerate(tasks_payload, start=1):
            if not all(key in item for key in ["title", "intent", "query"]):
                raise ValueError(f"任务{idx}缺少必需字段 (title, intent, query)")
            todo_items.append(TodoItem(
                id=idx,
                title=item["title"],
                intent=item["intent"],
                query=item["query"],
            ))

        return todo_items

    def _get_current_date(self) -> str:
        return datetime.now().strftime("%Y年%m月%d日")

    def _extract_tasks(self, response: str) -> List[dict]:
        """从 Agent 响应中提取 JSON 列表"""
        json_match = re.search(r'\[.*\]', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError as e:
                raise ValueError(f"JSON解析失败：{e}")
        raise ValueError("无法从响应中提取JSON")
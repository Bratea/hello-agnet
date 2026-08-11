#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
深度研究智能体主控
"""
import os
from typing import List, Tuple, Callable

from hello_agents import HelloAgentsLLM

from config import Configuration
from model.entity.todo_item import TodoItem
from model.entity.summary_state import SummaryState
from agent.planner_agent import PlannerAgent
from tools.search_client import SearchClient
from agent.summarizer_agent import SummarizerAgent
from agent.writer_agent import WriterAgent
from tools.notes_client import NotesClient


class DeepResearchAgent:
    """深度研究智能体

    协调三个子 Agent 完成研究：
    1. TODO Planner → 规划子任务
    2. Task Summarizer → 搜索并总结
    3. Report Writer → 生成最终报告
    """

    def __init__(self, config: Configuration):
        self.config = config
        self.llm = HelloAgentsLLM(
            model=os.getenv("LLM_MODEL_ID"),
            api_key=os.getenv("LLM_API_KEY"),
            base_url=os.getenv("LLM_BASE_URL"),
        )

        self._event_handlers: List[Callable] = []

        # 工具调用监听器
        def tool_listener(call_info):
            self._emit_event({
                "type": "tool_call",
                "agent": call_info["agent_name"],
                "tool": call_info["tool_name"],
                "parameters": call_info["parameters"],
            })

        # 创建服务
        self.search_service = SearchClient(config)
        self.planner = PlannerAgent(self.llm, tool_listener)
        self.summarizer = SummarizerAgent(self.llm, tool_listener)
        self.reporter = WriterAgent(self.llm, tool_listener)
        self.notes_service = NotesClient(workspace="./research_notes")

    # ---- 事件系统 ----

    def on_event(self, handler: Callable):
        """注册事件处理器"""
        self._event_handlers.append(handler)

    def _emit_event(self, event: dict):
        """发射事件"""
        for handler in self._event_handlers:
            try:
                handler(event)
            except Exception as e:
                print(f"[DeepResearchAgent] 事件处理器异常：{e}")

    # ---- 主流程 ----

    def run(self, research_topic: str) -> str:
        """执行完整研究流程

        Args:
            research_topic: 研究主题

        Returns:
            Markdown 格式的研究报告
        """
        state = SummaryState(research_topic=research_topic)

        # 1. 规划阶段
        self._emit_event({
            "type": "progress",
            "stage": "planning",
            "percentage": 5,
            "text": "正在规划研究任务..."
        })
        todo_list = self.planner.plan_todo_list(state)
        state.todo_items = todo_list
        self._emit_event({
            "type": "plan",
            "data": [item.dict() for item in todo_list]
        })

        # 2. 执行阶段
        self._emit_event({
            "type": "progress",
            "stage": "executing",
            "percentage": 10,
            "text": f"开始执行 {len(todo_list)} 个研究任务..."
        })
        task_summaries: List[Tuple[TodoItem, str, List[str]]] = []
        for idx, task in enumerate(todo_list, start=1):
            percentage = 10 + (idx / len(todo_list)) * 70
            self._emit_event({
                "type": "progress",
                "stage": "executing",
                "percentage": percentage,
                "text": f"正在研究任务 {idx}/{len(todo_list)}：{task.title}"
            })

            # 搜索
            search_results = self.search_service.search(task.query)

            # 总结
            summary, source_urls = self.summarizer.summarize_task(task, search_results)
            task_summaries.append((task, summary, source_urls))

            # 保存笔记
            self.notes_service.save_task_summary(task, search_results, summary)

            self._emit_event({
                "type": "task_summary",
                "task_id": task.id,
                "summary": summary
            })

        # 3. 报告阶段
        self._emit_event({
            "type": "progress",
            "stage": "reporting",
            "percentage": 90,
            "text": "正在生成最终报告..."
        })
        report = self.reporter.generate_report(research_topic, task_summaries)

        self._emit_event({
            "type": "progress",
            "stage": "completed",
            "percentage": 100,
            "text": "研究完成！"
        })
        self._emit_event({
            "type": "report",
            "data": report
        })

        return report
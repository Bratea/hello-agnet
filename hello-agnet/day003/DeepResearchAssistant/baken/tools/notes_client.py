#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
笔记持久化客户端
"""
from typing import List

from hello_agents.tools import NoteTool

from model.entity.todo_item import TodoItem


class NotesClient:
    """笔记服务 — 将研究进度和结果持久化到本地笔记"""

    def __init__(self, workspace: str):
        self.note_tool = NoteTool(workspace=workspace)

    def save_task_summary(
            self,
            task: TodoItem,
            search_results: List[dict],
            summary: str
    ):
        """保存任务总结"""
        content = self._format_note_content(task, search_results, summary)
        self.note_tool.run({
            "action": "create",
            "title": f"任务{task.id}：{task.title}",
            "content": content,
            "tags": ["research", "summary"]
        })

    def _format_note_content(
            self,
            task: TodoItem,
            search_results: List[dict],
            summary: str
    ) -> str:
        """格式化笔记内容"""
        parts = [f"# 任务{task.id}：{task.title}\n\n"]
        parts.append("## 任务信息\n\n")
        parts.append(f"- **意图**：{task.intent}\n")
        parts.append(f"- **查询**：{task.query}\n\n")

        parts.append("## 搜索结果\n\n")
        for idx, result in enumerate(search_results, start=1):
            parts.append(f"[{idx}] {result.get('title', '')}\n")
            parts.append(f"URL: {result.get('url', '')}\n")
            parts.append(f"摘要: {result.get('snippet', '')}\n\n")

        parts.append(f"## 总结\n\n{summary}\n")
        return "".join(parts)
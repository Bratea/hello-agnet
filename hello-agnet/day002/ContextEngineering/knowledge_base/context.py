#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
上下文工程模块（兼容 hello-agents 0.2.0 的本地实现）

由于安装的 hello-agents==0.2.0 没有提供 hello_agents.context 子模块，
但 knowledge_base/ 下的演示脚本依赖 ContextBuilder 与 ContextConfig，
故在本模块提供最小可用实现。
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Optional


@dataclass
class ContextConfig:
    """上下文构建配置"""

    max_tokens: int = 4000
    reserve_ratio: float = 0.2
    min_relevance: float = 0.2
    enable_compression: bool = True


class ContextBuilder:
    """上下文构建器

    基于记忆工具与 RAG 工具，为用户查询组装一个包含系统指令、
    相关记忆、知识库参考和对话历史的上下文字符串。
    """

    def __init__(
        self,
        memory_tool: Any = None,
        rag_tool: Any = None,
        config: Optional[ContextConfig] = None,
    ):
        self.memory_tool = memory_tool
        self.rag_tool = rag_tool
        self.config = config or ContextConfig()

    def build(
        self,
        user_query: str,
        conversation_history: Optional[List[Any]] = None,
        system_instructions: Optional[str] = None,
    ) -> str:
        """构建上下文字符串"""
        conversation_history = conversation_history or []

        # 1. 收集：检索相关记忆与 RAG 内容
        memory_context = self._retrieve_memories(user_query)
        rag_context = self._retrieve_rag(user_query)

        # 2. 结构化组装
        parts = []
        if system_instructions:
            parts.append(f"【系统指令】\n{system_instructions}")

        if memory_context:
            parts.append(f"【相关记忆】\n{memory_context}")

        if rag_context:
            parts.append(f"【知识库参考】\n{rag_context}")

        # 对话历史
        history_lines = []
        for msg in conversation_history:
            if hasattr(msg, "role") and hasattr(msg, "content"):
                history_lines.append(f"[{msg.role}] {msg.content}")
            elif isinstance(msg, dict):
                history_lines.append(
                    f"[{msg.get('role', 'unknown')}] {msg.get('content', '')}"
                )
            elif isinstance(msg, (list, tuple)) and len(msg) >= 2:
                history_lines.append(f"[{msg[0]}] {msg[1]}")
            else:
                history_lines.append(str(msg))

        if history_lines:
            parts.append("【对话历史】\n" + "\n".join(history_lines))

        parts.append(f"【当前问题】\n{user_query}")

        context = "\n\n".join(parts)

        # 3. 截断：中文字符较多，按每 token ≈ 1.5 个字符估算
        available_ratio = max(0.1, 1.0 - self.config.reserve_ratio)
        max_chars = int(self.config.max_tokens * available_ratio * 1.5)
        if len(context) > max_chars:
            context = context[: max_chars - 20] + "\n...[上下文已截断]"

        return context

    def _retrieve_memories(self, query: str) -> str:
        if self.memory_tool is None:
            return ""
        try:
            result = self.memory_tool.run(
                {"action": "search", "query": query, "limit": 5}
            )
            return str(result) if result else ""
        except Exception as e:
            return f"(记忆检索失败: {e})"

    def _retrieve_rag(self, query: str) -> str:
        if self.rag_tool is None:
            return ""
        try:
            if hasattr(self.rag_tool, "get_relevant_context"):
                return self.rag_tool.get_relevant_context(
                    query=query, limit=5, max_chars=1200
                )
            result = self.rag_tool.run(
                {"action": "search", "query": query, "limit": 5}
            )
            return str(result) if result else ""
        except Exception as e:
            return f"(知识库检索失败: {e})"

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
扩展 SimpleAgent，支持工具调用监听
"""
from typing import Optional, Callable

from hello_agents import SimpleAgent, HelloAgentsLLM, ToolRegistry


class ToolAwareSimpleAgent(SimpleAgent):
    """具有工具调用监听能力的 Agent

    在每次工具调用后通知监听器，用于实时进度展示和调试
    """

    def __init__(
            self,
            name: str,
            system_prompt: str,
            llm: HelloAgentsLLM,
            tool_registry: Optional[ToolRegistry] = None,
            tool_call_listener: Optional[Callable] = None,
    ):
        super().__init__(
            name=name,
            system_prompt=system_prompt,
            llm=llm,
            tool_registry=tool_registry,
        )
        self._tool_call_listener = tool_call_listener

    def _execute_tool_call(self, tool_name: str, parameters: str) -> str:
        """执行工具调用，并通知监听器"""
        result = super()._execute_tool_call(tool_name, parameters)

        if self._tool_call_listener:
            self._tool_call_listener({
                "agent_name": self.name,
                "tool_name": tool_name,
                "parameters": parameters,
                "result": result,
            })

        return result
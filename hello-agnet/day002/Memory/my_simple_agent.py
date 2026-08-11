#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
自定义 SimpleAgent，扩展工具调用解析器，支持 XML 标签格式。
"""

import re
from typing import Optional
from hello_agents import SimpleAgent, HelloAgentsLLM, Config
from hello_agents.tools.registry import ToolRegistry


class MySimpleAgent(SimpleAgent):
    """
    自定义 SimpleAgent，兼容 [TOOL_CALL:...] 和 <TOOL_CALL:...> 两种工具调用格式。
    """

    def __init__(
        self,
        name: str,
        llm: HelloAgentsLLM,
        system_prompt: Optional[str] = None,
        config: Optional[Config] = None,
        tool_registry: Optional[ToolRegistry] = None,
        enable_tool_calling: bool = True
    ):
        super().__init__(
            name=name,
            llm=llm,
            system_prompt=system_prompt,
            config=config,
            tool_registry=tool_registry,
            enable_tool_calling=enable_tool_calling
        )

    def _parse_tool_calls(self, text: str) -> list:
        """解析文本中的工具调用，支持方括号和 XML 两种格式"""
        tool_calls = []

        # 1. 方括号格式：[TOOL_CALL:tool_name:parameters]
        bracket_pattern = r'\[(?:TOOL_CALL|tool_call):([^:\]]+):([^\]]+)\]'
        for match in re.finditer(bracket_pattern, text, re.IGNORECASE):
            tool_calls.append({
                'tool_name': match.group(1).strip(),
                'parameters': match.group(2).strip(),
                'original': match.group(0)
            })

        # 2. XML 标签格式：<TOOL_CALL:tool_name:parameters />
        xml_pattern = r'<(?:TOOL_CALL|tool_call):([^:>]+):([^>]+)>'
        for match in re.finditer(xml_pattern, text, re.IGNORECASE):
            tool_calls.append({
                'tool_name': match.group(1).strip(),
                'parameters': match.group(2).strip(),
                'original': match.group(0)
            })

        return tool_calls

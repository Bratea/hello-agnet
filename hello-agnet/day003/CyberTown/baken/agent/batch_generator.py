#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
批量对话生成器 — 批量生成 NPC 背景对话（降低成本）
"""
import json
import re
from typing import Optional
from datetime import datetime

from hello_agents import HelloAgentsLLM

from agent.npc_agent import NPCAgentManager


class NPCBatchGenerator:
    """批量生成 NPC 对话的生成器"""

    def __init__(self, agent_manager: NPCAgentManager):
        self.llm = HelloAgentsLLM()
        self.agent_manager = agent_manager

    def generate_batch_dialogues(self, context: Optional[str] = None) -> dict[str, str]:
        """批量生成所有 NPC 的背景对话"""
        if context is None:
            context = self._get_current_context()

        npc_descriptions = []
        for npc_id, cfg in self.agent_manager.npc_configs.items():
            desc = (f"- {cfg['name']}({cfg['role']}): "
                    f"性格{cfg['personality']}")
            npc_descriptions.append(desc)

        npc_desc_text = "\n".join(npc_descriptions)

        prompt = f"""请为Datawhale办公室的3个NPC生成当前的对话或行为描述。

【场景】{context}

【NPC信息】
{npc_desc_text}

【生成要求】
1. 每个NPC生成1句话(20-40字)
2. 内容要符合角色设定、当前活动和场景氛围
3. 可以是自言自语、工作状态描述、或简单的思考
4. 要自然真实，像真实的办公室同事
5. **必须严格按照JSON格式返回**

【输出格式】(严格遵守)
{{"zhang_san": "...", "li_si": "...", "wang_wu": "..."}}

【示例输出】
{{"zhang_san": "这个bug真是见鬼了，已经调试两小时了...", "li_si": "嗯，这个功能的优先级需要重新评估一下。", "wang_wu": "这杯咖啡的拉花真不错，灵感来了!"}}

请生成(只返回JSON，不要其他内容):
"""
        response = self.llm.invoke([
            {"role": "system", "content": "你是一个游戏NPC对话生成器，擅长创作自然真实的办公室对话。"},
            {"role": "user", "content": prompt},
        ])

        text = "".join(response) if hasattr(response, "__iter__") and not isinstance(response, str) else str(response)
        dialogues = self._extract_json(text)
        if dialogues is None:
            return {npc_id: "..." for npc_id in self.agent_manager.npc_configs}
        return dialogues

    @staticmethod
    def _get_current_context() -> str:
        """根据当前时间推断场景"""
        hour = datetime.now().hour
        if hour < 9:
            return "早晨，同事们陆续来到办公室"
        elif hour < 12:
            return "上午工作时间"
        elif hour < 14:
            return "午餐时间"
        elif hour < 18:
            return "下午工作时间"
        else:
            return "下班时间，有些同事还在加班"

    @staticmethod
    def _extract_json(text: str) -> Optional[dict]:
        """从文本中提取 JSON"""
        try:
            return json.loads(text)
        except (json.JSONDecodeError, TypeError):
            pass
        fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
        if fenced:
            try:
                return json.loads(fenced.group(1))
            except json.JSONDecodeError:
                pass
        start, end = text.find("{"), text.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(text[start:end + 1])
            except json.JSONDecodeError:
                pass
        return None
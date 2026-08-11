#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
好感度管理器 — 管理 NPC 与玩家的好感度
"""
import json
from typing import Optional

from hello_agents import HelloAgentsLLM

from config import get_settings
from model.dto.affinity import AffinityInfo


class RelationshipManager:
    """好感度管理器"""

    def __init__(self, llm: Optional[HelloAgentsLLM] = None):
        self.affinity_data: dict[str, AffinityInfo] = {}
        self.llm = llm or HelloAgentsLLM()

    def get_affinity(self, npc_id: str, player_name: str) -> AffinityInfo:
        """获取好感度"""
        key = f"{npc_id}_{player_name}"
        if key not in self.affinity_data:
            self.affinity_data[key] = AffinityInfo()
        return self.affinity_data[key]

    def update_affinity(self, npc_id: str, player_name: str,
                        player_message: str, npc_reply: str) -> AffinityInfo:
        """更新好感度"""
        key = f"{npc_id}_{player_name}"
        affinity = self.get_affinity(npc_id, player_name)

        score_change = self._analyze_sentiment(player_message, npc_reply)
        new_score = max(0, min(100, affinity.score + score_change))

        affinity.score = new_score
        affinity.level = self._get_affinity_level(new_score)
        affinity.interaction_count += 1

        self.affinity_data[key] = affinity
        return affinity

    def _analyze_sentiment(self, player_message: str, npc_reply: str) -> int:
        """分析对话情感，返回好感度变化值"""
        prompt = f"""分析以下对话中玩家的态度:
玩家: {player_message}
NPC: {npc_reply}

请判断玩家的态度是:
1. 友好(+5分)
2. 中立(+2分)
3. 不友好(-3分)

只返回分数数字(5、2或-3)，不要其他内容。"""
        try:
            response = self.llm.invoke([{"role": "user", "content": prompt}])
            text = response.strip()
            # 尝试直接解析分数
            score_change = int(text)
            if score_change in (5, 2, -3):
                return score_change
            # 如果返回的是选项编号 1/2/3，映射到分数
            mapping = {"1": 5, "2": 2, "3": -3}
            return mapping.get(text.strip(), 2)
        except (ValueError, AttributeError, Exception):
            return 2

    @staticmethod
    def _get_affinity_level(score: float) -> str:
        """根据分数获取好感度等级"""
        if score <= 20:
            return "陌生"
        elif score <= 40:
            return "熟悉"
        elif score <= 60:
            return "友好"
        elif score <= 80:
            return "亲密"
        else:
            return "挚友"
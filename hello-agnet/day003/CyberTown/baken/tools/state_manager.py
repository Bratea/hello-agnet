#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
NPC 状态管理器 — 跟踪每个 NPC 的当前状态
"""
from typing import Optional
from datetime import datetime

from model.entity.npc_state import NPCState, NPCPosition


class StateManager:
    """NPC 状态管理器"""

    def __init__(self):
        self.npc_states: dict[str, NPCState] = {}

    def initialize_npcs(self):
        """初始化 NPC 状态"""
        npcs = [
            {
                "npc_id": "zhang_san",
                "name": "张三",
                "role": "Python工程师",
                "position": {"x": 300, "y": 200},
            },
            {
                "npc_id": "li_si",
                "name": "李四",
                "role": "产品经理",
                "position": {"x": 500, "y": 200},
            },
            {
                "npc_id": "wang_wu",
                "name": "王五",
                "role": "UI设计师",
                "position": {"x": 700, "y": 200},
            },
        ]
        for npc in npcs:
            self.npc_states[npc["npc_id"]] = NPCState(
                npc_id=npc["npc_id"],
                name=npc["name"],
                role=npc["role"],
                position=NPCPosition(**npc["position"]),
            )

    def get_npc_state(self, npc_id: str) -> Optional[NPCState]:
        """获取 NPC 状态"""
        return self.npc_states.get(npc_id)

    def get_all_npc_states(self) -> list[NPCState]:
        """获取所有 NPC 状态"""
        return list(self.npc_states.values())

    def is_npc_busy(self, npc_id: str) -> bool:
        """检查 NPC 是否忙碌"""
        npc = self.npc_states.get(npc_id)
        return npc.is_busy if npc else False

    def set_npc_busy(self, npc_id: str, busy: bool):
        """设置 NPC 忙碌状态"""
        if npc_id in self.npc_states:
            self.npc_states[npc_id].is_busy = busy
            if busy:
                self.npc_states[npc_id].last_interaction = datetime.now().isoformat()

    def update_background_dialogue(self, npc_id: str, dialogue: str):
        """更新 NPC 背景对话"""
        if npc_id in self.npc_states:
            self.npc_states[npc_id].background_dialogue = dialogue

    def get_npc_count(self) -> int:
        """获取 NPC 数量"""
        return len(self.npc_states)
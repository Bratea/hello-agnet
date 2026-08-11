#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
NPC Agent 管理器 — 管理所有 NPC 的 SimpleAgent 实例
"""
from typing import Optional

from hello_agents import HelloAgentsLLM, SimpleAgent

from agent.prompts.zhang_san import ZHANG_SAN_SYSTEM_PROMPT
from agent.prompts.li_si import LI_SI_SYSTEM_PROMPT
from agent.prompts.wang_wu import WANG_WU_SYSTEM_PROMPT
from config import get_settings
from model.entity.npc_state import NPCState


class NPCAgentManager:
    """NPC Agent 管理器"""

    def __init__(self, llm: Optional[HelloAgentsLLM] = None):
        self.llm = llm or HelloAgentsLLM()
        self.agents: dict[str, SimpleAgent] = {}
        self.npc_configs: dict[str, dict] = {
            "zhang_san": {
                "name": "张三",
                "role": "Python工程师",
                "personality": "严谨、专业、喜欢分享技术知识。说话直接，注重代码质量。",
                "prompt": ZHANG_SAN_SYSTEM_PROMPT,
            },
            "li_si": {
                "name": "李四",
                "role": "产品经理",
                "personality": "外向、善于沟通、注重用户体验。喜欢从用户角度思考问题。",
                "prompt": LI_SI_SYSTEM_PROMPT,
            },
            "wang_wu": {
                "name": "王五",
                "role": "UI设计师",
                "personality": "温和、富有创意、审美独特。注重视觉呈现和用户体验。",
                "prompt": WANG_WU_SYSTEM_PROMPT,
            },
        }

    def initialize_npcs(self):
        """初始化所有 NPC Agent"""
        for npc_id, config in self.npc_configs.items():
            agent = SimpleAgent(
                name=config["name"],
                llm=self.llm,
                system_prompt=config["prompt"],
            )
            self.agents[npc_id] = agent

    def get_agent(self, npc_id: str) -> Optional[SimpleAgent]:
        """获取指定 NPC 的 Agent"""
        return self.agents.get(npc_id)

    def get_agent_with_affinity(self, npc_id: str, affinity_level: str) -> SimpleAgent:
        """根据好感度等级获取 NPC Agent"""
        base_agent = self.get_agent(npc_id)
        if not base_agent:
            raise ValueError(f"NPC {npc_id} 不存在")

        config = self.npc_configs.get(npc_id, {})
        affinity_prompts = {
            "陌生": "你刚认识这位玩家，保持礼貌但不要过于热情。回复简短专业。",
            "熟悉": "你已经认识这位玩家，可以进行正常的交流。回复自然友好。",
            "友好": "你把这位玩家当作朋友，愿意分享更多信息。回复详细热情。",
            "亲密": "你非常信任这位玩家，可以分享私人话题。回复充满关心。",
            "挚友": "你把这位玩家当作最好的朋友，无话不谈。回复亲切真诚。",
        }

        system_prompt = f"""你是{config.get('name', npc_id)}，一位{config.get('role', '')}。
你的性格特点：{config.get('personality', '')}

当前与玩家的关系：{affinity_level}
{affinity_prompts.get(affinity_level, affinity_prompts['陌生'])}

你在Datawhale办公室工作，与同事们一起推动开源社区的发展。
请根据你的角色、性格和与玩家的关系，自然地回复。
"""

        return SimpleAgent(
            name=config.get("name", npc_id),
            llm=self.llm,
            system_prompt=system_prompt,
        )

    def has_npc(self, npc_id: str) -> bool:
        """检查 NPC 是否存在"""
        return npc_id in self.npc_configs

    def get_all_npcs(self) -> list[dict]:
        """获取所有 NPC 基本信息"""
        return [
            {"npc_id": npc_id, "name": cfg["name"], "role": cfg["role"]}
            for npc_id, cfg in self.npc_configs.items()
        ]
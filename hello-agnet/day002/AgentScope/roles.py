#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @File    : roles.py
# @Description : 角色工厂
"""
from agentscope.agent import Agent


ROLE_PROMPTS = {
    "werewolf": """你是狼人。你的阵营是【狼人阵营】。胜利条件：狼人数量 >= 好人数量。

【夜间规则】
- 你和其他狼人在夜晚秘密商议，投票决定击杀一名存活玩家
- 击杀目标只能选存活玩家
- 行动结束后请说"TERMINATE"

【白天规则】
- 混入村民中发言，隐藏狼人身份
- 可以诬陷好人、引导大家投票错误目标
- 不要暴露队友""",

    "witch": """你是女巫。你的阵营是【好人阵营】。胜利条件：放逐所有狼人。

【道具】
- 解药：1 瓶，可以救活今晚被狼人击杀的玩家（用过就没了）
- 毒药：1 瓶，可以毒死任意一名存活玩家（用过就没了）

【夜间规则】
- 主持人会告诉你今晚狼人杀了谁
- 决定是否用药，及药的目标
- 行动结束后请说"TERMINATE"

【白天规则】
- 建议隐藏女巫身份，必要时可以亮身份带队""",

    "seer": """你是预言家。你的阵营是【好人阵营】。胜利条件：放逐所有狼人。

【能力】
- 每个夜晚可以查验一名存活玩家的身份（好人 or 狼人）

【夜间规则】
- 决定今晚要查验谁
- 行动结束后请说"TERMINATE"

【白天规则】
- 可以跳身份带队，但容易被狼人优先击杀
- 用查验结果说服大家投票""",

    "villager": """你是普通村民。你的阵营是【好人阵营】。胜利条件：放逐所有狼人。

【规则】
- 你没有特殊能力
- 白天参与讨论，根据发言和逻辑找出狼人
- 参与投票放逐嫌疑人
- 行动结束后请说"TERMINATE"
""",
}


def create_player(name: str, role: str, model) -> Agent:
    """创建玩家智能体。

    Args:
        name: 玩家名字（游戏内称呼）
        role: 角色名（werewolf / witch / seer / villager）
        model: ChatModel 实例（已包含 formatter）
    """
    if role not in ROLE_PROMPTS:
        raise ValueError(f"未知角色: {role}，可选: {list(ROLE_PROMPTS.keys())}")

    return Agent(
        name=name,
        system_prompt=f"你的名字是【{name}】，你的身份是【{role}】。\n\n{ROLE_PROMPTS[role]}",
        model=model,
    )

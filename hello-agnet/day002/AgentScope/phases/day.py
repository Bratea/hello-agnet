#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @File    : phases/day.py
# @Description : 白天阶段：公布夜晚结果 → 讨论 → 投票
"""
from typing import Optional

from models import VoteDecision
from utils import broadcast, fanout, sequential_discuss, majority_vote, make_msg, extract_structured


async def announce_night_result(alive_players: list, deaths: list) -> None:
    """公布夜晚死亡结果。"""
    print(f"\n{'='*50}\n[白天] 公布夜晚结果\n{'='*50}")

    if not deaths:
        content = "天亮了，昨晚是平安夜，没有人死亡。"
    else:
        content = f"天亮了，昨晚死亡的玩家是：{', '.join(deaths)}。"

    print(f"  → {content}")
    await broadcast(
        [make_msg("Moderator", content)],
        alive_players,
    )


async def discussion_phase(alive_players: list, max_rounds: int = 1) -> None:
    """讨论阶段：每个存活玩家依次发言。"""
    print(f"\n{'='*50}\n[白天] 讨论阶段 - 顺序发言\n{'='*50}")

    open_msg = make_msg(
        "Moderator",
        "请每位玩家依次发言，分析谁是狼人。发言结束后说 TERMINATE。",
    )
    for round_idx in range(max_rounds):
        print(f"\n--- 讨论第 {round_idx + 1} 轮 ---")
        await sequential_discuss(alive_players, open_msg)


async def vote_phase(alive_players: list) -> Optional[str]:
    """投票阶段：所有存活玩家并行投票。"""
    print(f"\n{'='*50}\n[白天] 投票阶段\n{'='*50}")

    vote_msg = make_msg("Moderator", "请投票放逐你认为是狼人的玩家：")
    responses = await fanout(alive_players, vote_msg, structured_schema=VoteDecision)

    votes = []
    for resp, p in zip(responses, alive_players):
        decision = extract_structured(resp, VoteDecision)
        if decision:
            print(f"  {p.name} → {decision.target} ({decision.reasoning})")
            votes.append(decision.target)

    target = majority_vote(votes)
    print(f"\n[投票结果] 被放逐: {target}")
    return target

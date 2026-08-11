#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @File    : phases/night.py
# @Description : 夜晚阶段：狼人 → 女巫 → 预言家
"""
from typing import Optional

from models import KillDecision, WitchAction, SeerCheck
from utils import broadcast, fanout, sequential_discuss, majority_vote, make_msg, extract_structured


async def werewolf_phase(werewolves: list, alive_players: list) -> Optional[str]:
    """狼人阶段：所有狼人讨论并投票决定击杀目标。"""
    if not werewolves:
        return None

    print(f"\n{'='*50}\n[夜晚] 狼人阶段 - 存活狼人: {[w.name for w in werewolves]}\n{'='*50}")

    alive_names = [p.name for p in alive_players]

    # 1. 主持人公告（只发给狼人）
    await broadcast(
        [make_msg("Moderator", f"狼人们请注意。今晚存活玩家：{alive_names}。请讨论并选择击杀目标。")],
        werewolves,
    )

    # 2. 讨论阶段
    print("\n[狼人讨论]")
    discuss_msg = make_msg("Moderator", "请发表你的看法：")
    await sequential_discuss(werewolves, discuss_msg)

    # 3. 投票阶段
    print("\n[狼人投票]")
    vote_msg = make_msg("Moderator", "现在请投票决定今晚的击杀目标：")
    vote_responses = await fanout(werewolves, vote_msg, structured_schema=KillDecision)

    targets = []
    for resp, wolf in zip(vote_responses, werewolves):
        decision = extract_structured(resp, KillDecision)
        if decision:
            print(f"  {wolf.name} → {decision.target} ({decision.reasoning})")
            targets.append(decision.target)

    final_target = majority_vote(targets, default=None)
    print(f"\n[狼人决定] 击杀目标: {final_target}")
    return final_target


async def witch_phase(witch, werewolf_target: Optional[str], alive_players: list) -> dict:
    """女巫阶段：决定是否用药。"""
    if witch is None:
        return {"saved": False, "poisoned": None}

    print(f"\n{'='*50}\n[夜晚] 女巫阶段\n{'='*50}")

    alive_names = [p.name for p in alive_players if p is not witch]

    # 告诉女巫今晚谁被狼人杀了
    info = make_msg(
        "Moderator",
        f"今晚狼人击杀了【{werewolf_target}】。你有一瓶解药和一瓶毒药。\n存活玩家：{alive_names}",
    )
    await witch.observe(info)

    action_msg = make_msg("Moderator", "请决定你的行动：")
    resp = await witch.reply(action_msg, structured_schema=WitchAction)
    action = extract_structured(resp, WitchAction)

    result = {"saved": False, "poisoned": None}
    if action:
        print(f"  {witch.name} → 解药:{action.use_antidote}, 毒药:{action.use_poison}, 目标:{action.target_name}")
        if action.use_antidote and werewolf_target:
            result["saved"] = True
        if action.use_poison and action.target_name:
            result["poisoned"] = action.target_name

    return result


async def seer_phase(seer, alive_players: list) -> Optional[dict]:
    """预言家阶段：查验一名玩家。"""
    if seer is None:
        return None

    print(f"\n{'='*50}\n[夜晚] 预言家阶段\n{'='*50}")

    alive_names = [p.name for p in alive_players if p is not seer]

    info = make_msg(
        "Moderator",
        f"今晚你可以查验一名玩家。存活玩家：{alive_names}",
    )
    await seer.observe(info)

    action_msg = make_msg("Moderator", "请选择要查验的玩家：")
    resp = await seer.reply(action_msg, structured_schema=SeerCheck)
    check = extract_structured(resp, SeerCheck)

    if check:
        target_player = next((p for p in alive_players if p.name == check.target), None)
        target_role = target_player.role if target_player else "unknown"
        result_msg = make_msg(
            "Moderator",
            f"查验结果：{check.target} 的身份是【{target_role}】。",
        )
        await seer.observe(result_msg)
        print(f"  {seer.name} 查验了 {check.target} → {target_role}")
        return {"seer": seer.name, "target": check.target, "result": target_role}
    return None

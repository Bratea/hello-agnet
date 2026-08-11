#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @File    : utils.py
# @Description : AgentScope 2.0 协作工具（替代 1.x 的 MsgHub / fanout_pipeline）
"""
import asyncio
from collections import Counter
from typing import List

from agentscope.message import Msg, TextBlock


def make_msg(name: str, text: str, role: str = "user") -> Msg:
    """构造 Msg 的快捷方式（content 必须是 list[ContentBlock]）。

    默认 role='user'，因为 observe() 不接受 system role。
    """
    return Msg(name=name, content=[TextBlock(text=text)], role=role)


async def broadcast(messages: List[Msg], participants: list, exclude: list = None) -> None:
    """替代 MsgHub：把一条/多条消息广播给所有参与者。

    Args:
        messages: 要广播的消息列表
        participants: 接收者列表
        exclude: 排除的接收者（比如发言者本人）
    """
    exclude_ids = {id(p) for p in (exclude or [])}
    tasks = []
    for p in participants:
        if id(p) in exclude_ids:
            continue
        for msg in messages:
            tasks.append(p.observe(msg))
    if tasks:
        await asyncio.gather(*tasks)


async def fanout(participants: list, msg: Msg, structured_schema=None) -> list:
    """替代 fanout_pipeline：并行调用所有参与者。

    Args:
        participants: 要调用的智能体列表
        msg: 发送的消息
        structured_schema: Pydantic 模型，约束结构化输出

    Returns:
        所有智能体的回复（Msg 列表）
    """
    coros = [
        p.reply(msg, structured_schema=structured_schema) if structured_schema else p.reply(msg)
        for p in participants
    ]
    return await asyncio.gather(*coros)


async def sequential_discuss(participants: list, msg: Msg, structured_schema=None) -> list:
    """顺序发言场景：每个参与者依次回复，其他人能看到前面所有发言。

    Args:
        participants: 参与讨论的智能体列表
        msg: 主持人开场消息
        structured_schema: 约束输出格式

    Returns:
        所有发言的 Msg 列表
    """
    results = []
    for p in participants:
        if structured_schema:
            resp = await p.reply(msg, structured_schema=structured_schema)
        else:
            resp = await p.reply(msg)
        results.append(resp)
        # 把当前发言广播给所有其他参与者（包括后面还没发言的）
        await broadcast([resp], participants, exclude=[p])
    return results


def majority_vote(choices: list, default: str = None):
    """简单多数票。空列表返回 default。"""
    if not choices:
        return default
    counter = Counter(choices)
    return counter.most_common(1)[0][0]


def extract_structured(resp: Msg, schema_cls):
    """从 Msg 中提取结构化输出（AgentScope 2.0 放在 structured_output 字段里）。"""
    # 优先从 structured_output 字段取
    so = getattr(resp, "structured_output", None)
    if isinstance(so, schema_cls):
        return so
    if isinstance(so, dict):
        try:
            return schema_cls(**so)
        except Exception:
            pass
    # 兜底：尝试从 metadata 找
    meta = getattr(resp, "metadata", None) or {}
    for value in meta.values():
        if isinstance(value, schema_cls):
            return value
    return None

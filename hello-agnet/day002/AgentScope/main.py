#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @File    : main.py
# @Description : 入口
"""
import asyncio
import os

from dotenv import load_dotenv

from agentscope.model import OpenAIChatModel
from agentscope.credential import OpenAICredential
from agentscope.formatter import OpenAIChatFormatter

from roles import create_player
from game import WerewolfGame, Player


def build_model_and_formatter():
    """从 .env 读取配置，创建模型（formatter 作为 model 的一部分）。"""
    load_dotenv(override=True)

    print("API_KEY:", os.getenv("LLM_API_KEY"))
    print("BASE_URL:", os.getenv("LLM_BASE_URL"))
    print("MODEL_ID:", os.getenv("LLM_MODEL_ID"))

    api_key = os.getenv("LLM_API_KEY")
    base_url = os.getenv("LLM_BASE_URL")
    model_name = os.getenv("LLM_MODEL_ID")

    if not all([api_key, base_url, model_name]):
        raise RuntimeError(
            "请在 .env 里配置 LLM_API_KEY、LLM_BASE_URL、LLM_MODEL_ID"
        )

    credential = OpenAICredential(api_key=api_key, base_url=base_url)
    formatter = OpenAIChatFormatter()
    model = OpenAIChatModel(
        credential=credential,
        model=model_name,
        formatter=formatter,

    )
    return model


def setup_5_player_game() -> WerewolfGame:
    """构建 5 人局：2 狼人 + 1 女巫 + 1 预言家 + 1 村民"""
    model = build_model_and_formatter()

    # 5 个玩家的身份分配
    role_assignments = [
        ("Alice", "werewolf"),
        ("Bob",   "werewolf"),
        ("Carol", "witch"),
        ("Dave",  "seer"),
        ("Eve",   "villager"),
    ]

    players = []
    for name, role in role_assignments:
        agent = create_player(name, role, model)
        players.append(Player(name=name, role=role, agent=agent))

    return WerewolfGame(players, max_rounds=1)


async def main():
    game = setup_5_player_game()
    await game.run()


if __name__ == "__main__":
    asyncio.run(main())

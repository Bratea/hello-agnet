#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @File    : game.py
# @Description : 游戏主控（最小版本：5 人局，1 轮）
"""
from dataclasses import dataclass, field
from typing import List, Optional

from roles import create_player
from phases.night import werewolf_phase, witch_phase, seer_phase
from phases.day import announce_night_result, discussion_phase, vote_phase


@dataclass
class Player:
    """玩家数据类（轻量，存储身份信息）"""
    name: str
    role: str
    agent: object = None  # Agent 实例
    alive: bool = True


class WerewolfGame:
    """狼人杀游戏主控"""

    def __init__(self, players: List[Player], max_rounds: int = 1):
        self.players = players
        self.max_rounds = max_rounds
        self.round_num = 0

    @property
    def alive_players(self) -> List[Player]:
        return [p for p in self.players if p.alive]

    @property
    def werewolves(self) -> List[Player]:
        return [p for p in self.alive_players if p.role == "werewolf"]

    @property
    def witch(self) -> Optional[Player]:
        for p in self.alive_players:
            if p.role == "witch":
                return p.agent
        return None

    @property
    def seer(self) -> Optional[Player]:
        for p in self.alive_players:
            if p.role == "seer":
                return p.agent
        return None

    def is_game_over(self) -> bool:
        """判断游戏是否结束"""
        wolves = len(self.werewolves)
        good = len(self.alive_players) - wolves
        # 狼人全死 → 好人胜；狼人 >= 好人 → 狼人胜
        return wolves == 0 or wolves >= good

    def announce_winner(self):
        """宣布胜利方"""
        if len(self.werewolves) == 0:
            print("\n🏆 游戏结束！好人阵营胜利！")
        else:
            print("\n🐺 游戏结束！狼人阵营胜利！")
        print("\n所有玩家身份：")
        for p in self.players:
            status = "存活" if p.alive else "死亡"
            print(f"  - {p.name}: {p.role} ({status})")

    async def run_night(self) -> list:
        """运行夜晚阶段，返回死亡名单"""
        print(f"\n🌙 第 {self.round_num} 夜开始")

        # 1. 狼人阶段
        werewolf_target = await werewolf_phase(
            werewolves=[w.agent for w in self.werewolves],
            alive_players=self.alive_players,
        )

        # 2. 女巫阶段
        witch_result = await witch_phase(
            witch=self.witch,
            werewolf_target=werewolf_target,
            alive_players=self.alive_players,
        )

        # 3. 预言家阶段
        await seer_phase(self.seer, self.alive_players)

        # 4. 应用夜晚结果
        deaths = []
        if werewolf_target and not witch_result["saved"]:
            target_player = next((p for p in self.players if p.name == werewolf_target), None)
            if target_player and target_player.alive:
                target_player.alive = False
                deaths.append(target_player.name)
                print(f"\n💀 {target_player.name} 被狼人杀死")

        if witch_result["poisoned"]:
            target_player = next((p for p in self.players if p.name == witch_result["poisoned"]), None)
            if target_player and target_player.alive:
                target_player.alive = False
                deaths.append(target_player.name)
                print(f"💀 {target_player.name} 被女巫毒死")

        return deaths

    async def run_day(self) -> list:
        """运行白天阶段，返回放逐名单"""
        print(f"\n☀️ 第 {self.round_num} 白天开始")

        # 1. 公布夜晚结果
        await announce_night_result(self.alive_players, [])

        # 2. 讨论
        await discussion_phase(self.alive_players, max_rounds=1)

        # 3. 投票
        vote_target = await vote_phase([p.agent for p in self.alive_players])

        deaths = []
        if vote_target:
            target_player = next((p for p in self.players if p.name == vote_target), None)
            if target_player and target_player.alive:
                target_player.alive = False
                deaths.append(target_player.name)
                print(f"\n⚰️ {target_player.name} 被放逐")

        return deaths

    async def run(self):
        """游戏主循环（最小版：1 轮）"""
        print("\n" + "=" * 60)
        print("🐺 狼人杀 - 最小版本 (5 人 1 轮)")
        print("=" * 60)

        # 打印初始身份
        print("\n游戏开始！玩家身份：")
        for p in self.players:
            print(f"  - {p.name}: {p.role}")

        for _ in range(self.max_rounds):
            self.round_num += 1

            # 夜晚
            await self.run_night()
            if self.is_game_over():
                break

            # 白天
            await self.run_day()
            if self.is_game_over():
                break

        self.announce_winner()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @File    : models.py
# @Description : 结构化输出模型（Pydantic）
"""
from typing import Optional, List
from pydantic import BaseModel, Field


class DiscussionOutput(BaseModel):
    """讨论发言输出"""
    reach_agreement: bool = Field(default=False, description="是否已达成一致意见")
    confidence_level: int = Field(ge=1, le=10, default=5, description="对当前推理的信心程度(1-10)")
    key_evidence: Optional[str] = Field(default=None, description="支持你观点的关键证据")


class KillDecision(BaseModel):
    """狼人击杀决策"""
    target: str = Field(description="要击杀的玩家名字")
    reasoning: str = Field(description="选择该目标的理由")


class WitchAction(BaseModel):
    """女巫行动"""
    use_antidote: bool = Field(default=False, description="是否使用解药救人")
    use_poison: bool = Field(default=False, description="是否使用毒药")
    target_name: Optional[str] = Field(default=None, description="毒药目标玩家姓名")


class SeerCheck(BaseModel):
    """预言家查验"""
    target: str = Field(description="要查验的玩家名字")


class VoteDecision(BaseModel):
    """投票决策"""
    target: str = Field(description="投票放逐的玩家")
    reasoning: str = Field(description="投票理由")

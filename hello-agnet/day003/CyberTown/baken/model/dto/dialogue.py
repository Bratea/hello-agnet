#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
对话 DTO
"""
from typing import Optional
from pydantic import BaseModel, Field


class DialogueRequest(BaseModel):
    """对话请求"""
    npc_id: str = Field(..., description="NPC ID")
    player_name: str = Field(default="玩家", description="玩家名称")
    player_message: str = Field(..., description="玩家消息")


class DialogueResponse(BaseModel):
    """对话响应"""
    npc_reply: str = Field(..., description="NPC 回复")
    affinity_level: str = Field(..., description="好感度等级")
    affinity_score: float = Field(..., description="好感度分数")


class AffinityRequest(BaseModel):
    """好感度查询请求"""
    npc_id: str = Field(..., description="NPC ID")
    player_name: str = Field(default="玩家", description="玩家名称")


class AffinityInfo(BaseModel):
    """好感度信息"""
    score: float = Field(0, description="好感度分数")
    level: str = Field("陌生", description="好感度等级")
    interaction_count: int = Field(0, description="互动次数")


class NPCStatusResponse(BaseModel):
    """NPC 状态列表响应"""
    npcs: list


class BatchDialogueResponse(BaseModel):
    """批量对话响应"""
    dialogues: dict
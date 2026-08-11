#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
NPC 状态实体
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class NPCPosition(BaseModel):
    """NPC 位置"""
    x: float = 0
    y: float = 0


class NPCState(BaseModel):
    """NPC 状态"""
    npc_id: str
    name: str
    role: str
    personality: str = ""
    position: NPCPosition = NPCPosition()
    is_busy: bool = False
    current_action: str = "idle"
    last_interaction: Optional[str] = None
    background_dialogue: str = ""


class NPCStatus(BaseModel):
    """NPC 状态响应"""
    npc_id: str
    name: str
    role: str
    position: dict
    is_busy: bool
    current_action: str
    background_dialogue: str
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
好感度 DTO
"""
from pydantic import BaseModel, Field


class AffinityInfo(BaseModel):
    """好感度信息"""
    score: float = Field(0, ge=0, le=100, description="好感度分数")
    level: str = Field("陌生", description="好感度等级")
    interaction_count: int = Field(0, description="互动次数")
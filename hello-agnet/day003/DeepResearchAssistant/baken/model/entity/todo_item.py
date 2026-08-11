#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
子任务实体
"""
from pydantic import BaseModel


class TodoItem(BaseModel):
    """子任务项"""
    id: int
    title: str
    intent: str
    query: str
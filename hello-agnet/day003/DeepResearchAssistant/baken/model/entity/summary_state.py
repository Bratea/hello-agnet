#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
研究状态实体
"""
from typing import List, Optional
from pydantic import BaseModel

from model.entity.todo_item import TodoItem


class SummaryState(BaseModel):
    """研究状态"""
    research_topic: str
    todo_items: Optional[List[TodoItem]] = None
    current_task_index: int = 0
    is_completed: bool = False
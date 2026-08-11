#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2026/8/10 14:47
# @Author  : 小陈
# @File    : DayPlan.py
# @Software: PyCharm
"""
from typing import Optional, List

from pydantic import BaseModel,Field
from model.entity.attraction import Attraction
from model.entity.hotel import Hotel
from model.entity.meal import Meal


class DayPlan(BaseModel):
    """单日行程"""
    date: Optional[str] = Field(default=None,description="日期")
    day_index: Optional[int] = Field(default=None,description="第几天(从0开始)")
    description: Optional[str] = Field(default=None,description="当日行程描述")
    transportation: Optional[str] = Field(default=None,description="交通方式")
    accommodation: Optional[str] = Field(default=None,description="住宿安排")
    hotel: Optional[Hotel] = Field(default=None,description="酒店信息")
    attractions: List[Attraction] = Field(default_factory=list,description="景点列表")
    meals: List[Meal] = Field(default_factory=list,description="餐饮安排")

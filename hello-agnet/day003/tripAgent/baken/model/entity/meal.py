#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2026/8/10 14:41
# @Author  : 小陈
# @File    : Meal.py
# @Software: PyCharm
"""

from pydantic import BaseModel,Field
from typing import Optional
from model.entity.location import Location

class Meal(BaseModel):
    """餐饮信息"""
    type: Optional[str] = Field(default=None,description="餐饮类型：breakfast/lunch/dinner/snack")
    name: Optional[str] = Field(default=None,description="餐饮名称")
    address: Optional[str] = Field(default=None,description="地址")
    location: Optional[Location] = Field(default=None,description="经纬度坐标")
    description: Optional[str] = Field(default=None,description="描述")
    estimated_cost: int = Field(default=0,description="预估费用(元)")

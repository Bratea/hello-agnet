#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2026/8/10 14:39
# @Author  : 小陈
# @File    : Attraction.py
# @Software: PyCharm
"""

from pydantic import BaseModel,Field
from typing import Optional
from model.entity.location import Location


class Attraction(BaseModel):
    """景点信息"""
    name: str = Field(...,description="景点名称")
    address: Optional[str] = Field(default=None,description="地址")
    location: Optional[Location] = Field(default=None,description="经纬度坐标")
    visit_duration: Optional[int] = Field(default=None,description="建议游览时间(分钟)")
    description: Optional[str] = Field(default=None,description="景点描述")
    category: Optional[str] = Field(default="景点",description="景点类别")
    rating: Optional[float] = Field(default=None,ge=0,le=5,description="评分")
    image_url: Optional[str] = Field(default=None,description="图片URL")
    ticket_price: int = Field(default=0,ge=0,description="门票价格(元)")

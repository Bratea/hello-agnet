#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2026/8/10 14:46
# @Author  : 小陈
# @File    : Budget.py
# @Software: PyCharm
"""

from typing import Optional, Union
from pydantic import BaseModel,Field

class Budget(BaseModel):
    """预算信息"""
    total_attractions: Optional[Union[int, str]] = Field(default=None,description="景点门票总费用")
    total_hotels: Optional[Union[int, str]] = Field(default=None,description="酒店总费用")
    total_meals: Optional[Union[int, str]] = Field(default=None,description="餐饮总费用")
    total_transportation: Optional[Union[int, str]] = Field(default=None,description="交通总费用")
    total: Optional[Union[int, str]] = Field(default=None,description="总费用")

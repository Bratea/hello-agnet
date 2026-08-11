#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2026/8/10 15:16
# @Author  : 小陈
# @File    : TripPlanRequest.py
# @Software: PyCharm
"""

from pydantic import BaseModel

class TripPlanRequest(BaseModel):
    city: str
    start_date: str
    end_date: str
    days: int
    preferences: str = ""
    budget: str = ""
    transportation: str = ""
    accommodation: str = ""
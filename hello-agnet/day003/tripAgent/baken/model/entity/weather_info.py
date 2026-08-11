#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2026/8/10 14:49
# @Author  : 小陈
# @File    : WeatherInfo.py
# @Software: PyCharm
"""

from typing import Optional, Union
from pydantic import field_validator
from pydantic import BaseModel,Field

class WeatherInfo(BaseModel):
    """天气信息"""
    date: Optional[str] = Field(default=None, description="日期")
    day_weather: Optional[str] = Field(default=None, description="白天天气")
    night_weather: Optional[str] = Field(default=None, description="夜间天气")
    day_temp: Optional[int] = Field(default=None, description="白天温度(摄氏度)")
    night_temp: Optional[int] = Field(default=None, description="夜间温度(摄氏度)")
    wind_direction: Optional[Union[int, str]] = Field(default=None, description="风向")
    wind_power: Optional[Union[int, str]] = Field(default=None, description="风力")

    @field_validator('day_temp', 'night_temp', mode='before')
    def parse_temperature(cls, v):
        """解析温度字符串："16°C" -> 16"""
        if isinstance(v, str):
            v = v.replace('°C', '').replace('℃', '').replace('°', '').strip()
            try:
                return int(v)
            except ValueError:
                return 0  # 容错处理
        return v

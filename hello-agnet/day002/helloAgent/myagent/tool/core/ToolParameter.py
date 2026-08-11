#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2026/8/8 15:10
# @Author  : 小陈
# @File    : ToolParameter.py
# @Software: PyCharm
"""

class ToolParameter(BaseModel):
    """工具参数定义"""
    name: str
    type: str
    description: str
    required: bool = True
    default: Any = None

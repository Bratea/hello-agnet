#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2026/8/11 15:23
# @Author  : 小陈
# @File    : person.py
# @Software: PyCharm
"""

from pydantic import BaseModel


class Person(BaseModel):
    """
    人员模型
    请求示例: {"name": "张三", "age": 25, "email": "zhangsan@example.com"}
    """

    name: str
    age: int
    email: str | None = None  # 可选字段

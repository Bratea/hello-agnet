#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2026/8/11 15:23
# @Author  : 小陈
# @File    : person_router.py
# @Software: PyCharm
"""

from fastapi import APIRouter
from model.person import Person


# 相当于 Java 的 @Controller，url 前缀是 /persons
router = APIRouter(prefix="/persons", tags=["人员管理"])


@router.get("")
def get_persons():
    """返回人员列表"""
    return [
        {"name": "张三", "age": 25, "email": "zhangsan@example.com"},
        {"name": "李四", "age": 30, "email": None},
    ]


@router.post("")
def create_person(person: Person):
    """新增人员"""
    return {
        "message": f"已创建用户: {person.name}",
        "age": person.age,
        "email": person.email,
    }

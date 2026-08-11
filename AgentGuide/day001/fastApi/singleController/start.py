#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2026/8/11 15:41
# @Author  : 小陈
# @File    : start.py
# @Software: PyCharm
#
# ============================================
# 单控制器模式（Single Controller）
# 所有路由写在一个文件里，不拆 APIRouter
# 适合：小项目、快速原型、学习阶段
# ============================================
"""

# 1. 安装依赖
#    pip install "fastapi[standard]"

# 2. 导入
from fastapi import FastAPI
from pydantic import BaseModel

# 3. 创建应用实例
app = FastAPI()


# ============================================
# 数据模型
# ============================================


class Item(BaseModel):
    """商品模型"""

    name: str
    price: float
    is_offer: bool | None = None


class Person(BaseModel):
    """人员模型"""

    name: str
    age: int
    email: str | None = None


# ============================================
# 路由 — 根路径
# ============================================


@app.get("/")
def read_root():
    """根路径"""
    return {"Hello": "World"}


# ============================================
# 路由 — 商品相关
# ============================================


@app.get("/items")
def get_items():
    """获取商品列表"""
    return [
        {"name": "苹果", "price": 5.5},
        {"name": "香蕉", "price": 3.0, "is_offer": True},
    ]


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    """根据 ID 查询商品"""
    return {"item_id": item_id, "q": q}


@app.post("/items")
def create_item(item: Item):
    """新增商品"""
    return {"message": f"已收到商品: {item.name}", "price": item.price}


# ============================================
# 路由 — 人员相关
# ============================================


@app.get("/persons")
def get_persons():
    """获取人员列表"""
    return [
        {"name": "张三", "age": 25},
        {"name": "李四", "age": 30},
    ]


@app.post("/persons")
def create_person(person: Person):
    """新增人员"""
    return {"message": f"已创建用户: {person.name}", "age": person.age}

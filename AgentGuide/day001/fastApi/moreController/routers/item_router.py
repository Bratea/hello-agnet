#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2026/8/11 15:08
# @Author  : 小陈
# @File    : item_router.py
# @Software: PyCharm
"""

from fastapi import APIRouter
from pydantic import BaseModel


# 相当于 Java 的 @Controller，url 前缀是 /items
router = APIRouter(prefix="/items", tags=["商品管理"])


class Item(BaseModel):
    """
    商品模型
    请求示例: {"name": "苹果", "price": 5.5, "is_offer": true}
    """

    name: str
    price: float
    is_offer: bool | None = None  # 可选


@router.get("")
def get_items():
    """返回商品列表"""
    return [
        {"name": "苹果", "price": 5.5},
        {"name": "香蕉", "price": 3.0, "is_offer": True},
        {"name": "樱桃", "price": 15.0},
    ]


@router.get("/{item_id}")
def read_item(item_id: int, q: str | None = None):
    """根据 item_id 查询商品"""
    return {"item_id": item_id, "q": q}


@router.post("")
def create_item(item: Item):
    """新增商品"""
    return {
        "message": f"已收到商品: {item.name}",
        "price": item.price,
        "is_offer": item.is_offer,
    }

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2026/8/11 15:08
# @Author  : 小陈
# @File    : start.py
# @Software: PyCharm
"""

# ============================================
# 1. 安装依赖
# 执行: pip install "fastapi[standard]"
# ============================================

# 2. 导入 FastAPI
from fastapi import FastAPI

# 3. 导入所有 router（相当于 Java 的 Controller）
from routers.item_router import router as item_router
from routers.person_router import router as person_router

# 4. 创建 FastAPI 应用实例
app = FastAPI()

# 5. 注册 router（把 controller 挂到主应用上）
app.include_router(item_router)
app.include_router(person_router)


# 6. 根路由（公用的放这里）
@app.get("/")
def read_root():
    """返回一个简单的问候消息"""
    return {"Hello": "World"}

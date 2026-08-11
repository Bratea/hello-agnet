#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FastAPI 入口 — 挂载赛博小镇路由并启动服务
"""
import os
import logging

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

load_dotenv(override=True)

# 尝试从项目根目录加载 .env
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path, override=True)

logging.basicConfig(level=logging.INFO)

from router.cyber_town import router as cyber_town_router, godot_router as godot_compat_router, start_background_tasks

app = FastAPI(
    title="赛博小镇后端服务",
    description="基于 HelloAgents 的 AI NPC 对话系统",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cyber_town_router)
app.include_router(godot_compat_router)


@app.on_event("startup")
async def startup():
    start_background_tasks()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
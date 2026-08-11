#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FastAPI 入口 — 挂载路由并启动服务
"""
import os
import logging

from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn

# 加载项目根目录的 .env 文件
env_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env")
load_dotenv(dotenv_path=env_path)
logging.basicConfig(level=logging.INFO)

from router.research import router as research_router

app = FastAPI(title="深度研究助手 API")
app.include_router(research_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
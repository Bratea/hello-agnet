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

load_dotenv(override=True)
logging.basicConfig(level=logging.INFO)

from router.trip import router as trip_router

app = FastAPI(title="旅行规划助手 API")
app.include_router(trip_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
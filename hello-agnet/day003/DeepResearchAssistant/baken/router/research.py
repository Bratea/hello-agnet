#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
研究路由 — FastAPI 端点 + SSE 流式推流（@RestController）
"""
import json
import logging
from typing import AsyncGenerator

from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

from agent.research_agent import DeepResearchAgent
from config import Configuration

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["research"])


# ---- 事件队列 ----

class EventQueue:
    """异步事件队列，在 Agent 和 SSE 之间传递事件"""

    def __init__(self):
        self._events: list = []

    def push(self, event: dict):
        self._events.append(event)

    def pop_all(self) -> list:
        events = self._events[:]
        self._events.clear()
        return events


# ---- SSE 流式生成器 ----

async def research_stream(topic: str) -> AsyncGenerator[str, None]:
    """研究流式生成器，产生 SSE 格式数据"""
    config = Configuration()
    agent = DeepResearchAgent(config)
    queue = EventQueue()

    agent.on_event(lambda e: queue.push(e))

    try:
        yield f"data: {json.dumps({'type': 'progress', 'stage': 'planning', 'percentage': 10, 'text': '正在规划研究任务...'}, ensure_ascii=False)}\n\n"

        import asyncio
        loop = asyncio.get_event_loop()
        report = await loop.run_in_executor(None, agent.run, topic)

        for event in queue.pop_all():
            yield f"data: {json.dumps(event, ensure_ascii=False)}\n\n"

        yield f"data: {json.dumps({'type': 'report', 'data': report}, ensure_ascii=False)}\n\n"
        yield f"data: {json.dumps({'type': 'progress', 'stage': 'completed', 'percentage': 100, 'text': '研究完成！'}, ensure_ascii=False)}\n\n"

    except Exception as e:
        logger.exception("研究过程出错")
        yield f"data: {json.dumps({'type': 'error', 'message': str(e)}, ensure_ascii=False)}\n\n"


# ---- 路由 ----

@router.get("/research")
async def research(topic: str = Query(..., description="研究主题")):
    """研究端点（SSE）"""
    return StreamingResponse(
        research_stream(topic),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "http://localhost:5173",
        }
    )


@router.get("/health")
async def health():
    """健康检查"""
    return {"status": "ok"}
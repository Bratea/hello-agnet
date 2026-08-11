#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
旅行路由 — FastAPI 端点（@RestController）
"""
import asyncio

from fastapi import APIRouter

from config import get_settings
from model.entity.trip_plan import TripPlan
from model.dto.trip_plan_request import TripPlanRequest
from agent.TripPlannerAgent import TripPlannerAgent
from tools.unsplash_client import UnsplashClient

router = APIRouter(prefix="/api/trip", tags=["trip"])

# 模块级单例
_planner = TripPlannerAgent()
_unsplash = UnsplashClient(get_settings().unsplash_access_key)


def _generate(request: TripPlanRequest) -> TripPlan:
    trip_plan = _planner.plan_trip(request)
    for day in trip_plan.days:
        for attr in day.attractions:
            if not attr.image_url:
                attr.image_url = _unsplash.get_photo_url(f"{attr.name} {trip_plan.city}")
    return trip_plan


@router.post("/plan", response_model=TripPlan)
async def create_trip_plan(request: TripPlanRequest) -> TripPlan:
    """生成旅行计划"""
    return await asyncio.to_thread(_generate, request)
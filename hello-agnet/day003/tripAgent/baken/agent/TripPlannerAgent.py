#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
行程规划 Agent — 主控 Agent，协调景点/天气/酒店子 Agent 生成旅行计划
"""
import json
import os
import re
import concurrent.futures
from typing import Optional

from dotenv import load_dotenv
from hello_agents import HelloAgentsLLM, SimpleAgent
from hello_agents.tools import MCPTool

from config import get_settings
from model.entity.trip_plan import TripPlan
from model.dto.trip_plan_request import TripPlanRequest
from agent.prompts.attraction import ATTRACTION_AGENT_PROMPT
from agent.prompts.weather import WEATHER_AGENT_PROMPT
from agent.prompts.hotel import HOTEL_AGENT_PROMPT
from agent.prompts.planner import PLANNER_AGENT_PROMPT


class TripPlannerAgent:

    def __init__(self):
        load_dotenv(override=True)

        self.llm = HelloAgentsLLM(
            model=os.getenv("LLM_MODEL_ID"),
            api_key=os.getenv("LLM_API_KEY"),
            base_url=os.getenv("LLM_BASE_URL"),
        )

        settings = get_settings()
        mcp_tool = MCPTool(name="amap_mcp",
                           server_command=["npx", "-y", "@amap/amap-maps-mcp-server"],
                           env={"AMAP_MAPS_API_KEY": settings.amap_api_key},
                           auto_expand=True)

        self.attraction_agent = SimpleAgent(name="景点搜索", llm=self.llm, system_prompt=ATTRACTION_AGENT_PROMPT)
        self.weather_agent = SimpleAgent(name="天气查询", llm=self.llm, system_prompt=WEATHER_AGENT_PROMPT)
        self.hotel_agent = SimpleAgent(name="酒店推荐", llm=self.llm, system_prompt=HOTEL_AGENT_PROMPT)

        self.attraction_agent.add_tool(mcp_tool)
        self.weather_agent.add_tool(mcp_tool)
        self.hotel_agent.add_tool(mcp_tool)

        self.planner_agent = SimpleAgent(name="行程规划", llm=self.llm, system_prompt=PLANNER_AGENT_PROMPT)

    def plan_trip(self, request: TripPlanRequest) -> TripPlan:
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
            f_attr  = ex.submit(self.attraction_agent.run, f"请搜索{request.city}的{request.preferences}景点")
            f_wea   = ex.submit(self.weather_agent.run,    f"请查询{request.city}的天气")
            f_hotel = ex.submit(self.hotel_agent.run,     f"请搜索{request.city}的{request.accommodation}酒店")
            attraction_response = f_attr.result()
            weather_response    = f_wea.result()
            hotel_response      = f_hotel.result()

        planner_query = self._build_planner_query(request, attraction_response, weather_response, hotel_response)
        planner_response = self.planner_agent.run(planner_query)

        return self._parse_trip_plan(planner_response)

    def _build_planner_query(self, request, attraction_response, weather_response, hotel_response) -> str:
        return f"""
    请根据以下信息生成{request.city}的{request.days}日旅行计划:

    **用户需求:**
    - 目的地: {request.city}
    - 日期: {request.start_date} 至 {request.end_date}
    - 天数: {request.days}天
    - 偏好: {request.preferences}
    - 预算: {request.budget}
    - 交通方式: {request.transportation}
    - 住宿类型: {request.accommodation}

    **景点信息:** {attraction_response}
    **天气信息:** {weather_response}
    **酒店信息:** {hotel_response}

    请生成详细的旅行计划,包括每天的景点安排、餐饮推荐、住宿信息和预算明细。
    """

    def _parse_trip_plan(self, text: str) -> TripPlan:
        data = self._extract_json(text)
        if data is None:
            raise ValueError("行程规划结果解析失败,请稍后重试")
        data = self._normalize_plan(data)
        return TripPlan.model_validate(data)

    @staticmethod
    def _normalize_plan(data: dict) -> dict:
        days = data.get("days") if isinstance(data, dict) else None
        if isinstance(days, list):
            for day in days:
                if not isinstance(day, dict):
                    continue
                meals = day.get("meals")
                if isinstance(meals, dict):
                    day["meals"] = [
                        {"type": k, "name": v} if isinstance(v, str)
                        else {"type": k, **(v if isinstance(v, dict) else {})}
                        for k, v in meals.items()
                    ]
        return data

    @staticmethod
    def _extract_json(text: str) -> Optional[dict]:
        try:
            return json.loads(text)
        except (json.JSONDecodeError, TypeError):
            pass
        fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
        if fenced:
            try:
                return json.loads(fenced.group(1))
            except json.JSONDecodeError:
                pass
        start, end = text.find("{"), text.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(text[start:end + 1])
            except json.JSONDecodeError:
                pass
        return None
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
配置管理
"""
from enum import Enum
from pydantic import BaseModel


class SearchAPI(str, Enum):
    TAVILY = "tavily"
    DUCKDUCKGO = "duckduckgo"
    PERPLEXITY = "perplexity"
    SEARXNG = "searxng"
    ADVANCED = "advanced"


class Configuration(BaseModel):
    search_api: SearchAPI = SearchAPI.TAVILY
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
搜索请求/响应 DTO
"""
from pydantic import BaseModel


class ResearchRequest(BaseModel):
    """研究请求"""
    topic: str
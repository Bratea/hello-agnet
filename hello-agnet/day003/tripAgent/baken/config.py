#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2026/8/10 18:00
# @Author  : 小陈
# @File    : config.py
# @Software: PyCharm
"""

import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(override=True)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=".env")
    amap_api_key: str = ""
    unsplash_access_key: str = ""

settings = Settings()

def get_settings() -> Settings:
    return settings

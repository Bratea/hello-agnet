#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
赛博小镇配置
"""
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(override=True)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=".env")

    HOST: str = "0.0.0.0"
    PORT: int = 8000
    NPC_STATUS_UPDATE_INTERVAL: int = 30  # 秒


settings = Settings()


def get_settings() -> Settings:
    return settings
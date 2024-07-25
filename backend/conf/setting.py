#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : settings.py
from functools import lru_cache

from pydantic import Field
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """
    配置
    """

    DEBUG: bool = Field(default=False, description="是否为开发模式")
    SERVER_NAME: str = Field(default="server", description="项目名")
    TOOL_NAME: str = Field(default="IT-XIAOBIN", description="工具名")
    EMAIL: str = Field(default="2274858959@qq.com", description="邮箱")
    AUTHOR: str = Field(default="XIAO BIN", description="作者")

    BASE_DIR: Path = Field(default=BASE_DIR, description="项目基础路径")

    VERSION: str = Field(default="0.1.0", description="版本号")
    # 日志
    LOG: dict = {"max_log_size": "20MB", "backup_count": 20}

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()

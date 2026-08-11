#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
对话日志系统 — 双输出：控制台 + 文件
"""
import logging
from datetime import datetime
from pathlib import Path


class DialogueLogger:
    """对话日志记录器"""

    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)

        today = datetime.now().strftime("%Y-%m-%d")
        log_file = self.log_dir / f"dialogue_{today}.log"

        self.logger = logging.getLogger("DialogueLogger")
        self.logger.setLevel(logging.INFO)

        # 避免重复添加 handler
        if not self.logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%H:%M:%S'
            )
            console_handler.setFormatter(console_formatter)

            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.INFO)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)

            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)

    def log_dialogue(self, npc_id: str, player_name: str,
                     player_message: str, npc_reply: str,
                     affinity_info: dict):
        """记录对话"""
        log_message = f"""
{'='*60}
NPC: {npc_id}
玩家: {player_name}
玩家消息: {player_message}
NPC回复: {npc_reply}
好感度: {affinity_info['level']} ({affinity_info['score']}/100)
互动次数: {affinity_info['interaction_count']}
{'='*60}
"""
        self.logger.info(log_message)

    def log_error(self, error_message: str):
        """记录错误"""
        self.logger.error(error_message)
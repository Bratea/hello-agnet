#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
赛博小镇路由 — FastAPI 端点（@RestController）
"""
import asyncio
import json
import logging
from typing import AsyncGenerator

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse

from agent.npc_agent import NPCAgentManager
from agent.batch_generator import NPCBatchGenerator
from tools.state_manager import StateManager
from tools.relationship_manager import RelationshipManager
from tools.logger import DialogueLogger
from model.dto.dialogue import (
    DialogueRequest, DialogueResponse, AffinityInfo, NPCStatusResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["cyber_town"])
godot_router = APIRouter(tags=["godot"])  # Godot 前端兼容路由（无 /api 前缀）

# 模块级单例
agent_manager = NPCAgentManager()
state_manager = StateManager()
relationship_manager = RelationshipManager()
dialogue_logger = DialogueLogger()
batch_generator = NPCBatchGenerator(agent_manager)

# 启动时初始化
agent_manager.initialize_npcs()
state_manager.initialize_npcs()
logger.info("✅ NPC Agents 和状态管理器已初始化")


async def background_dialogue_update():
    """后台任务：每 5 分钟更新一次 NPC 背景对话"""
    while True:
        try:
            dialogues = batch_generator.generate_batch_dialogues()
            for npc_name, dialogue in dialogues.items():
                state_manager.update_background_dialogue(npc_name, dialogue)
            logger.info(f"✅ 背景对话更新完成: {len(dialogues)}个NPC")
        except Exception as e:
            logger.error(f"❌ 背景对话更新失败: {e}")
        await asyncio.sleep(300)


# 启动后台对话更新
def start_background_tasks():
    """启动后台任务（由 main.py 在事件循环启动后调用）"""
    try:
        asyncio.create_task(background_dialogue_update())
        logger.info("✅ 后台对话更新任务已启动")
    except RuntimeError:
        logger.warning("⚠️ 无法启动后台任务（无事件循环）")


@router.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "running",
        "message": "赛博小镇后端服务正在运行",
        "npcs": state_manager.get_npc_count(),
    }


@router.get("/npcs/status")
async def get_npc_status():
    """获取所有 NPC 状态"""
    npcs = state_manager.get_all_npc_states()
    return {"npcs": [npc.model_dump() for npc in npcs]}


@router.get("/npcs/{npc_id}/status")
async def get_single_npc_status(npc_id: str):
    """获取单个 NPC 状态"""
    npc = state_manager.get_npc_state(npc_id)
    if not npc:
        raise HTTPException(status_code=404, detail=f"NPC {npc_id} 不存在")
    return npc.model_dump()


@router.post("/dialogue", response_model=DialogueResponse)
async def dialogue(request: DialogueRequest):
    """处理玩家与 NPC 的对话"""
    if not agent_manager.has_npc(request.npc_id):
        raise HTTPException(status_code=404, detail=f"NPC {request.npc_id} 不存在")

    if state_manager.is_npc_busy(request.npc_id):
        raise HTTPException(
            status_code=409,
            detail=f"NPC {request.npc_id} 正在与其他玩家对话",
        )

    state_manager.set_npc_busy(request.npc_id, True)

    try:
        affinity_info = relationship_manager.get_affinity(
            request.npc_id, request.player_name
        )

        agent = agent_manager.get_agent_with_affinity(
            request.npc_id, affinity_info.level
        )
        reply = agent.run(request.player_message)

        new_affinity = relationship_manager.update_affinity(
            request.npc_id, request.player_name, request.player_message, reply
        )

        dialogue_logger.log_dialogue(
            npc_id=request.npc_id,
            player_name=request.player_name,
            player_message=request.player_message,
            npc_reply=reply,
            affinity_info=new_affinity.model_dump(),
        )

        return DialogueResponse(
            npc_reply=reply,
            affinity_level=new_affinity.level,
            affinity_score=new_affinity.score,
        )

    except Exception as e:
        dialogue_logger.log_error(f"对话处理失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"对话处理失败: {str(e)}")

    finally:
        state_manager.set_npc_busy(request.npc_id, False)


@router.get("/affinity/{npc_id}/{player_name}", response_model=AffinityInfo)
async def get_affinity(npc_id: str, player_name: str = "玩家"):
    """获取玩家与 NPC 的好感度"""
    if not agent_manager.has_npc(npc_id):
        raise HTTPException(status_code=404, detail=f"NPC {npc_id} 不存在")

    affinity = relationship_manager.get_affinity(npc_id, player_name)
    return affinity


@router.get("/batch-dialogue")
async def get_batch_dialogue():
    """获取批量生成的 NPC 背景对话"""
    context = Query(None, description="场景上下文")
    try:
        dialogues = batch_generator.generate_batch_dialogues(context)
        return {"dialogues": dialogues}
    except Exception as e:
        logger.error(f"批量对话生成失败: {e}")
        raise HTTPException(status_code=500, detail="批量对话生成失败")


# ═══════════════════════════════════════════
# Godot 前端兼容路由（匹配 Godot 的 API 路径和格式）
# ═══════════════════════════════════════════

# NPC 名称 ↔ ID 映射
NPC_NAME_TO_ID = {
    "张三": "zhang_san",
    "李四": "li_si",
    "王五": "wang_wu",
}
NPC_ID_TO_NAME = {v: k for k, v in NPC_NAME_TO_ID.items()}


@godot_router.post("/chat")
async def godot_chat(data: dict):
    """Godot 前端对话接口"""
    npc_name = data.get("npc_name", "")
    message = data.get("message", "")
    npc_id = NPC_NAME_TO_ID.get(npc_name)

    if not npc_id:
        return {"success": False, "npc_name": npc_name, "message": "NPC不存在"}

    if state_manager.is_npc_busy(npc_id):
        return {"success": False, "npc_name": npc_name, "message": "该NPC正在忙"}

    state_manager.set_npc_busy(npc_id, True)
    try:
        affinity_info = relationship_manager.get_affinity(npc_id, "玩家")
        agent = agent_manager.get_agent_with_affinity(npc_id, affinity_info.level)
        reply = agent.run(message)

        new_affinity = relationship_manager.update_affinity(npc_id, "玩家", message, reply)

        dialogue_logger.log_dialogue(
            npc_id=npc_id, player_name="玩家",
            player_message=message, npc_reply=reply,
            affinity_info=new_affinity.model_dump(),
        )

        return {"success": True, "npc_name": npc_name, "message": reply}
    except Exception as e:
        dialogue_logger.log_error(f"对话处理失败: {e}")
        return {"success": False, "npc_name": npc_name, "message": "服务器内部错误"}
    finally:
        state_manager.set_npc_busy(npc_id, False)


@godot_router.get("/npcs")
async def godot_npc_list():
    """Godot 前端 NPC 列表"""
    npcs = []
    for npc_id, cfg in agent_manager.npc_configs.items():
        npc_state = state_manager.get_npc_state(npc_id)
        npcs.append({
            "name": cfg["name"],
            "title": cfg["role"],
            "position": {
                "x": npc_state.position.x if npc_state else 0,
                "y": npc_state.position.y if npc_state else 0,
            },
        })
    return {"npcs": npcs}


@godot_router.get("/npcs/status")
async def godot_npc_status():
    """Godot 前端 NPC 状态（背景对话）"""
    dialogues = {}
    for npc_id, cfg in agent_manager.npc_configs.items():
        npc_state = state_manager.get_npc_state(npc_id)
        dialogues[cfg["name"]] = npc_state.background_dialogue if npc_state else ""
    return {"dialogues": dialogues}
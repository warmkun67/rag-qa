# -*- coding: utf-8 -*-
"""对话持久化模块 —— JSON 文件存储，无数据库依赖"""

import os
import json
import uuid
from datetime import datetime

CONVERSATIONS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "conversations")


def _ensure_dir():
    """确保 conversations/ 目录存在"""
    os.makedirs(CONVERSATIONS_DIR, exist_ok=True)


def _conversation_path(conversation_id: str) -> str:
    """返回对话 JSON 文件的完整路径"""
    return os.path.join(CONVERSATIONS_DIR, f"{conversation_id}.json")


def generate_title(messages: list) -> str:
    """从第一条用户消息提取标题（截取前 30 个字符）"""
    for m in messages:
        if m.get("role") == "user":
            content = m.get("content", "").strip()
            if content:
                return content[:30] + ("..." if len(content) > 30 else "")
    return "新对话"


def save_conversation(conversation_id: str, messages: list):
    """保存/覆写一个对话到 JSON 文件"""
    if not messages:
        return
    _ensure_dir()
    path = _conversation_path(conversation_id)
    now = datetime.now().isoformat()

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        created_at = data.get("created_at", now)
    else:
        created_at = now

    data = {
        "id": conversation_id,
        "title": generate_title(messages),
        "created_at": created_at,
        "updated_at": now,
        "messages": messages,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_conversation(conversation_id: str) -> list:
    """加载对话，返回 messages 列表；文件不存在或损坏返回空列表"""
    path = _conversation_path(conversation_id)
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("messages", [])
    except (json.JSONDecodeError, KeyError):
        return []


def list_conversations() -> list[dict]:
    """列出所有对话摘要，按 updated_at 降序排列"""
    _ensure_dir()
    result = []
    for filename in os.listdir(CONVERSATIONS_DIR):
        if not filename.endswith(".json"):
            continue
        path = os.path.join(CONVERSATIONS_DIR, filename)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            result.append({
                "id": data.get("id", ""),
                "title": data.get("title", "未命名"),
                "created_at": data.get("created_at", ""),
                "updated_at": data.get("updated_at", ""),
                "message_count": len(data.get("messages", [])),
            })
        except (json.JSONDecodeError, KeyError):
            continue
    result.sort(key=lambda x: x["updated_at"], reverse=True)
    return result


def delete_conversation(conversation_id: str):
    """删除一个对话的 JSON 文件"""
    path = _conversation_path(conversation_id)
    if os.path.exists(path):
        os.remove(path)


def format_time(iso_str: str) -> str:
    """将 ISO 时间字符串格式化为友好显示：今天→HH:MM，今年→MM/DD，更早→YYYY/MM/DD"""
    if not iso_str:
        return ""
    dt = datetime.fromisoformat(iso_str)
    now = datetime.now()
    if dt.date() == now.date():
        return dt.strftime("%H:%M")
    elif dt.year == now.year:
        return dt.strftime("%m/%d")
    else:
        return dt.strftime("%Y/%m/%d")

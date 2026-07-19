# -*- coding: utf-8 -*-
"""
RAG项目全局配置
"""
import os
from dotenv import load_dotenv

load_dotenv()

# 大模型配置
LLM_MODEL = "deepseek-chat"
LLM_BASE_URL = "https://api.deepseek.com"

# API Key：优先从 Streamlit Secrets 读取（部署环境），否则从环境变量读取（本地）
try:
    import streamlit as st
    LLM_API_KEY = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
except Exception:
    LLM_API_KEY = os.getenv("OPENAI_API_KEY")

# 文档配置
DOCS_DIR = "./docs"
CHUNK_SIZE = 600
CHUNK_OVERLAP = 50

# 检索配置
TOP_K = 3

# 确保文档目录存在（部署时首次启动不会报错）
os.makedirs(DOCS_DIR, exist_ok=True)
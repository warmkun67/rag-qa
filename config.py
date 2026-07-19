# -*- coding: utf-8 -*-
"""
RAG项目全局配置
"""
import os
from dotenv import load_dotenv

load_dotenv()

# 大模型配置
LLM_MODEL = "deepseek-chat"
LLM_API_KEY = os.getenv("OPENAI_API_KEY")
LLM_BASE_URL = "https://api.deepseek.com"

# 文档配置
DOCS_DIR = "./docs"
CHUNK_SIZE = 600
CHUNK_OVERLAP = 50

# 检索配置
TOP_K = 3

# 确保文档目录存在（部署时首次启动不会报错）
os.makedirs(DOCS_DIR, exist_ok=True)
# -*- coding: utf-8 -*-
import sys
from rag_chain import build_rag_chain

# 强制 UTF-8 输出，防止 Windows cmd 下 emoji 报错
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

print("=" * 60)
print("    🔥 企业级 RAG 知识库问答系统 启动成功 🔥")
print("=" * 60)

rag = build_rag_chain()

while True:
    q = input("\n你：")
    if q in ["exit", "quit", "退出"]:
        print("👋 已退出")
        break
    try:
        ans = rag(q)
        print(f"\nAI：{ans}")
    except Exception as e:
        print(f"❌ 错误：{e}")
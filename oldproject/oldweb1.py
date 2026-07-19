# -*- coding: utf-8 -*-
import streamlit as st
import os
from dotenv import load_dotenv

# 加载配置
load_dotenv()
import config
from doc_loader import load_all_docs
from rag_chain import build_rag_chain

# 页面配置
st.set_page_config(page_title="RAG 智能问答系统", layout="wide")
st.title("📚 RAG 智能问答系统")

# 状态初始化
if "rag_chain" not in st.session_state:
    with st.spinner("📄 正在加载 docs 文件夹..."):
        st.session_state.rag_chain = build_rag_chain()
if "last_uploaded_file" not in st.session_state:
    st.session_state.last_uploaded_file = None
if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------- 左侧：文档管理 --------------------------
with st.sidebar:
    st.subheader("📁 文档管理")

    # 1. 上传文件
    uploaded_file = st.file_uploader("上传文件到 docs", type=["pdf", "txt"])
    if uploaded_file is not None:
        if st.session_state.last_uploaded_file != uploaded_file.name:
            save_path = os.path.join(config.DOCS_DIR, uploaded_file.name)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"✅ 已上传：{uploaded_file.name}")
            del st.session_state["rag_chain"]
            st.session_state.rag_chain = build_rag_chain()
            st.session_state.last_uploaded_file = uploaded_file.name

    # 2. 显示当前文件列表
    st.subheader("📂 当前文件")
    if os.path.exists(config.DOCS_DIR):
        files = os.listdir(config.DOCS_DIR)
        if files:
            for f in files:
                st.write(f"• {f}")
        else:
            st.warning("文件夹为空")
    else:
        os.makedirs(config.DOCS_DIR)

    # 3. 删除文件
    st.subheader("🗑️ 删除文件")
    del_file = st.selectbox("选择要删除的文件", files if files else [])
    if st.button("删除选中文件") and del_file:
        os.remove(os.path.join(config.DOCS_DIR, del_file))
        st.success(f"已删除：{del_file}")
        del st.session_state["rag_chain"]
        st.session_state.rag_chain = build_rag_chain()

    # 4. 清空对话
    if st.button("🧹 清空对话历史"):
        st.session_state.history = []
        st.rerun()

# -------------------------- 右侧：问答界面 --------------------------
# 显示历史对话
for q, a in st.session_state.history:
    with st.chat_message("user"):
        st.write(q)
    with st.chat_message("assistant"):
        st.write(a)

# 输入框
question = st.text_input("请输入你的问题：", key="user_question")

# 回答按钮
if st.button("🚀 开始回答") and question:
    with st.spinner("🤖 正在检索并生成答案..."):
        answer = st.session_state.rag_chain(question)
        
        # 保存历史
        st.session_state.history.append((question, answer))
        
        # 显示回答
        st.markdown("### 🤖 AI回答：")
        st.success(answer)
        
        # 显示引用来源
        st.markdown("---")
        st.caption("📄 参考来源：docs 文件夹内文档片段")
        
        # 复制按钮
        st.button("📋 复制答案", on_click=lambda: st.write(st.code(answer)))

st.markdown("<br><br><center>基于 RAG 检索增强生成 | 智能问答系统</center>", unsafe_allow_html=True)
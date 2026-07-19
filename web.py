# -*- coding: utf-8 -*-
import streamlit as st
import os
from dotenv import load_dotenv

# 加载环境
load_dotenv()
import config

# 最强缓存：只加载一次，速度起飞
@st.cache_resource(show_spinner="📄 正在加载文档...")
def get_rag_chain():
    from rag_chain import build_rag_chain
    return build_rag_chain()

# 页面初始化
st.set_page_config(page_title="RAG 智能问答系统", layout="wide")
st.title("📚 RAG 智能问答系统")

# 初始化状态
rag = get_rag_chain()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # 多轮对话历史
if "last_uploaded" not in st.session_state:
    st.session_state.last_uploaded = None

# ====================== 左侧边栏：文档管理 ======================
with st.sidebar:
    st.subheader("📁 文档管理")

    # 1. 上传文件
    uploaded_file = st.file_uploader("上传文件到 docs", type=["pdf", "txt", "docx", "md", "xlsx", "xls", "csv"])
    if uploaded_file is not None:
        if st.session_state.last_uploaded != uploaded_file.name:
            save_path = os.path.join(config.DOCS_DIR, uploaded_file.name)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"✅ 已上传：{uploaded_file.name}")
            st.session_state.last_uploaded = uploaded_file.name
            st.cache_resource.clear()
            st.rerun()

    # 2. 显示当前文件
    st.subheader("📂 当前文档")
    files = os.listdir(config.DOCS_DIR) if os.path.exists(config.DOCS_DIR) else []
    if files:
        for f in files:
            st.write(f"• {f}")
    else:
        st.warning("暂无文档")

    # 3. 删除文件
    st.subheader("🗑️ 删除文档")
    file_to_delete = st.selectbox("选择要删除的文件", files) if files else None
    if st.button("删除选中文件") and file_to_delete:
        os.remove(os.path.join(config.DOCS_DIR, file_to_delete))
        st.success(f"已删除：{file_to_delete}")
        st.cache_resource.clear()
        st.rerun()

    # 4. 清空对话历史
    if st.button("🧹 清空对话历史"):
        st.session_state.chat_history = []
        st.rerun()

# ====================== 右侧聊天区：多轮对话 ======================
# 显示历史对话
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.write(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.write(msg["content"])
            # 复制答案按钮
            st.code(msg["content"], language="text")
            st.caption("📄 参考来源：docs 文件夹内文档")

# 用户输入（聊天式输入，更丝滑）
user_question = st.chat_input("请输入你的问题...")
if user_question:
    # 显示用户问题
    with st.chat_message("user"):
        st.write(user_question)
    st.session_state.chat_history.append({"role": "user", "content": user_question})

    # 生成回答
    with st.chat_message("assistant"):
        with st.spinner("🤖 正在思考..."):
            answer = rag(user_question)
            st.write(answer)
            # 复制按钮+引用来源
            st.code(answer, language="text")
            st.caption("📄 参考来源：docs 文件夹内文档")
            # 保存到历史
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
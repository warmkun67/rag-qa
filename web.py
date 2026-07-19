# -*- coding: utf-8 -*-
import streamlit as st
import os
from dotenv import load_dotenv

# 加载环境
load_dotenv()
import config

# ====================== 密码验证 ======================
def get_password():
    """优先从 Streamlit Secrets 读取，否则从环境变量读取"""
    try:
        return st.secrets.get("APP_PASSWORD", os.getenv("APP_PASSWORD", ""))
    except Exception:
        return os.getenv("APP_PASSWORD", "")

APP_PASSWORD = get_password()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# set_page_config 必须在最前面调用
st.set_page_config(
    page_title="RAG 智能问答系统",
    page_icon="🔓" if st.session_state.authenticated else "🔒",
    layout="wide"
)

if not st.session_state.authenticated:
    st.markdown("""
    <div style="max-width:400px; margin:100px auto; text-align:center;">
        <p style="font-size:48px;">🔐</p>
        <h2>RAG 智能问答系统</h2>
        <p style="color:#9aa0a6;">请输入访问密码</p>
    </div>
    """, unsafe_allow_html=True)
    pwd = st.text_input("密码", type="password", placeholder="请输入密码...", label_visibility="collapsed")
    if st.button("验证", use_container_width=True):
        if pwd == APP_PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("❌ 密码错误")
    st.stop()

# ====================== 自定义 CSS ======================
st.markdown("""
<style>
    /* --- 全局字体与背景 --- */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Noto Sans SC', sans-serif;
    }

    /* --- 顶部标题栏 --- */
    .main-header {
        background: linear-gradient(135deg, #1a73e8 0%, #6c5ce7 100%);
        padding: 28px 40px;
        border-radius: 16px;
        margin-bottom: 24px;
        color: white;
        box-shadow: 0 4px 20px rgba(26,115,232,0.3);
    }
    .main-header h1 {
        margin: 0;
        font-size: 28px;
        font-weight: 700;
        color: white !important;
    }
    .main-header p {
        margin: 6px 0 0 0;
        font-size: 14px;
        opacity: 0.9;
        color: white !important;
    }

    /* --- 侧边栏 --- */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9ff 0%, #f0f2fc 100%);
    }
    [data-testid="stSidebar"] .stButton > button {
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.2s;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .sidebar-file-item {
        background: white;
        padding: 8px 12px;
        border-radius: 8px;
        margin: 4px 0;
        font-size: 13px;
        border-left: 3px solid #1a73e8;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }

    /* --- 聊天消息 --- */
    [data-testid="stChatMessage"] {
        border-radius: 14px !important;
        padding: 16px 20px !important;
        margin: 10px 0 !important;
    }
    [data-testid="stChatMessage"][aria-label*="user"] {
        background: #e8f0fe !important;
    }
    [data-testid="stChatMessage"][aria-label*="assistant"] {
        background: #ffffff !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid #e8eaed;
    }

    /* --- 复制区域 --- */
    .copy-box {
        position: relative;
        margin-top: 12px;
    }
    .copy-box summary {
        cursor: pointer;
        color: #5f6368;
        font-size: 12px;
        padding: 4px 0;
    }

    /* --- 底部 --- */
    .main-footer {
        text-align: center;
        color: #9aa0a6;
        font-size: 12px;
        padding: 20px 0 10px 0;
        border-top: 1px solid #e8eaed;
        margin-top: 40px;
    }

    /* --- 状态标签 --- */
    .doc-count-badge {
        display: inline-block;
        background: #1a73e8;
        color: white;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# ====================== 顶部标题栏 ======================
st.markdown("""
<div class="main-header">
    <h1>📚 RAG 智能问答系统</h1>
    <p>基于本地知识库 · 精准问答 · 支持多格式文档</p>
</div>
""", unsafe_allow_html=True)

# ====================== 缓存 ======================
@st.cache_resource(show_spinner="📄 正在加载文档...")
def get_rag_chain():
    from rag_chain import build_rag_chain
    return build_rag_chain()

# ====================== 初始化状态 ======================
rag = get_rag_chain()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_uploaded" not in st.session_state:
    st.session_state.last_uploaded = None

# ====================== 左侧边栏 ======================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=48)
    st.markdown("### ⚙️ 控制台")

    # --- 文档统计 ---
    files = os.listdir(config.DOCS_DIR) if os.path.exists(config.DOCS_DIR) else []
    col1, col2 = st.columns(2)
    col1.metric("📄 文档数", len(files))
    col2.metric("💬 对话轮", len(st.session_state.chat_history) // 2)

    st.divider()

    # --- 上传文件 ---
    st.markdown("#### 📤 上传文档")
    uploaded_file = st.file_uploader(
        "支持 PDF / DOCX / TXT / MD / XLSX / CSV",
        type=["pdf", "txt", "docx", "md", "xlsx", "xls", "csv"],
        label_visibility="collapsed"
    )
    if uploaded_file is not None:
        if st.session_state.last_uploaded != uploaded_file.name:
            save_path = os.path.join(config.DOCS_DIR, uploaded_file.name)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"✅ 已上传：{uploaded_file.name}")
            st.session_state.last_uploaded = uploaded_file.name
            st.cache_resource.clear()
            st.rerun()

    st.divider()

    # --- 当前文档列表 ---
    st.markdown("#### 📂 知识库文档")
    if files:
        for f in files:
            st.markdown(f'<div class="sidebar-file-item">📎 {f}</div>', unsafe_allow_html=True)
    else:
        st.info("暂无文档，请上传")

    st.divider()

    # --- 管理操作 ---
    st.markdown("#### 🛠️ 管理")
    if files:
        file_to_delete = st.selectbox("选择要删除的文件", files, label_visibility="collapsed")
        if st.button("🗑️ 删除选中文件", use_container_width=True):
            os.remove(os.path.join(config.DOCS_DIR, file_to_delete))
            st.success(f"已删除：{file_to_delete}")
            st.cache_resource.clear()
            st.rerun()

    if st.button("🧹 清空对话历史", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# ====================== 右侧聊天区 ======================
# 空状态引导
if len(st.session_state.chat_history) == 0:
    st.markdown("""
    <div style="text-align:center; padding:60px 0; color:#9aa0a6;">
        <p style="font-size:48px; margin:0;">💡</p>
        <p style="font-size:18px; font-weight:500; margin:12px 0;">上传文档，开始提问</p>
        <p style="font-size:14px;">在左侧上传你的文档，然后输入问题开始智能问答</p>
    </div>
    """, unsafe_allow_html=True)

# 显示历史对话
for i, msg in enumerate(st.session_state.chat_history):
    if msg["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.write(msg["content"])
    else:
        with st.chat_message("assistant", avatar="🤖"):
            st.write(msg["content"])
            with st.expander("📋 复制答案"):
                st.code(msg["content"], language=None)

# 用户输入
user_question = st.chat_input("💬 输入你的问题，按回车发送...")
if user_question:
    # 显示用户消息
    with st.chat_message("user", avatar="👤"):
        st.write(user_question)
    st.session_state.chat_history.append({"role": "user", "content": user_question})

    # 生成回答
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("🤔 正在分析文档内容..."):
            answer = rag(user_question)
            st.write(answer)
            with st.expander("📋 复制答案"):
                st.code(answer, language=None)
            st.caption("📄 回答基于知识库文档内容")
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

# ====================== 底部 ======================
st.markdown("""
<div class="main-footer">
    RAG 智能问答系统 · Powered by DeepSeek AI
</div>
""", unsafe_allow_html=True)

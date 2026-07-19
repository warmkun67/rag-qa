# -*- coding: utf-8 -*-
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()
import config

# ====================== 密码验证 ======================
def get_password():
    try:
        return st.secrets.get("APP_PASSWORD", os.getenv("APP_PASSWORD", ""))
    except Exception:
        return os.getenv("APP_PASSWORD", "")

APP_PASSWORD = get_password()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

st.set_page_config(
    page_title="RAG 智能问答系统",
    page_icon="🔓" if st.session_state.authenticated else "🔒",
    layout="wide"
)

# --- 登录页 ---
if not st.session_state.authenticated:
    st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(160deg, #f5f3f0 0%, #e8e6e1 100%);
        }
        .login-card {
            max-width: 400px;
            margin: 120px auto 0 auto;
            background: white;
            padding: 48px 40px;
            border-radius: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 8px 30px rgba(0,0,0,0.04);
            text-align: center;
        }
        .login-card .icon { font-size: 48px; margin-bottom: 8px; }
        .login-card h2 { font-size: 22px; font-weight: 600; color: #1e1b4b; margin: 0 0 6px 0; }
        .login-card .sub { font-size: 14px; color: #8b8a91; margin-bottom: 28px; }
    </style>
    <div class="login-card">
        <div class="icon">🔐</div>
        <h2>知识库问答系统</h2>
        <p class="sub">请输入访问密码</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([0.28, 0.44, 0.28])
    with col2:
        pwd = st.text_input("密码", type="password", placeholder="请输入密码...", label_visibility="collapsed")
        if st.button("验证身份", use_container_width=True):
            if pwd == APP_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("密码错误")
    st.stop()

# ====================== 全局样式 ======================
st.markdown("""
<style>
    /* === 基础 === */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', 'Noto Sans SC', -apple-system, sans-serif;
    }
    body { color: #334155; }

    /* 隐藏默认顶栏 */
    [data-testid="stHeader"] { display: none; }
    [data-testid="stToolbar"] { display: none; }

    /* === 主背景 === */
    [data-testid="stAppViewContainer"] > .main {
        background: #fafaf8;
    }

    /* === 页眉 === */
    .app-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 18px 32px;
        margin-bottom: 8px;
    }
    .app-header .brand {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .app-header .brand .logo {
        width: 38px; height: 38px;
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        font-size: 20px;
    }
    .app-header .brand h1 {
        font-size: 18px; font-weight: 600; color: #1e1b4b; margin: 0;
    }
    .app-header .badge {
        font-size: 11px; color: #8b8a91;
        background: #f1f0ec; padding: 4px 12px; border-radius: 20px;
    }

    /* === 侧边栏 === */
    [data-testid="stSidebar"] {
        background: white;
        border-right: 1px solid #f0efe9;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h4 {
        font-size: 12px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #8b8a91 !important;
        margin-top: 24px;
        margin-bottom: 8px;
    }
    [data-testid="stSidebar"] .stButton > button {
        border-radius: 10px;
        font-size: 13px;
        font-weight: 500;
        transition: all 0.15s;
        border: 1px solid #e5e3de;
        background: white;
        color: #334155;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        border-color: #d4d1c8;
        background: #fafaf8;
    }
    [data-testid="stSidebar"] .stButton > button:has-text("删除") {
        color: #dc2626;
        border-color: #fecaca;
    }
    [data-testid="stSidebar"] .stButton > button:has-text("删除"):hover {
        background: #fef2f2;
    }

    /* === 文档卡片 === */
    .doc-card {
        background: #fafaf8;
        padding: 10px 14px;
        border-radius: 10px;
        margin: 4px 0;
        font-size: 13px;
        color: #334155;
        display: flex;
        align-items: center;
        gap: 8px;
        border: 1px solid transparent;
        transition: all 0.15s;
    }
    .doc-card:hover {
        background: white;
        border-color: #e5e3de;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }
    .doc-card .file-icon { font-size: 16px; flex-shrink: 0; }

    /* === 统计卡片 === */
    .stat-card {
        background: #fafaf8;
        border-radius: 12px;
        padding: 14px 12px;
        text-align: center;
        border: 1px solid #f0efe9;
    }
    .stat-card .stat-num {
        font-size: 22px; font-weight: 700; color: #4f46e5; line-height: 1.2;
    }
    .stat-card .stat-label {
        font-size: 11px; color: #8b8a91; margin-top: 2px;
    }

    /* === 聊天主区域 === */
    .chat-container {
        max-width: 780px;
        margin: 0 auto;
    }

    /* === 聊天气泡 === */
    [data-testid="stChatMessage"] {
        border-radius: 16px !important;
        padding: 14px 20px !important;
        margin: 6px 0 !important;
    }
    [data-testid="stChatMessage"][data-testid="stChatMessage"] {
        background: white !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        border: 1px solid #f0efe9;
    }

    /* === 空状态 === */
    .empty-state {
        text-align: center;
        padding: 80px 20px;
    }
    .empty-state .empty-icon {
        width: 64px; height: 64px;
        margin: 0 auto 20px auto;
        background: #f0efee;
        border-radius: 20px;
        display: flex; align-items: center; justify-content: center;
        font-size: 28px;
    }
    .empty-state h3 { font-size: 18px; font-weight: 600; color: #1e1b4b; margin: 0 0 6px 0; }
    .empty-state p { font-size: 14px; color: #8b8a91; margin: 0; }

    /* === 输入框 === */
    [data-testid="stChatInput"] textarea {
        border-radius: 14px !important;
        border: 2px solid #e5e3de !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
        transition: border-color 0.15s;
    }
    [data-testid="stChatInput"] textarea:focus {
        border-color: #4f46e5 !important;
        box-shadow: 0 0 0 3px rgba(79,70,229,0.08) !important;
    }

    /* === 展开区 === */
    .stExpander {
        border: none !important;
        background: transparent !important;
    }
    .stExpander summary {
        font-size: 12px !important;
        color: #8b8a91 !important;
    }

    /* === 页脚 === */
    .app-footer {
        text-align: center;
        padding: 32px 0 16px 0;
        font-size: 12px;
        color: #c4c1ba;
    }

    /* === 上传区 === */
    [data-testid="stFileUploader"] {
        border-radius: 12px !important;
        border: 2px dashed #e5e3de !important;
        background: #fafaf8 !important;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #4f46e5 !important;
        background: #f5f3ff !important;
    }
</style>
""", unsafe_allow_html=True)

# ====================== 侧边栏 ======================
with st.sidebar:
    # 品牌
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;padding:4px 0 20px 0;">
        <div style="width:34px;height:34px;background:linear-gradient(135deg,#4f46e5,#7c3aed);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:18px;">⚡</div>
        <div>
            <div style="font-size:15px;font-weight:600;color:#1e1b4b;line-height:1.2;">知识库问答</div>
            <div style="font-size:11px;color:#8b8a91;">Powered by DeepSeek</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 统计
    files = os.listdir(config.DOCS_DIR) if os.path.exists(config.DOCS_DIR) else []
    st.markdown(f"""
    <div style="display:flex;gap:8px;">
        <div class="stat-card" style="flex:1;">
            <div class="stat-num">{len(files)}</div>
            <div class="stat-label">📄 文档</div>
        </div>
        <div class="stat-card" style="flex:1;">
            <div class="stat-num">{len(st.session_state.chat_history) // 2}</div>
            <div class="stat-label">💬 对话</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # 上传
    st.markdown("##### 📤 上传文档")
    uploaded_file = st.file_uploader(
        "支持 PDF / DOCX / TXT / MD / XLSX / CSV",
        type=["pdf", "txt", "docx", "md", "xlsx", "xls", "csv"],
        label_visibility="collapsed"
    )
    if uploaded_file is not None and st.session_state.last_uploaded != uploaded_file.name:
        save_path = os.path.join(config.DOCS_DIR, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"已上传 {uploaded_file.name}")
        st.session_state.last_uploaded = uploaded_file.name
        st.cache_resource.clear()
        st.rerun()

    # 文档列表
    st.markdown("##### 📂 知识库")
    if files:
        icon_map = {
            ".pdf": "📕", ".docx": "📘", ".doc": "📘",
            ".txt": "📄", ".md": "📝",
            ".xlsx": "📊", ".xls": "📊", ".csv": "📋"
        }
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            icon = icon_map.get(ext, "📎")
            st.markdown(f'<div class="doc-card"><span class="file-icon">{icon}</span>{f}</div>', unsafe_allow_html=True)
    else:
        st.caption("暂无文档，上传后即可开始问答")

    st.markdown("<br>", unsafe_allow_html=True)

    # 管理
    st.markdown("##### ⚙️ 管理")
    if files:
        file_to_delete = st.selectbox("选择要删除的文件", files, label_visibility="collapsed", key="del_select")
        if st.button("🗑️ 删除选中文件", use_container_width=True):
            os.remove(os.path.join(config.DOCS_DIR, file_to_delete))
            st.cache_resource.clear()
            st.rerun()

    if st.button("🧹 清空对话历史", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# ====================== 缓存 ======================
@st.cache_resource(show_spinner="📄 正在加载文档...")
def get_rag_chain():
    from rag_chain import build_rag_chain
    return build_rag_chain()

rag = get_rag_chain()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_uploaded" not in st.session_state:
    st.session_state.last_uploaded = None

# ====================== 主聊天区 ======================
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# --- 空状态 ---
if len(st.session_state.chat_history) == 0:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">💡</div>
        <h3>准备开始</h3>
        <p>在左侧上传知识文档，然后输入你的问题</p>
    </div>
    """, unsafe_allow_html=True)

# --- 对话历史 ---
for msg in st.session_state.chat_history:
    avatar = "🧑" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])
        if msg["role"] == "assistant":
            with st.expander("📋 复制答案"):
                st.code(msg["content"], language=None)

# --- 输入 ---
if user_question := st.chat_input("输入问题，按回车发送..."):
    with st.chat_message("user", avatar="🧑"):
        st.write(user_question)
    st.session_state.chat_history.append({"role": "user", "content": user_question})

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("正在分析文档..."):
            answer = rag(user_question)
            st.write(answer)
            with st.expander("📋 复制答案"):
                st.code(answer, language=None)
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

st.markdown('</div>', unsafe_allow_html=True)

# --- 页脚 ---
st.markdown('<div class="app-footer">RAG 智能问答系统 · Powered by DeepSeek AI</div>', unsafe_allow_html=True)

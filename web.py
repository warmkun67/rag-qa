# -*- coding: utf-8 -*-
import streamlit as st

# === set_page_config 必须是第一条 Streamlit 命令 ===
st.set_page_config(
    page_title="RAG 智能问答系统",
    page_icon="🔒",
    layout="wide"
)

import os
from dotenv import load_dotenv

load_dotenv()
import config

# ====================== 密码验证 ======================
def get_password():
    """Streamlit Secrets 优先，环境变量兜底"""
    try:
        return st.secrets.get("APP_PASSWORD", os.getenv("APP_PASSWORD", ""))
    except Exception:
        return os.getenv("APP_PASSWORD", "")

APP_PASSWORD = get_password()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# --- 登录页 ---
if not st.session_state.authenticated:
    st.markdown("""
    <style>
        /* 全屏登录遮罩——覆盖整个页面包括侧边栏 */
        .login-overlay {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            z-index: 9999;
            background: linear-gradient(160deg, #f0ede8 0%, #e3dfd8 50%, #ece8e2 100%);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }
        /* 装饰光斑 */
        .bg-orb {
            position: fixed;
            border-radius: 50%;
            filter: blur(80px);
            opacity: 0.5;
            pointer-events: none;
            z-index: 0;
        }
        .bg-orb.orb-1 {
            width: 320px; height: 320px;
            background: radial-gradient(circle, rgba(79,70,229,0.15) 0%, transparent 70%);
            top: -80px; right: -60px;
        }
        .bg-orb.orb-2 {
            width: 260px; height: 260px;
            background: radial-gradient(circle, rgba(124,58,237,0.12) 0%, transparent 70%);
            bottom: -60px; left: -40px;
        }
        .bg-orb.orb-3 {
            width: 200px; height: 200px;
            background: radial-gradient(circle, rgba(245,158,11,0.10) 0%, transparent 70%);
            top: 50%; left: 50%;
            transform: translate(-50%, -50%);
        }
        .login-card-full {
            width: 400px;
            background: rgba(255,255,255,0.85);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            padding: 48px 40px 36px 40px;
            border-radius: 20px;
            border: 1px solid rgba(255,255,255,0.8);
            box-shadow: 0 2px 8px rgba(0,0,0,0.04), 0 16px 40px rgba(0,0,0,0.06);
            text-align: center;
            position: relative;
            z-index: 1;
        }
        .login-card-full .icon-wrap {
            display: inline-flex;
            align-items: center; justify-content: center;
            width: 72px; height: 72px;
            border-radius: 50%;
            background: linear-gradient(135deg, rgba(79,70,229,0.08) 0%, rgba(124,58,237,0.06) 100%);
            margin-bottom: 16px;
            box-shadow: 0 0 0 8px rgba(79,70,229,0.04);
        }
        .login-card-full .icon-wrap .icon { font-size: 32px; }
        .login-card-full h2 { font-size: 22px; font-weight: 600; color: #1e1b4b; margin: 0 0 8px 0; }
        .login-card-full .divider {
            width: 32px; height: 3px;
            background: linear-gradient(90deg, #4f46e5, #7c3aed);
            border-radius: 2px;
            margin: 0 auto 24px auto;
            opacity: 0.5;
        }
    </style>
    <div class="login-overlay">
        <div class="bg-orb orb-1"></div>
        <div class="bg-orb orb-2"></div>
        <div class="bg-orb orb-3"></div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([0.28, 0.44, 0.28])
    with col2:
        st.markdown("""
        <div class="login-card-full">
            <div class="icon-wrap"><span class="icon">🔐</span></div>
            <h2>知识库问答系统</h2>
            <div class="divider"></div>
        """, unsafe_allow_html=True)
        pwd = st.text_input("密码", type="password", placeholder="请输入访问密码...", label_visibility="collapsed")
        if st.button("🔐 验证身份", use_container_width=True):
            if pwd == APP_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("密码错误，请重试")
        st.markdown('</div>', unsafe_allow_html=True)  <!-- 闭合 login-card-full -->
    st.markdown('</div>', unsafe_allow_html=True)      <!-- 闭合 login-overlay -->
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

    /* === 主背景 + 纹理 === */
    [data-testid="stAppViewContainer"] > .main {
        background-color: #fafaf8;
        background-image:
            radial-gradient(circle, #e8e6e1 1px, transparent 1px);
        background-size: 24px 24px;
    }

    /* === 侧边栏 === */
    [data-testid="stSidebar"] {
        background: #f7f6f3;
        border-right: 1px solid #edece7;
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
        background: white;
        padding: 10px 14px;
        border-radius: 10px;
        margin: 4px 0;
        font-size: 13px;
        color: #334155;
        display: flex;
        align-items: center;
        gap: 8px;
        border: 1px solid #edece7;
        transition: all 0.2s;
    }
    .doc-card:hover {
        border-color: #d4d1c8;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transform: translateX(2px);
    }
    .doc-card .file-icon { font-size: 16px; flex-shrink: 0; }

    /* === 统计卡片 === */
    .stat-card {
        background: white;
        border-radius: 12px;
        padding: 14px 12px;
        text-align: center;
        border: 1px solid #edece7;
        transition: all 0.2s;
        cursor: default;
    }
    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
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
        margin: 8px 0 !important;
    }
    [data-testid="stChatMessage"][data-testid="stChatMessage"] {
        background: white !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        border: 1px solid #f0efe9;
    }
    /* 用户消息：左侧靛蓝色条 */
    [data-testid="stChatMessage"][data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatar"]):not(:has([aria-label="assistant"])) {
        border-left: 3px solid #4f46e5 !important;
    }
    /* 用户消息靠右，AI消息靠左（通过 container 属性） */
    /* Streamlit 通过 flex-direction 控制左右，这里用 CSS 增强 */
    .stChatMessage [data-testid="stChatMessageAvatar"] {
        font-size: 20px;
    }

    /* === 空状态 === */
    .welcome-card {
        text-align: center;
        padding: 40px 32px;
        margin: 40px 0;
        background: white;
        border-radius: 20px;
        border: 1px solid #edece7;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03), 0 8px 24px rgba(0,0,0,0.04);
    }
    .welcome-card .welcome-icon {
        width: 72px; height: 72px;
        margin: 0 auto 20px auto;
        background: linear-gradient(135deg, rgba(79,70,229,0.08) 0%, rgba(124,58,237,0.06) 100%);
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 32px;
        box-shadow: 0 0 0 8px rgba(79,70,229,0.04);
    }
    .welcome-card h3 { font-size: 20px; font-weight: 600; color: #1e1b4b; margin: 0 0 8px 0; }
    .welcome-card .welcome-desc { font-size: 14px; color: #8b8a91; margin: 0 0 24px 0; line-height: 1.6; }
    .welcome-card .feature-tags {
        display: flex; gap: 10px; justify-content: center; flex-wrap: wrap;
    }
    .welcome-card .feature-tag {
        font-size: 12px; color: #6d6a81;
        background: #f7f6f3;
        border: 1px solid #edece7;
        padding: 6px 14px; border-radius: 20px;
        display: inline-flex; align-items: center; gap: 5px;
    }

    /* === 输入框 === */
    [data-testid="stChatInput"] textarea {
        border-radius: 14px !important;
        border: 2px solid #e5e3de !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
        transition: all 0.2s;
        background: white !important;
    }
    [data-testid="stChatInput"] textarea:focus {
        border-color: #4f46e5 !important;
        box-shadow: 0 0 0 4px rgba(79,70,229,0.10), 0 2px 12px rgba(79,70,229,0.08) !important;
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
        border: 2px dashed #d4d1c8 !important;
        background: white !important;
        transition: all 0.2s;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #4f46e5 !important;
        background: #f5f3ff !important;
    }
</style>
""", unsafe_allow_html=True)

# ====================== 缓存与状态初始化 ======================
@st.cache_resource
def get_rag_chain():
    from rag_chain import build_rag_chain
    return build_rag_chain()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_uploaded" not in st.session_state:
    st.session_state.last_uploaded = None

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

# ====================== 主聊天区 ======================
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# --- 空状态 ---
if len(st.session_state.chat_history) == 0:
    st.markdown("""
    <div class="welcome-card">
        <div class="welcome-icon">✨</div>
        <h3>欢迎使用知识库问答</h3>
        <p class="welcome-desc">上传文档到左侧知识库，然后用自然语言提问<br>AI 将基于你的文档内容精准回答</p>
        <div class="feature-tags">
            <span class="feature-tag">📕 PDF</span>
            <span class="feature-tag">📘 Word</span>
            <span class="feature-tag">📊 Excel</span>
            <span class="feature-tag">📝 Markdown</span>
            <span class="feature-tag">📄 TXT/CSV</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 对话历史 ---
for msg in st.session_state.chat_history:
    avatar = "⭐" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])
        if msg["role"] == "assistant":
            with st.expander("📋 复制答案"):
                st.code(msg["content"], language=None)

# --- 输入 ---
if user_question := st.chat_input("输入问题，按回车发送..."):
    with st.chat_message("user", avatar="⭐"):
        st.write(user_question)
    st.session_state.chat_history.append({"role": "user", "content": user_question})

    with st.chat_message("assistant", avatar="🤖"):
        rag = get_rag_chain()  # 首次加载文档（秒级），后续走缓存
        with st.spinner("🤔 正在分析文档..."):
            answer = rag(user_question)
            st.write(answer)
            with st.expander("📋 复制答案"):
                st.code(answer, language=None)
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

st.markdown('</div>', unsafe_allow_html=True)

# --- 页脚 ---
st.markdown('<div class="app-footer">RAG 智能问答系统 · Powered by DeepSeek AI</div>', unsafe_allow_html=True)

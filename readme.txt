以下是根据你的项目代码和文件结构编写的 **README.md** 文档。它涵盖了项目介绍、功能特性、技术栈、快速开始、使用说明、打包部署以及常见问题，适合直接放在 GitHub 上。

```markdown
# 📚 RAG 智能问答系统

基于 LangChain + Streamlit 构建的企业级文档问答系统。支持上传 PDF、Word、Excel、Markdown、TXT 等多种格式文档，自动提取文本并使用大模型（DeepSeek / OpenAI 兼容）生成精准答案。创新性地采用 **全量上下文策略**，在小规模知识库场景下实现 100% 信息覆盖，彻底杜绝检索遗漏问题。

## ✨ 功能特性

- 📄 **多格式文档支持**：PDF、DOCX、TXT、Markdown、Excel（.xlsx/.xls）、CSV
- 🔍 **全量上下文 RAG**：放弃向量检索，直接将所有文档内容送入大模型，保证答案完整
- 💬 **多轮对话历史**：保留聊天记录，支持连续提问
- 🗂️ **文档管理**：Web 界面内上传、删除文档，自动重建索引
- 🚀 **高性能缓存**：Streamlit 缓存机制，文档仅加载一次，问答响应迅速
- 🖥️ **双模式交互**：Web 图形界面（Streamlit） + 命令行终端（CLI）
- 📦 **一键打包**：使用 PyInstaller 打包为 Windows 可执行文件，无需 Python 环境

## 🛠️ 技术栈

| 类别 | 技术 |
|------|------|
| 核心框架 | LangChain, Streamlit |
| 大模型 API | DeepSeek（兼容 OpenAI API） |
| 文档解析 | PyPDF, python-docx, pandas, openpyxl, Unstructured |
| 文本分割 | RecursiveCharacterTextSplitter |
| 环境管理 | python-dotenv |
| 打包工具 | PyInstaller |

## 📁 项目结构

```
RAG_QA_System/
├── docs/                     # 上传的文档存放目录（自动创建）
├── .env                      # 环境变量（API Key）
├── config.py                 # 全局配置
├── doc_loader.py             # 文档加载与分块
├── rag_chain.py              # RAG 链构建（全量上下文）
├── web.py                    # Streamlit Web 界面（主程序）
├── main.py                   # 命令行交互版本
├── requirements.txt          # Python 依赖
├── run.bat                   # 启动 CLI 版（Windows）
├── run_web.bat               # 启动 Web 版（Windows）
├── build.bat                 # 打包脚本
└── RAG_QA_System.spec        # PyInstaller 配置文件
```

## 🚀 快速开始

### 1. 克隆项目并安装依赖

```bash
git clone https://github.com/yourname/RAG_QA_System.git
cd RAG_QA_System
pip install -r requirements.txt
```

### 2. 配置 API 密钥

在项目根目录创建 `.env` 文件（或复制 `.env.example`）：

```
OPENAI_API_KEY=your_deepseek_api_key_here
```

> 本系统使用 DeepSeek API（兼容 OpenAI 接口）。如需使用其他模型，请修改 `config.py` 中的 `LLM_BASE_URL` 和 `LLM_MODEL`。

### 3. 准备文档

在项目根目录下创建 `docs` 文件夹，将你的知识文档（PDF、DOCX、TXT 等）放入其中。

### 4. 运行应用

#### 启动 Web 界面（推荐）

```bash
streamlit run web.py
```

或直接双击 `run_web.bat`。

#### 启动命令行版本

```bash
python main.py
```

或双击 `run.bat`。

### 5. 使用

- 打开浏览器访问 `http://localhost:8501`
- 左侧边栏上传/删除文档
- 右侧聊天框输入问题，系统将基于全部文档内容回答
- 支持多轮对话，可随时清空历史

## 📦 打包为独立 EXE（Windows）

项目已配置 PyInstaller，可打包为单文件可执行程序，无需安装 Python 环境。

```bash
# 安装 PyInstaller（如未安装）
pip install pyinstaller

# 执行打包脚本
build.bat
```

打包完成后，可执行文件位于 `dist/RAG_QA_System.exe`，双击即可运行（首次启动稍慢）。

> 注意：打包时会包含 Python 解释器和所有依赖，文件体积约 150~200 MB。

## 🧠 核心设计说明

### 全量上下文策略

传统 RAG 需要将文档分块、向量化、检索 Top-K 片段，存在信息遗漏风险。本项目针对**小规模文档库**（总字符数 ≤ 大模型上下文窗口）采用**暴力但可靠**的方案：

1. 加载所有文档 → 分块（保留元数据）
2. 将**所有块拼接**为一个超大上下文
3. 每次提问时，将完整上下文 + 问题填入提示词，直接调用 LLM

**优点**：100% 信息覆盖，实现简单，无需调优检索参数。  
**限制**：文档总大小不能超过模型的上下文限制（DeepSeek 支持 64K token，约 5~10 万字中文）。

### 文档加载兼容性

- PDF：按页提取文本
- DOCX：优先 `Docx2txtLoader`，失败则回退 `python-docx` 读取段落
- Excel/CSV：使用 `pandas` 转换为文本表格
- TXT/MD：直接读取

### 缓存与性能优化

- `@st.cache_resource` 缓存 RAG 链构建过程，文档仅加载一次
- 上传/删除文档时清除缓存并自动刷新，实现热更新

## ❓ 常见问题

**Q：上传文档后为什么没有立即生效？**  
A：上传或删除文档后，系统会自动清除缓存并刷新页面，稍等片刻即可。如果仍不生效，请手动刷新浏览器。

**Q：提示“上下文过长”或 API 返回错误？**  
A：表示 `docs` 文件夹内文档总大小超过了模型上下文窗口。请减少文档数量或改用传统检索式 RAG（可参考项目中的 `rag_chain_retrieval.py` 示例）。

**Q：如何修改分块大小？**  
A：编辑 `config.py` 中的 `CHUNK_SIZE` 和 `CHUNK_OVERLAP`。

**Q：支持哪些大模型？**  
A：任何兼容 OpenAI API 的模型均可，只需修改 `config.py` 中的 `LLM_BASE_URL`、`LLM_MODEL` 和 `.env` 中的 API Key。

**Q：打包后的 EXE 报毒？**  
A：PyInstaller 打包的单文件常被部分杀毒软件误报。添加信任即可，代码完全开源可审查。

## 📄 许可证

MIT License

## 🙏 致谢

- [LangChain](https://www.langchain.com/)
- [Streamlit](https://streamlit.io/)
- [DeepSeek](https://deepseek.com/)

## 📬 联系方式

如有问题或建议，欢迎提交 Issue 或联系 [your-email@example.com]。
```


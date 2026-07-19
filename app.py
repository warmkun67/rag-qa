# -*- coding: utf-8 -*-
"""
RAG系统 最终稳定版（支持PDF / TXT / DOCX / Excel）
"""
import os
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 强制 UTF-8 输出，防止 Windows cmd 下 emoji 报错
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# 加载环境变量
load_dotenv()

# 配置模型
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.deepseek.com",
    temperature=0
)

# ------------------------------
# 【全格式文档加载】支持 PDF / TXT / DOCX / XLSX / CSV
# ------------------------------
def load_all_files():
    full_text = ""

    if not os.path.exists("docs"):
        return full_text

    for filename in os.listdir("docs"):
        path = os.path.join("docs", filename)

        try:
            # TXT
            if filename.endswith(".txt"):
                with open(path, "r", encoding="utf-8") as f:
                    full_text += f.read() + "\n\n"

            # PDF
            elif filename.endswith(".pdf"):
                from langchain_community.document_loaders import PyPDFLoader
                loader = PyPDFLoader(path)
                pages = loader.load()
                for page in pages:
                    full_text += page.page_content + "\n\n"

            # WORD DOCX
            elif filename.endswith(".docx"):
                from docx import Document
                doc = Document(path)
                text = "\n".join([para.text for para in doc.paragraphs])
                full_text += text + "\n\n"

            # EXCEL
            elif filename.endswith((".xlsx", ".xls", ".csv")):
                import pandas as pd
                if filename.endswith(".csv"):
                    df = pd.read_csv(path)
                else:
                    df = pd.read_excel(path)
                full_text += df.to_string(index=False) + "\n\n"

        except Exception as e:
            print(f"⚠️  跳过文件 {filename}：{str(e)}")

    return full_text

# 加载并分块
def load_and_split_docs():
    all_text = load_all_files()
    if not all_text.strip():
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    splits = splitter.split_text(all_text)
    return splits

# ------------------------------
# 主程序
# ------------------------------
if __name__ == "__main__":
    print("=" * 50)
    print("  企业级RAG问答系统 启动成功")
    print("=" * 50)
    print("提示：输入exit退出程序\n")

    if not os.path.exists("docs"):
        os.mkdir("docs")
        print("已创建docs文件夹，请放入文档")
        exit()

    splits = load_and_split_docs()
    print(f"✅ 已加载文档，共 {len(splits)} 个片段\n")

    if len(splits) == 0:
        print("❌ 文档为空，请检查 docs 文件夹")
        exit()

    # 问答循环
    while True:
        question = input("请输入你的问题：")
        if question.lower() in ["exit", "quit"]:
            print("程序退出")
            break

        # 上下文：取全部片段（保证不会漏内容）
        context = "\n\n".join(splits)
        prompt = f"""你是一个文档问答助手，请根据以下上下文回答用户的问题。
如果无法回答，就说"根据文档无法回答"，不要编造内容。

上下文：{context}
问题：{question}
回答："""

        # 调用模型
        response = llm.invoke(prompt)
        print(f"\n回答：{response.content}\n")
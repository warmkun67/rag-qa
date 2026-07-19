# -*- coding: utf-8 -*-
import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import config

def load_all_docs():
    """
    自动加载 docs 文件夹下 所有 PDF / TXT / MD
    丢文件就生效，不用改代码
    """
    doc_path = config.DOCS_DIR
    all_splits = []

    # 遍历所有文件
    for filename in os.listdir(doc_path):
        full_path = os.path.join(doc_path, filename)

        # PDF
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(full_path)
            docs = loader.load()
            print(f"✅ 加载PDF：{filename}")

        # TXT
        elif filename.endswith(".txt"):
            loader = TextLoader(full_path, encoding="utf-8")
            docs = loader.load()
            print(f"✅ 加载TXT：{filename}")

        # MD
        elif filename.endswith(".md"):
            loader = UnstructuredMarkdownLoader(full_path)
            docs = loader.load()
            print(f"✅ 加载MD：{filename}")

        else:
            continue

        # 分块
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
            separators=["\n\n", "\n", "。", "！", "？", " "]
        )
        splits = splitter.split_documents(docs)
        all_splits.extend(splits)

    print(f"\n📄 总文档片段数：{len(all_splits)}")
    return all_splits
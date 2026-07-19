@echo off
chcp 65001 >nul
pyinstaller --windowed --name RAG_QA_System ^
--hidden-import=streamlit ^
--hidden-import=langchain ^
--hidden-import=langchain_openai ^
--hidden-import=pypdf ^
--hidden-import=python_docx ^
--hidden-import=pandas ^
--hidden-import=openpyxl ^
--hidden-import=dotenv ^
--hidden-import=config ^
--hidden-import=doc_loader ^
--hidden-import=rag_chain ^
web.py
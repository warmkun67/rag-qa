# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

RAG (Retrieval-Augmented Generation) intelligent Q&A system — a local knowledge-base chatbot built with LangChain and Streamlit, backed by the DeepSeek API. Users upload documents (PDF, DOCX, TXT, MD, XLSX, CSV) via a web UI and ask questions; the system answers strictly from document content.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Streamlit web UI (primary interface)
streamlit run web.py

# Run the CLI version
python main.py

# Package into a standalone Windows EXE
build.bat
```

There are no tests or linting setup in this project.

## Architecture

### Core design: full-context RAG (not traditional retrieval)

This project deliberately avoids vector search (FAISS). Instead, it concatenates **all document chunks into a single prompt context** and sends the entire thing to the LLM on every query. This guarantees zero retrieval omissions for small-to-medium document collections (≤ ~100K chars). The trade-off: it breaks down when total document size exceeds the model's context window (~64K tokens for DeepSeek).

### Module chain (used by `web.py` and `main.py`)

```
config.py          — API keys, model name, docs directory, chunk settings
doc_loader.py      — load_all_docs() reads all files from docs/, splits with RecursiveCharacterTextSplitter
rag_chain.py       — build_rag_chain() concatenates all splits into full_context, returns a callable (question → answer)
web.py             — Streamlit UI: sidebar for doc upload/delete, chat panel for Q&A, @st.cache_resource on the chain
main.py            — Thin CLI wrapper: calls build_rag_chain(), then a read-loop
```

### Standalone variant: `app.py`

`app.py` is a self-contained older version that does **not** use `doc_loader.py` or `rag_chain.py`. It has its own inline `load_all_files()` / `load_and_split_docs()` and its own LLM invocation loop. Changes to the module chain won't affect `app.py`.

### Important: config values not wired through

`config.py` defines `CHUNK_SIZE=600` and `CHUNK_OVERLAP=50`, but `doc_loader.py` hardcodes `chunk_size=1024` and `chunk_overlap=128` directly in its `RecursiveCharacterTextSplitter` call — the config values are **not used**. Similarly, `config.py` defines `TOP_K=3` but the full-context approach doesn't use top-K retrieval at all (it's a leftover from an earlier retrieval-based design).

### `oldproject/` directory

Contains previous iterations of the core modules (old versions of doc_loader, rag_chain, and web). These are not imported by the current code — purely historical reference.

## Environment

- `.env` at the project root must contain `OPENAI_API_KEY=<your-deepseek-api-key>`
- The LLM endpoint is `https://api.deepseek.com` with model `deepseek-chat` (set in `config.py`)
- Documents live in `./docs/` (created automatically if missing)
- `testtxt/` contains sample test documents used during development

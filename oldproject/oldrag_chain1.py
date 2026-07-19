from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
import config

def build_rag_chain():
    from doc_loader import load_all_docs
    docs = load_all_docs()

    # ========== 向量检索（真正RAG）==========
    embeddings = OpenAIEmbeddings(
        api_key=config.LLM_API_KEY,
        base_url=config.LLM_BASE_URL
    )
    db = FAISS.from_documents(docs, embeddings)
    retriever = db.as_retriever(search_kwargs={"k": 3})

    # ========== 模型 ==========
    llm = ChatOpenAI(
        model=config.LLM_MODEL,
        api_key=config.LLM_API_KEY,
        base_url=config.LLM_BASE_URL,
        temperature=0.05
    )

    prompt = PromptTemplate.from_template("""
    你是专业的文档问答助手。
    只根据提供的上下文回答问题，不编造内容。
    不知道就回答：根据文档无法回答。

    上下文：{context}
    问题：{question}
    回答：
    """)

    def rag_chain(question):
        retrieved = retriever.invoke(question)
        context = "\n".join([d.page_content for d in retrieved])
        response = llm.invoke(prompt.format(context=context, question=question))
        return response.content

    return rag_chain
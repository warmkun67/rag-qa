from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import config

def build_rag_chain():
    from doc_loader import load_all_docs
    docs = load_all_docs()
    if not docs:
        return lambda q: "文档为空，请先上传文件"

    # 【终极方案】直接拼接完整文档，彻底告别检索漏内容问题
    # 小文档（10万字符内）完全无压力，100%不遗漏任何内容
    full_context = "\n\n".join([doc.page_content for doc in docs])

    # 大模型配置
    llm = ChatOpenAI(
        model=config.LLM_MODEL,
        api_key=config.LLM_API_KEY,
        base_url=config.LLM_BASE_URL,
        temperature=0.05  # 极低温度，保证回答严格基于文档，不瞎编
    )

    # 【强化提示词】强制AI完整、有条理回答，禁止漏内容
    prompt = PromptTemplate.from_template("""
    你是专业的文档问答助手，必须严格遵守以下规则：
    1.  100%只根据提供的完整上下文回答，绝对不编造任何内容
    2.  问题涉及多个年份/部分时，必须完整覆盖所有相关内容，不遗漏任何要点
    3.  回答要条理清晰、分点明确，用简洁的语言总结
    4.  上下文有相关信息就必须回答，禁止以“上下文未提供”为由拒绝回答
    5.  只有上下文完全没有相关信息时，才回答：根据文档无法回答

    完整上下文：
    {context}

    用户问题：
    {question}

    你的回答：
    """)

    def rag_chain(question):
        # 直接用完整上下文调用AI，100%不遗漏
        response = llm.invoke(prompt.format(context=full_context, question=question))
        return response.content

    return rag_chain
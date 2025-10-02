from langchain.prompts import PromptTemplate

QA_SYSTEM_PROMPT = PromptTemplate(
    input_variables=["summaries", "question"],
    template="""
Use the content below (text, tables, or OCR snippets) to answer the question.

Context:
{summaries}

Question:
{question}

Answer:
"""
)
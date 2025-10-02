from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.llms.ollama import Ollama
from utils.prompt import QA_SYSTEM_PROMPT
from utils.table_extractor import embed_table_rows


def split_text(text):
    return RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50).split_text(text)

def create_vectorstore(chunks):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    print(chunks)
    print(embeddings)
    return FAISS.from_texts(
        texts=chunks,
        embedding=embeddings,
        metadatas=[{"source": f"chunk_{i+1}"} for i in range(len(chunks))]
    )



def get_qa_chain(vectorstore):
    llm = Ollama(model="llama3")
    retriever = vectorstore.as_retriever(       
        search_type="mmr",
        search_kwargs={"k": 6, "lambda_mult": 0.7}
    )
    return RetrievalQAWithSourcesChain.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": QA_SYSTEM_PROMPT},
        return_source_documents=True
    )

# table row embeddings
def get_table_vector_index(tables):
    return embed_table_rows(tables)
    
    return RetrievalQAWithSourcesChain.from_chain_type(llm=llm, retriever=retriever)

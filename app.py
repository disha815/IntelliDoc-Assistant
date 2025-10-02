import streamlit as st
import tempfile
import re
from utils.docling_extractor import extract_text_with_docling
from utils.rag_pipeline import split_text, create_vectorstore, get_qa_chain
from utils.table_extractor import extract_tables_from_markdown, search_tables_for_range
from utils.ui_helpers import preview_text, download_chat
from components.sidebar import show_sidebar_info
from components.chat_history import render_chat_history

# --- Page Config ---
st.set_page_config(page_title="📋 IntelliDoc Assistant: NHPC PDF Assistant", layout="centered")
st.title(":rocket: NHPC Smart PDF Chatbot")

# --- Session Setup ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""
if "tables" not in st.session_state:
    st.session_state.tables = []

# --- Reset Button ---
if st.button("🔁 Reset Session"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()

# --- File Upload ---
uploaded_file = st.file_uploader("📄 Upload a PDF", type="pdf")

if uploaded_file and "processed_file" not in st.session_state:    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        pdf_path = tmp_file.name

    st.session_state.current_file = uploaded_file.name

    with st.spinner("🔍 Extracting content with Docling + OCR..."):
        try:
            text = extract_text_with_docling(pdf_path)
            tables = extract_tables_from_markdown(text)
            chunks = split_text(text)
            vectorstore = create_vectorstore(chunks)
            qa_chain = get_qa_chain(vectorstore)

            st.session_state.qa_chain = qa_chain
            st.session_state.vectorstore = vectorstore
            st.session_state.extracted_text = text
            st.session_state.tables = tables
            st.session_state.processed_file = True  # ✅ Mark file as processed


            st.success("✅ PDF parsed. You can now ask questions.")
        except Exception as e:
            st.error(f"❌ Error loading PDF: {str(e)}")

# --- Check if QA Chain Ready ---
if st.session_state.qa_chain is None:
    st.warning("⚠️ RAG pipeline is not ready. Please upload a valid PDF first.")

# --- Question-Answering Section ---
if st.session_state.extracted_text:
    preview_text(st.session_state.extracted_text)
    query = st.text_input("💬 Ask a question about the document:")

    if query:
        st.markdown("### 🧠 Answer")
        try:
            final_answer = ""

            if st.session_state.qa_chain is None:
                final_answer = "❌ QA system not initialized. Please upload a valid PDF."
            else:
                number_match = re.search(r'(\d+)', query)
                if number_match and st.session_state.tables:
                    number = int(number_match.group())
                    answer_df = search_tables_for_range(st.session_state.tables, column_name="Value", value=number)
                    if answer_df is not None and not answer_df.empty:
                        table_answer = answer_df.to_markdown(index=False)
                        final_answer = f"📊 Found in table:\n\n{table_answer}"
                    else:
                        response = st.session_state.qa_chain.invoke({"question": query})
                        final_answer = response.get("answer", "🤖 Sorry, no relevant answer found.")
                else:
                    response = st.session_state.qa_chain.invoke({"question": query})
                    final_answer = response.get("answer", "🤖 Sorry, no relevant answer found.")

                st.write(final_answer)

                if isinstance(response, dict) and "source_documents" in response:
                    for doc in response["source_documents"]:
                        st.markdown(f"**📌 From Chunk:** `{doc.metadata.get('source', 'unknown')}`")
                        st.text(doc.page_content[:500])

            st.session_state.chat_history.append((query, final_answer))
        except Exception as e:
            st.error(f"❌ Error during QA: {str(e)}")

    render_chat_history()
    download_chat(st.session_state.chat_history)

# --- Sidebar Info ---
show_sidebar_info()

import pandas as pd
import streamlit as st

def download_chat(chat_history):
    df = pd.DataFrame(chat_history, columns=["Question", "Answer"])
    st.download_button("Download Q&A Log", df.to_csv(index=False), "chat_log.csv", "text/csv")

def preview_text(text):
    st.markdown("### 📄 Extracted Content Preview")
    st.text_area("Text (first 2000 chars):", text[:2000], height=200)

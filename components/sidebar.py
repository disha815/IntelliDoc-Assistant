import streamlit as st

def show_sidebar_info():
    with st.sidebar:
        st.image("static/nhpc_logo.png", width=200)
        st.markdown("## 📊 Info")
        st.write("Model: LLaMA 3.2")
        st.write(f"Questions Asked: {len(st.session_state.chat_history)}")
        if "current_file" in st.session_state:
            st.write(f"PDF: {st.session_state.current_file}")

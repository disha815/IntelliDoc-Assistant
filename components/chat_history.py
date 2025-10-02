import streamlit as st

def render_chat_history():
    st.markdown("### 💬 Chat History")
    for q, a in reversed(st.session_state.chat_history):
        st.markdown(f"**👤 You:** {q}")
        st.markdown(f"**🤖 NHPC Assistant:** {a}")
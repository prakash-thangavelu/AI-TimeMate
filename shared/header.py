import streamlit as st

def render_header(title):
    st.markdown(
        f"""
        <div style="
            background-color:#4F46E5;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1.5rem;">
            <h2 style="color:white; margin:0; line-height:0">AI-TimeMate</h2>
            <h3 style="color:white; margin:0; line-height:0; font-weight: normal; font-style: italic">{title}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

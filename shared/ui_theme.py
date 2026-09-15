import streamlit as st

PRIMARY = "#4F46E5"        # Indigo
SECONDARY = "#6366F1"      # Light Indigo
BG_LIGHT = "#F3F4F6"       # Light Gray
CARD_BG = "white"
TEXT_DARK = "#1F2937"

def apply_theme():
    st.markdown(
        f"""
        <style>
            body {{
                background-color: {BG_LIGHT};
            }}

            .stButton>button {{
                background-color: {PRIMARY};
                color: white;
                border-radius: 8px;
                padding: 0.6rem 1.2rem;
                font-size: 1rem;
                border: none;
            }}

            .stButton>button:hover {{
                background-color: {SECONDARY};
            }}

            .card {{
                background-color: {CARD_BG};
                padding: 1.2rem;
                border-radius: 10px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                margin-bottom: 1rem;
            }}

            h1, h2, h3 {{
                color: {TEXT_DARK};
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

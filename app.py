import streamlit as st

from shared.sidebar import render_sidebar
from shared.header import render_header
from shared.ui_theme import apply_theme

apply_theme()
render_sidebar()
render_header("Home")

st.set_page_config(page_title="AI-TimeMate")
st.write("Use the left sidebar to navigate.")

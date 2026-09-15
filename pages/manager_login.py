import streamlit as st

from db import get_db
from shared.sidebar import render_sidebar
from shared.header import render_header
from shared.ui_theme import apply_theme

apply_theme()
render_sidebar()

# 🚫 Prevent manager login if employee is already logged in
if st.session_state.get("employee_id"):
    st.error("A employee is already logged in. Please logout before continuing as an manager.")
    st.stop()

render_header("Manager Login")

# st.title("AI-TimeMate - Manager Login")

# Connect DB
conn = get_db()
cursor = conn.cursor()

# Fetch managers list
cursor.execute("SELECT manager_id, manager_name FROM managers")
managers = cursor.fetchall()

if not managers:
    st.error("No managers found in database.")
    st.stop()

# Dropdown list
manager_names = {name: mid for mid, name in managers}

selected_manager = st.selectbox("Select Manager", list(manager_names.keys()))

if st.button("Login"):
    st.session_state["manager_id"] = manager_names[selected_manager]
    st.session_state["manager_name"] = selected_manager

    st.success(f"Welcome {selected_manager}!")
    st.switch_page("pages/manager_approval.py")

conn.close()
import streamlit as st
import sqlite3

st.title("AI-TimeMate - Manager Login")

# Connect DB
conn = sqlite3.connect("aitimemate.db")
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

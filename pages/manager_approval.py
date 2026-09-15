import streamlit as st
import sqlite3
import json

from shared.sidebar import render_sidebar
from shared.header import render_header
from shared.ui_theme import apply_theme
from shared.animated import success_screen
from shared.cards import timesheet_card

apply_theme()
render_sidebar()
render_header("Manager Approval")

# 🔥 NEW: Check manager login
if "manager_id" not in st.session_state:
    st.error("Please login as Manager.")
    st.stop()

manager_name = st.session_state["manager_name"]

# st.title("Manager Approval Dashboard")
st.write(f"Logged in as **{manager_name}**")

# 🔥 NEW: Load pending timesheets
conn = sqlite3.connect("aitimemate.db")
cursor = conn.cursor()

cursor.execute("""
    SELECT id, employee_id, employee_name, json_data, status
    FROM timesheets
    WHERE status = 'Pending Approval'
""")

rows = cursor.fetchall()

if not rows:
    st.info("No pending timesheets.")
    st.stop()

# 🔥 NEW: Show each timesheet in an expandable card
for row in rows:
    ts_id, emp_id, emp_name, json_data, status = row
    data = json.loads(json_data)

    timesheet_card(
        ts_id=ts_id,
        emp_id=emp_id,
        emp_name=emp_name,
        status=status,
        json_data=json_data,
        manager_comment=data.get("manager_comment")
    )
    
conn.close()

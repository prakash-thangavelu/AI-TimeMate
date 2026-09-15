import streamlit as st
import sqlite3
import json

from shared.sidebar import render_sidebar
from shared.header import render_header
from shared.ui_theme import apply_theme

apply_theme()
render_sidebar()
render_header("Manager Approval History")

# 🔥 Check manager login
if "manager_id" not in st.session_state:
    st.error("Please login as Manager.")
    st.stop()

manager_name = st.session_state["manager_name"]
st.write(f"Logged in as **{manager_name}**")

# 🔥 Load approved + rejected timesheets
conn = sqlite3.connect("aitimemate.db")
cursor = conn.cursor()

cursor.execute("""
    SELECT id, employee_id, employee_name, json_data, status
    FROM timesheets
    WHERE status IN ('Approved', 'Rejected')
    ORDER BY id DESC
""")

rows = cursor.fetchall()

if not rows:
    st.info("No approval history available.")
    st.stop()

# ⭐ Simple List View
st.markdown("### 📜 Approval History")

for row in rows:
    ts_id, emp_id, emp_name, json_data, status = row
    data = json.loads(json_data)

    week = data.get("week", "Week not specified")
    comment = data.get("manager_comment", "No comments")

    st.markdown(
    f"""<div style="background-color:#F8FAFC; padding:15px; border-radius:10px;
    margin-bottom:12px; border:1px solid #E5E7EB;">
        <b>{emp_name}</b> — Timesheet #{ts_id}<br>
        <span style="color:#6B7280;">{week}</span><br><br>
        <b>Status:</b> {status}<br>
        <b>Manager Comment:</b> {comment}
    </div>""",
    unsafe_allow_html=True
)


conn.close()

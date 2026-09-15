import streamlit as st
import json

from db import get_db
from shared.sidebar import render_sidebar
from shared.header import render_header
from shared.ui_theme import apply_theme
from shared.cards import timesheet_card

apply_theme()
render_sidebar()
render_header("Employee Dashboard")

# st.title("Employee Dashboard")

# 🔥 Check employee login
if "employee_id" not in st.session_state:
    st.error("Please login as Employee.")
    st.stop()

employee_id = st.session_state["employee_id"]
employee_name = st.session_state["employee_name"]

if st.session_state.get("edit_mode"):
    from pages.timesheet_edit import render_edit_form
    render_edit_form(
        st.session_state["edit_ts_id"],
        st.session_state["edit_ts_data"]
    )
    st.stop()

st.write(f"Logged in as **{employee_name}**")

# 🔥 Connect DB
conn = get_db()
cursor = conn.cursor()

# 🔥 Fetch employee's timesheets
cursor.execute("""
    SELECT id, json_data, status
    FROM timesheets
    WHERE employee_id = ?
    ORDER BY id DESC
""", (employee_id,))

rows = cursor.fetchall()

if not rows:
    st.info("You have not submitted any timesheets yet.")
    st.stop()

# 🔥 Show each timesheet
for row in rows:
    ts_id, json_data, status = row
    data = json.loads(json_data)

    manager_comment = data.get("manager_comment")

    timesheet_card(
        ts_id=ts_id,
        emp_id=employee_id,
        emp_name=employee_name,
        status=status,
        json_data=json_data,
        manager_comment=manager_comment
    )

conn.close()

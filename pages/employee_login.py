import streamlit as st

from db import get_db
from shared.sidebar import render_sidebar
from shared.header import render_header
from shared.ui_theme import apply_theme

apply_theme()
render_sidebar()

# 🚫 Prevent employee login if manager is already logged in
if st.session_state.get("manager_id"):
    st.error("A manager is already logged in. Please logout before continuing as an employee.")
    st.stop()

render_header("Employee Login")

st.set_page_config(page_title="Employee Login")

# DB connection
conn = get_db()
cursor = conn.cursor()

# Fetch employees
cursor.execute("SELECT employee_id, employee_name FROM employees")
employees = cursor.fetchall()

# st.title("AI-TimeMate - Employee Login")

# Dropdown for employee selection
employee_names = {emp[1]: emp[0] for emp in employees}
selected_employee = st.selectbox("Select Employee", list(employee_names.keys()))

# Store selected employee_id
employee_id = employee_names[selected_employee]

st.success(f"Logged in as: {selected_employee} (ID: {employee_id})")

# Continue button
if st.button("Continue"):
    st.session_state["employee_id"] = employee_id
    st.session_state["employee_name"] = selected_employee
    st.switch_page("pages/timesheet_input.py")


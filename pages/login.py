import streamlit as st
import sqlite3

st.set_page_config(page_title="Login")

# DB connection
conn = sqlite3.connect("aitimemate.db")
cursor = conn.cursor()

# Fetch employees
cursor.execute("SELECT employee_id, employee_name FROM employees")
employees = cursor.fetchall()

st.title("AI-TimeMate - Employee Login")

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


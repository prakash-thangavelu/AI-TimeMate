import streamlit as st

st.set_page_config(page_title="AI-TimeMate")
st.write("Use the left sidebar to navigate.")
st.sidebar.title("Navigation")

st.sidebar.page_link("pages/login.py", label="Employee Login")
st.sidebar.page_link("pages/timesheet_input.py", label="Timesheet Input")
st.sidebar.page_link("pages/manager_login.py", label="Manager Login")
st.sidebar.page_link("pages/manager_approval.py", label="Manager Approval")

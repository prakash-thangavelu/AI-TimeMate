import streamlit as st

def render_sidebar():
    st.sidebar.title("Navigation")

    st.sidebar.page_link("app.py", label="🏠 Home")
    st.sidebar.page_link("pages/login.py", label="👨‍💼 Employee Login")
    st.sidebar.page_link("pages/timesheet_input.py", label="📝 Timesheet Input")
    st.sidebar.page_link("pages/employee_dashboard.py", label="📊 Employee Dashboard")
    st.sidebar.page_link("pages/manager_login.py", label="🧑‍💼 Manager Login")
    st.sidebar.page_link("pages/manager_approval.py", label="✔️ Manager Approval")

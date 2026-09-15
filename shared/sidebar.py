import streamlit as st

def render_sidebar():
    st.sidebar.title("Navigation")

    st.sidebar.page_link("app.py", label="🏠 Home")
    st.sidebar.page_link("pages/employee_login.py", label="👨‍💼 Employee Login")
    st.sidebar.page_link("pages/timesheet_input.py", label="📝 Timesheet Input")
    st.sidebar.page_link("pages/employee_dashboard.py", label="📊 Employee Dashboard")
    st.sidebar.page_link("pages/manager_login.py", label="🧑‍💼 Manager Login")
    st.sidebar.page_link("pages/manager_approval.py", label="✔️ Manager Approval")
    st.sidebar.page_link("pages/manager_history.py", label="📜 Approval History")

    st.sidebar.markdown("---")

    # ⭐ LOGOUT BUTTON
    if (st.session_state.get("manager_id") or st.session_state.get("employee_id")):
        if st.sidebar.button("🚪 Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.sidebar.success("Logged out successfully!")
            st.rerun()

import streamlit as st
import sqlite3
import json

# 🔥 NEW: Check manager login
if "manager_id" not in st.session_state:
    st.error("Please login as Manager.")
    st.stop()

manager_name = st.session_state["manager_name"]

st.title("Manager Approval Dashboard")
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

    with st.expander(f"Timesheet #{ts_id} — {emp_name}"):
        st.json(data)

        # 🔥 NEW: Manager comments
        comment = st.text_area(f"Manager Comments for Timesheet #{ts_id}")

        col1, col2 = st.columns(2)

        # 🔥 NEW: Approve button
        if col1.button(f"Approve #{ts_id}"):
            cursor.execute("""
                UPDATE timesheets
                SET status = 'Approved', json_data = ?
                WHERE id = ?
            """, (json.dumps({**data, "manager_comment": comment}), ts_id))
            conn.commit()
            st.success(f"Timesheet #{ts_id} Approved")

        # 🔥 NEW: Reject button
        if col2.button(f"Reject #{ts_id}"):
            cursor.execute("""
                UPDATE timesheets
                SET status = 'Rejected', json_data = ?
                WHERE id = ?
            """, (json.dumps({**data, "manager_comment": comment}), ts_id))
            conn.commit()
            st.error(f"Timesheet #{ts_id} Rejected")

conn.close()

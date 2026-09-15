import json
import streamlit as st
from db import get_db

def timesheet_card(ts_id, emp_id, emp_name, status, json_data, manager_comment=None):
    # Handle dict or raw JSON string safely
    if isinstance(json_data, str):
        data = json.loads(json_data)
    else:
        data = json_data

    # --- CARD HEADER ---
    st.markdown(
        f"""<div style="
            background-color: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            margin-bottom: 10px;">
            <h3 style="margin:0; color:#4F46E5;">
                {emp_name} - Timesheet #{ts_id}
            </h3>
            <p style="margin: 5px 0 0 0; font-size: 16px; color: #374151;">
                Status: <b>{status}</b>
            </p>
        </div>""",
        unsafe_allow_html=True
    )

    if status == "Rejected":
        if st.button(f"Edit Timesheet #{ts_id}"):
            st.session_state["edit_ts_id"] = ts_id
            st.session_state["edit_ts_data"] = data
            st.session_state["edit_mode"] = True
            st.session_state["edit_from_dashboard"] = True
            st.rerun()

    # --- HTML TABLE FOR ENTRIES ---
    entries = data.get("entries", [])

    table_html = """<table style="
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
        background-color: white;">
        <tr style="background-color:#E5E7EB;">
            <th style="padding:8px; border:1px solid #D1D5DB;">Day</th>
            <th style="padding:8px; border:1px solid #D1D5DB;">Mode</th>
            <th style="padding:8px; border:1px solid #D1D5DB;">Hours</th>
            <th style="padding:8px; border:1px solid #D1D5DB;">Tasks</th>
        </tr>"""

    for e in entries:
        table_html += f"""<tr>
            <td style="padding:8px; border:1px solid #D1D5DB;">{e.get('day')}</td>
            <td style="padding:8px; border:1px solid #D1D5DB;">{e.get('mode')}</td>
            <td style="padding:8px; border:1px solid #D1D5DB;">{e.get('hours')}</td>
            <td style="padding:8px; border:1px solid #D1D5DB;">{e.get('tasks')}</td>
        </tr>"""

    table_html += "</table>"

    st.markdown(table_html, unsafe_allow_html=True)

    # --- NOTES ---
    if "notes" in data:
        st.markdown(
            f"""<div style="
                background-color:#F9FAFB;
                padding:12px;
                border-radius:8px;
                margin-top:10px;">
                <b>Notes:</b><br>{data['notes']}
            </div>""",
            unsafe_allow_html=True
        )

    # --- MANAGER COMMENT ---
    if manager_comment:
        st.markdown(
            f"""<div style="
                background-color: #F3F4F6;
                padding: 12px;
                border-radius: 8px;
                margin-top: 10px;">
                <b>Manager Comment:</b><br>
                {manager_comment}
            </div><hr>""",
            unsafe_allow_html=True
        )

    # --- MANAGER ACTIONS ---
    if st.session_state.get("manager_id"):
        st.markdown("<hr>", unsafe_allow_html=True)

        comment = st.text_area(f"Manager Comments for Timesheet #{ts_id}", key=f"mgr_comment_{ts_id}")

        col1, col2 = st.columns(2)

        if col1.button(f"Approve #{ts_id}", key=f"approve_{ts_id}"):
            conn = get_db()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE timesheets
                SET status = 'Approved', json_data = ?
                WHERE id = ?
            """, (json.dumps({**data, "manager_comment": comment}), ts_id))
            conn.commit()
            conn.close()
            st.success("Approved ✔️")
            st.rerun()

        if col2.button(f"Reject #{ts_id}", key=f"reject_{ts_id}"):
            conn = get_db()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE timesheets
                SET status = 'Rejected', json_data = ?
                WHERE id = ?
            """, (json.dumps({**data, "manager_comment": comment}), ts_id))
            conn.commit()
            conn.close()
            st.error("Rejected ❌")
            st.rerun()

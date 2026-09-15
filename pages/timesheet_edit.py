import streamlit as st
import json

from db import get_db

def render_edit_form(ts_id, data):
    st.header(f"Edit Timesheet #{ts_id}")

    updated_entries = []

    for entry in data["entries"]:
        st.subheader(entry["day"])

        mode = st.selectbox(
            "Mode",
            ["Office", "WFH", "Leave"],
            index=["Office","WFH","Leave"].index(entry["mode"]),
            key=f"mode_{entry['day']}"
        )

        hours = st.number_input(
            "Hours",
            min_value=0,
            max_value=12,
            value=entry["hours"],
            key=f"hours_{entry['day']}"
        )

        tasks = st.text_input(
            "Tasks",
            value=entry["tasks"],
            key=f"tasks_{entry['day']}"
        )

        updated_entries.append({
            "day": entry["day"],
            "mode": mode,
            "hours": hours,
            "tasks": tasks
        })

    notes = st.text_area("Notes", value=data.get("notes", ""))

    if st.button("Resubmit"):
        updated_json = json.dumps({
            "week": data["week"],
            "entries": updated_entries,
            "notes": notes
        })

        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE timesheets SET json_data=?, status='Pending Approval' WHERE id=?",
            (updated_json, ts_id)
        )
        conn.commit()
        conn.close()

        st.success("Timesheet resubmitted for approval!")
        st.session_state["edit_mode"] = False

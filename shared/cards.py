import json
import streamlit as st
from db import get_db

def timesheet_card(ts_id, emp_id, emp_name, proj_name, status, json_data, manager_comment=None):
    # Handle dict or raw JSON string safely
    if isinstance(json_data, str):
        data = json.loads(json_data)
    else:
        data = json_data or {}

    week_range = data.get("week", "N/A")

    # Define color scheme based on status
    status_styles = {
        "Submitted": "background-color: #dbeafe; color: #1e40af;",
        "Approved":  "background-color: #dcfce7; color: #166534;",
        "Pending":   "background-color: #fef3c7; color: #92400e;",
        "Rejected":  "background-color: #fee2e2; color: #991b1b;",
    }
    badge_style = status_styles.get(status, "background-color: #f1f5f9; color: #475569;")

    # --- BUILD SINGLE COMBINED HTML BLOCK ---
    card_html = f"""<div style="background-color: #ffffff; padding: 16px 20px; border-radius: 10px 10px 0 0; border: 1px solid #e2e8f0; border-bottom: none; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
<span style="font-size: 16px; font-weight: 700; color: #0f172a;">{emp_name}</span>
<span style="padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; {badge_style}">{status}</span>
</div>
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; font-size: 13px; color: #334155;">
<div><span style="font-size: 11px; font-weight: 600; color: #64748b; text-transform: uppercase; display: block; margin-bottom: 2px;">Week Range</span><strong style="color: #1e293b;">{week_range}</strong></div>
<div><span style="font-size: 11px; font-weight: 600; color: #64748b; text-transform: uppercase; display: block; margin-bottom: 2px;">Project</span><strong style="color: #1e293b;">{proj_name}</strong></div>
</div>
</div>"""

    # --- TABLE SECTION ---
    entries = data.get("entries", [])
    table_rows = ""
    for e in entries:
        table_rows += f"""<tr style="border-bottom: 1px solid #f1f5f9; color: #334155;">
<td style="padding: 10px; font-weight: 600;">{e.get('day')}</td>
<td style="padding: 10px;">{e.get('mode')}</td>
<td style="padding: 10px;">{e.get('hours')}</td>
<td style="padding: 10px;">{e.get('tasks')}</td>
</tr>"""

    table_html = f"""<div style="border: 1px solid #e2e8f0; border-top: none; background: white; padding: 0 20px 16px 20px; border-radius: 0 0 10px 10px;">
<table style="width: 100%; border-collapse: collapse; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 13px;">
<thead>
<tr style="background-color: #f8fafc; color: #475569; text-align: left; font-size: 11px; text-transform: uppercase;">
<th style="padding: 10px; border-bottom: 2px solid #e2e8f0;">Day</th>
<th style="padding: 10px; border-bottom: 2px solid #e2e8f0;">Mode</th>
<th style="padding: 10px; border-bottom: 2px solid #e2e8f0;">Hours</th>
<th style="padding: 10px; border-bottom: 2px solid #e2e8f0;">Tasks</th>
</tr>
</thead>
<tbody>
{table_rows}
</tbody>
</table>"""

    # --- NOTES BLOCK ---
    if "notes" in data and data["notes"]:
        table_html += f"""<div style="background-color: #f8fafc; padding: 10px 12px; border-radius: 6px; margin-top: 12px; font-size: 12px; color: #475569; border: 1px solid #f1f5f9;"><strong style="color: #1e293b;">Notes:</strong> {data['notes']}</div>"""

    # --- MANAGER COMMENT BLOCK ---
    if manager_comment:
        table_html += f"""<div style="margin-top: 12px; padding: 10px 12px; background-color: #fef2f2; border-left: 3px solid #ef4444; border-radius: 4px; font-size: 12px; color: #991b1b;"><strong>Manager Comment:</strong> {manager_comment}</div>"""

    table_html += "</div>"

    # RENDER COMPLETE HTML CARD
    st.markdown(card_html + table_html, unsafe_allow_html=True)

    # --- EDIT ACTION FOR REJECTED TIMESHEETS ---
    if status == "Rejected":
        if st.button(f"Edit Timesheet #{ts_id}", key=f"edit_btn_{ts_id}"):
            st.session_state["edit_ts_id"] = ts_id
            st.session_state["edit_ts_data"] = data
            st.session_state["edit_mode"] = True
            st.session_state["edit_from_dashboard"] = True
            st.rerun()

    # --- MANAGER ACTIONS ---
    if st.session_state.get("manager_id"):
        with st.container():
            comment = st.text_area(f"Manager Comments", key=f"mgr_comment_{ts_id}")

            col1, col2 = st.columns(2)

            if col1.button(f"Approve #{ts_id}", key=f"approve_{ts_id}", type="primary"):
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

        st.markdown("<hr style='margin: 20px 0; border: none; border-top: 1px solid #e2e8f0;'>", unsafe_allow_html=True)
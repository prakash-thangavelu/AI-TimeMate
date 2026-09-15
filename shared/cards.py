import streamlit as st
import json

def timesheet_card(ts_id, status, json_data, manager_comment=None):
    data = json.loads(json_data)

    # Card container
    st.markdown(
        f"""
        <div style="
            background-color:white;
            padding:20px;
            border-radius:12px;
            box-shadow:0 4px 12px rgba(0,0,0,0.08);
            margin-bottom:20px;">
            
            <h3 style="margin:0; color:#4F46E5;">
                Timesheet #{ts_id}
            </h3>

            <p style="margin:5px 0 15px 0; 
                      font-size:16px; 
                      color:#374151;">
                Status: <b>{status}</b>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # JSON preview
    with st.expander("View Details"):
        st.json(data)

    # Manager comment
    if manager_comment:
        st.markdown(
            f"""
            <div style="
                background-color:#F3F4F6;
                padding:12px;
                border-radius:8px;
                margin-top:10px;">
                <b>Manager Comment:</b><br>
                {manager_comment}
            </div>
            """,
            unsafe_allow_html=True
        )

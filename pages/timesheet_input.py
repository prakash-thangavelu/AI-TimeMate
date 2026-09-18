import streamlit as st
import json

from db import get_db
from shared.sidebar import render_sidebar
from shared.header import render_header
from shared.ui_theme import apply_theme
from shared.animated import success_screen
from shared.cards import timesheet_card  # Import timesheet card renderer

apply_theme()
render_sidebar()
render_header("Weekly Timesheet Input")

# Import Azure GenAI extractor
from genai_extractor import extract_timesheet

# Check login
if "employee_id" not in st.session_state:
    st.error("Please login first.")
    st.stop()

employee_id = st.session_state["employee_id"]
employee_name = st.session_state["employee_name"]
assigned_project = st.session_state["assigned_project"]

st.write(f"Logged in as **{employee_name}**")

# Text area for natural language input
weekly_text = st.text_area(
    "Enter your weekly work details:",
    placeholder="Example: I worked from home on Mon–Wed, took leave on Thursday, and went to office on Friday."
)

# Preview with real GenAI extraction
if st.button("Generate Preview"):
    if not weekly_text.strip():
        st.error("Please enter your weekly details.")
    else:
        # Call Azure GenAI extraction logic
        preview_json = extract_timesheet(weekly_text)

        # If model returned a list, convert to dict
        if isinstance(preview_json, list):
            if len(preview_json) > 0:
                preview_json = preview_json[0]
            else:
                st.error("Extraction failed: empty list returned.")
                st.stop()

        if not isinstance(preview_json, dict):
            st.error("Extraction failed: model did not return a valid JSON object.")
            st.write(preview_json)
            st.stop()

        # Add employee info into extracted JSON
        preview_json["employee_id"] = employee_id
        preview_json["employee_name"] = employee_name
        preview_json["project"] = assigned_project
        preview_json["status"] = "Draft"

        st.session_state["preview_json"] = preview_json

# --- DISPLAY PREVIEW CARD IF PREVIEW DATA EXISTS ---
if "preview_json" in st.session_state:
    p_data = st.session_state["preview_json"]
    
    st.subheader("Preview Timesheet")
    
    # Render the styled HTML card component
    timesheet_card(
        ts_id="PREVIEW",
        emp_id=p_data["employee_id"],
        emp_name=p_data["employee_name"],
        proj_name=p_data["project"],
        status=p_data["status"],
        json_data=p_data
    )

# Submit button
if st.button("Submit Timesheet"):
    if "preview_json" not in st.session_state:
        st.error("Please generate preview before submitting.")
    else:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS timesheets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER,
                employee_name TEXT,
                json_data TEXT,
                status TEXT
            )
        """)

        # Set status to Pending Approval on submit
        submit_data = {**st.session_state["preview_json"], "status": "Pending Approval"}

        cursor.execute("""
            INSERT INTO timesheets (employee_id, employee_name, json_data, status)
            VALUES (?, ?, ?, ?)
        """, (
            employee_id,
            employee_name,
            json.dumps(submit_data),
            "Pending Approval"
        ))

        conn.commit()
        conn.close()

        # Clear session state preview after successful submission
        del st.session_state["preview_json"]

        success_screen(
            message="Timesheet Submitted 🎉",
            sub_message="Timesheet submitted for manager approval!"
        )
import streamlit as st
import sqlite3
import json

# Import Azure GenAI extractor
from genai_extractor import extract_timesheet

# Check login
if "employee_id" not in st.session_state:
    st.error("Please login first.")
    st.stop()

employee_id = st.session_state["employee_id"]
employee_name = st.session_state["employee_name"]

st.title("AI-TimeMate - Weekly Timesheet Input")
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

        # Add employee info into extracted JSON
        preview_json["employee_id"] = employee_id
        preview_json["employee_name"] = employee_name
        preview_json["status"] = "Draft"

        st.subheader("Preview (JSON)")
        st.json(preview_json)

        st.session_state["preview_json"] = preview_json

# Submit button
if st.button("Submit Timesheet"):
    if "preview_json" not in st.session_state:
        st.error("Please generate preview before submitting.")
    else:
        conn = sqlite3.connect("aitimemate.db")
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

        cursor.execute("""
            INSERT INTO timesheets (employee_id, employee_name, json_data, status)
            VALUES (?, ?, ?, ?)
        """, (
            employee_id,
            employee_name,
            json.dumps(st.session_state["preview_json"]),
            "Pending Approval"
        ))

        conn.commit()
        conn.close()

        st.success("Timesheet submitted for manager approval!")

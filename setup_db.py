import os
import json

from db import get_db

conn = get_db()
cursor = conn.cursor()

# Managers table
cursor.execute("""
CREATE TABLE IF NOT EXISTS managers (
    manager_id INTEGER PRIMARY KEY,
    manager_name TEXT NOT NULL
)
""")

# Employees table
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    employee_id INTEGER PRIMARY KEY,
    employee_name TEXT NOT NULL,
    manager_id INTEGER,
    FOREIGN KEY(manager_id) REFERENCES managers(manager_id)
)
""")

# Calendar table (Mon–Sun mapping)
cursor.execute("""
CREATE TABLE IF NOT EXISTS calendar (
    date TEXT PRIMARY KEY,
    weekday TEXT NOT NULL
)
""")

# Leave table  ⭐ FIXED LINE
cursor.execute("""
CREATE TABLE IF NOT EXISTS leaves (
    employee_id INTEGER,
    date TEXT,
    leave_type TEXT,
    PRIMARY KEY (employee_id, date)
)
""")

# Holidays table
cursor.execute("""
CREATE TABLE IF NOT EXISTS holidays (
    date TEXT PRIMARY KEY,
    holiday_name TEXT NOT NULL
)
""")

# Timesheet submissions
cursor.execute("""
CREATE TABLE IF NOT EXISTS timesheets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    employee_name TEXT,
    project_name TEXT,
    json_data TEXT,
    status TEXT
)
""")

# Sample managers
cursor.execute("INSERT OR IGNORE INTO managers VALUES (101, 'Ramesh')")
cursor.execute("INSERT OR IGNORE INTO managers VALUES (102, 'Priya')")

# Sample employees
cursor.execute("INSERT OR IGNORE INTO employees VALUES (1, 'Prakash', 101)")
cursor.execute("INSERT OR IGNORE INTO employees VALUES (2, 'Karthik', 101)")
cursor.execute("INSERT OR IGNORE INTO employees VALUES (3, 'Divya', 102)")

# -----------------------------
# ⭐ SAMPLE TIMESHEET DATA
# -----------------------------

# 1️⃣ Pending Timesheet
pending_json = json.dumps({
    "week": "2026-09-07 to 2026-09-11",
    "entries": [
        {"day": "Monday", "mode": "WFH", "hours": 8, "tasks": "API integration testing"},
        {"day": "Tuesday", "mode": "Office", "hours": 8, "tasks": "Sprint planning + code review"},
        {"day": "Wednesday", "mode": "WFH", "hours": 7, "tasks": "Bug fixes"},
        {"day": "Thursday", "mode": "WFH", "hours": 8, "tasks": "UI enhancements"},
        {"day": "Friday", "mode": "Leave", "hours": 0, "tasks": "N/A"}
    ],
    "notes": "Completed UI fixes for Timesheet module"
})

cursor.execute("""
INSERT INTO timesheets (employee_id, employee_name, project_name, json_data, status)
VALUES (?, ?, ?, ?, ?)
""", (1, "Prakash", "Phoenix Migration", pending_json, "Pending Approval"))

# 2️⃣ Approved Timesheet
approved_json = json.dumps({
    "week": "2026-08-31 to 2026-09-04",
    "entries": [
        {"day": "Monday", "mode": "Office", "hours": 8, "tasks": "Requirement discussion"},
        {"day": "Tuesday", "mode": "WFH", "hours": 7, "tasks": "Prototype development"},
        {"day": "Wednesday", "mode": "WFH", "hours": 8, "tasks": "Model testing"},
        {"day": "Thursday", "mode": "Office", "hours": 8, "tasks": "Team sync-up"},
        {"day": "Friday", "mode": "WFH", "hours": 6, "tasks": "Documentation"}
    ],
    "notes": "Prototype ready for demo",
    "manager_comment": "Good work Prakash. Keep the same pace."
})

cursor.execute("""
INSERT INTO timesheets (employee_id, employee_name, project_name, json_data, status)
VALUES (?, ?, ?, ?, ?)
""", (1, "Prakash", "Phoenix Migration", approved_json, "Approved"))

# 3️⃣ Rejected Timesheet
rejected_json = json.dumps({
    "week": "2026-08-24 to 2026-08-28",
    "entries": [
        {"day": "Monday", "mode": "WFH", "hours": 8, "tasks": "Initial setup"},
        {"day": "Tuesday", "mode": "WFH", "hours": 8, "tasks": "Environment configuration"},
        {"day": "Wednesday", "mode": "WFH", "hours": 8, "tasks": "DB schema design"},
        {"day": "Thursday", "mode": "WFH", "hours": 8, "tasks": "Streamlit page creation"},
        {"day": "Friday", "mode": "WFH", "hours": 8, "tasks": "Testing"}
    ],
    "notes": "Completed initial setup",
    "manager_comment": "Hours seem unrealistic for all days. Please resubmit with correct details."
})

cursor.execute("""
INSERT INTO timesheets (employee_id, employee_name, project_name, json_data, status)
VALUES (?, ?, ?, ?, ?)
""", (1, "Prakash", "Phoenix Migration", rejected_json, "Rejected"))



# Projects table
cursor.execute("""
CREATE TABLE IF NOT EXISTS projects (
    project_id INTEGER PRIMARY KEY,
    project_name TEXT NOT NULL
)
""")

# Project assignments table
cursor.execute("""
CREATE TABLE IF NOT EXISTS project_assignments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    project_id INTEGER NOT NULL,
    FOREIGN KEY(employee_id) REFERENCES employees(employee_id),
    FOREIGN KEY(project_id) REFERENCES projects(project_id)
)
""")

# Sample projects
cursor.execute("INSERT OR IGNORE INTO projects VALUES (201, 'Phoenix Migration')")
cursor.execute("INSERT OR IGNORE INTO projects VALUES (202, 'AI-TimeMate')")
cursor.execute("INSERT OR IGNORE INTO projects VALUES (203, 'Retail Analytics Dashboard')")

# Sample project assignments
cursor.execute("INSERT OR IGNORE INTO project_assignments (employee_id, project_id) VALUES (1, 201)")
cursor.execute("INSERT OR IGNORE INTO project_assignments (employee_id, project_id) VALUES (2, 202)")
cursor.execute("INSERT OR IGNORE INTO project_assignments (employee_id, project_id) VALUES (3, 203)")



conn.commit()
conn.close()

print("Database setup completed with sample data!")



# streamlit config
def create_streamlit_config():
    config_dir = ".streamlit"
    config_file = os.path.join(config_dir, "config.toml")

    # Create folder if missing
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    # Theme content
    theme_content = """
[theme]
base="light"
primaryColor="#4F46E5"
backgroundColor="#F3F4F6"
secondaryBackgroundColor="#FFFFFF"
textColor="#1F2937"
font="sans serif"
"""

    # Write file
    with open(config_file, "w") as f:
        f.write(theme_content.strip())

    print("✓ Streamlit theme config.toml created.")

# Call this inside your main setup flow
create_streamlit_config()


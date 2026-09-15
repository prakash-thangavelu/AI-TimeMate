import sqlite3
import json

conn = sqlite3.connect("aitimemate.db")
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
INSERT INTO timesheets (employee_id, employee_name, json_data, status)
VALUES (?, ?, ?, ?)
""", (1, "Prakash", pending_json, "Pending Approval"))

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
INSERT INTO timesheets (employee_id, employee_name, json_data, status)
VALUES (?, ?, ?, ?)
""", (1, "Prakash", approved_json, "Approved"))

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
INSERT INTO timesheets (employee_id, employee_name, json_data, status)
VALUES (?, ?, ?, ?)
""", (1, "Prakash", rejected_json, "Rejected"))

conn.commit()
conn.close()

print("Database setup completed with sample data!")

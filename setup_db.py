import sqlite3

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

# Leave table
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

conn.commit()
conn.close()

print("Database setup completed!")

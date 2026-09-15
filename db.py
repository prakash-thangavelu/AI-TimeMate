# db.py
import sqlite3

DB_PATH = "aitimemate.db"

def get_db():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

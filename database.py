import sqlite3
import os

DB_FILE = "data/gym.db"

def get_connection():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def setup_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Members table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            membership_type TEXT NOT NULL,
            fee INTEGER NOT NULL,
            paid INTEGER DEFAULT 0,
            join_date TEXT DEFAULT CURRENT_DATE
        )
    """)

    # Finance table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS finance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            amount INTEGER NOT NULL,
            month TEXT NOT NULL,
            year INTEGER NOT NULL,
            date TEXT NOT NULL
        )
    """)

    # Attendance table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER NOT NULL,
            member_name TEXT NOT NULL,
            date TEXT NOT NULL,
            month TEXT NOT NULL,
            year INTEGER NOT NULL
        )
    """)

    # Expenses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            amount INTEGER NOT NULL,
            month TEXT NOT NULL,
            year INTEGER NOT NULL,
            date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print("Database ready!")
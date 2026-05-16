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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            password TEXT NOT NULL,
            membership_type TEXT DEFAULT NULL,
            fee INTEGER DEFAULT 0,
            admission_fee INTEGER DEFAULT 0,
            total_fee INTEGER DEFAULT 0,
            paid INTEGER DEFAULT 0,
            status TEXT DEFAULT 'unverified',
            months_unpaid INTEGER DEFAULT 0,
            join_date TEXT DEFAULT CURRENT_DATE,
            expiry_date TEXT DEFAULT NULL
        )
    """)

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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER NOT NULL,
            member_name TEXT NOT NULL,
            date TEXT NOT NULL,
            check_in TEXT DEFAULT NULL,
            check_out TEXT DEFAULT NULL,
            month TEXT NOT NULL,
            year INTEGER NOT NULL,
            auto_checkout INTEGER DEFAULT 0
        )
    """)

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
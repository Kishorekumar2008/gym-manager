from database import get_connection
from datetime import datetime

def setup():
    pass

def add_member(name, phone, membership_type, fee):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO members (name, phone, membership_type, fee, paid)
        VALUES (?, ?, ?, ?, 0)
    """, (name, phone, membership_type, fee))
    conn.commit()
    conn.close()
    print(f"Member {name} added!")

def get_all_members():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def show_members():
    members = get_all_members()
    if len(members) == 0:
        print("No members yet!")
        return
    print("\n===== GYM MEMBERS =====")
    for m in members:
        status = "PAID" if m["paid"] else "NOT PAID"
        print(f"ID:{m['id']} | {m['name']} | {m['phone']} | {status}")
    print("=======================\n")

def mark_paid(member_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE members SET paid = 1 WHERE id = ?", (member_id,))
    conn.commit()
    conn.close()
    print(f"Member {member_id} marked as paid!")

def reset_all_payments():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE members SET paid = 0")
    conn.commit()
    conn.close()
    print("All payments reset for new month!")
from database import get_connection
from datetime import datetime

PLANS = {
    "monthly":     {"fee": 700,  "admission": 200, "label": "Monthly"},
    "quarterly":   {"fee": 1800, "admission": 0,   "label": "Quarterly"},
    "half_yearly": {"fee": 3400, "admission": 0,   "label": "Half Yearly"},
    "yearly":      {"fee": 6000, "admission": 0,   "label": "Yearly"},
}

def setup():
    pass

def add_member(name, phone, membership_type, is_first_month=True):
    plan = PLANS[membership_type]
    fee = plan["fee"]
    admission = plan["admission"] if is_first_month and membership_type == "monthly" else 0
    total = fee + admission
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO members
        (name, phone, membership_type, fee, admission_fee, total_fee, paid, status, months_unpaid)
        VALUES (?, ?, ?, ?, ?, ?, 0, 'active', 0)
    """, (name, phone, membership_type, fee, admission, total))
    conn.commit()
    conn.close()
    print(f"Member {name} added! Fee: ₹{total}")

def get_all_members():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members WHERE status = 'active' ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_inactive_members():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members WHERE status = 'inactive' ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_warned_members():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM members
        WHERE status = 'active' AND months_unpaid >= 1
        ORDER BY months_unpaid DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def mark_paid(member_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE members
        SET paid = 1, months_unpaid = 0
        WHERE id = ?
    """, (member_id,))
    conn.commit()
    conn.close()

def soft_remove_member(member_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE members SET status = 'inactive' WHERE id = ?
    """, (member_id,))
    conn.commit()
    conn.close()

def reactivate_member(member_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE members
        SET status = 'active', months_unpaid = 0, paid = 0
        WHERE id = ?
    """, (member_id,))
    conn.commit()
    conn.close()

def run_monthly_check():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE members
        SET months_unpaid = months_unpaid + 1
        WHERE status = 'active' AND paid = 0
    """)
    cursor.execute("""
        UPDATE members
        SET status = 'inactive'
        WHERE status = 'active' AND months_unpaid >= 2
    """)
    cursor.execute("""
        UPDATE members SET paid = 0 WHERE status = 'active'
    """)
    conn.commit()
    conn.close()
    print("Monthly check done!")

def show_members():
    members = get_all_members()
    for m in members:
        print(f"ID:{m['id']} | {m['name']} | {m['membership_type']} | ₹{m['total_fee']}")
from database import get_connection
from datetime import datetime, timedelta

PLANS = {
    "monthly":     {"fee": 700,  "admission": 200, "label": "Monthly",     "days": 30},
    "quarterly":   {"fee": 1800, "admission": 0,   "label": "Quarterly",   "days": 90},
    "half_yearly": {"fee": 3400, "admission": 0,   "label": "Half Yearly", "days": 180},
    "yearly":      {"fee": 6000, "admission": 0,   "label": "Yearly",      "days": 365},
}

def setup():
    pass

# MEMBER REGISTRATION
def register_member(name, username, phone, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO members (name, username, phone, password, status)
            VALUES (?, ?, ?, ?, 'unverified')
        """, (name, username, phone, password))
        conn.commit()
        conn.close()
        return True, "Registration successful!"
    except Exception as e:
        conn.close()
        return False, "Username already taken!"

# MEMBER LOGIN
def member_login(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members WHERE username = ? AND password = ?", (username, password))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

# GET MEMBER BY ID
def get_member_by_id(member_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members WHERE id = ?", (member_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

# CHANGE PASSWORD
def change_password(member_id, old_password, new_password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members WHERE id = ? AND password = ?", (member_id, old_password))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return False, "Old password is wrong!"
    cursor.execute("UPDATE members SET password = ? WHERE id = ?", (new_password, member_id))
    conn.commit()
    conn.close()
    return True, "Password changed!"

# SELECT PLAN AFTER PAYMENT
def select_plan(member_id, membership_type, is_first_month=True):
    plan = PLANS[membership_type]
    fee = plan["fee"]
    admission = plan["admission"] if is_first_month and membership_type == "monthly" else 0
    total = fee + admission
    expiry = (datetime.now() + timedelta(days=plan["days"])).strftime("%d-%m-%Y")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE members
        SET membership_type=?, fee=?, admission_fee=?, total_fee=?,
            paid=0, status='active', expiry_date=?
        WHERE id=?
    """, (membership_type, fee, admission, total, expiry, member_id))
    conn.commit()
    conn.close()
    return total, expiry

# MARK PAID BY OWNER
def mark_paid(member_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE members SET paid=1, months_unpaid=0 WHERE id=?", (member_id,))
    conn.commit()
    conn.close()

# OWNER - GET ALL ACTIVE MEMBERS
def get_all_members():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members WHERE status='active' ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# OWNER - GET UNVERIFIED (registered but no plan)
def get_unverified_members():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members WHERE status='unverified' ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# OWNER - GET INACTIVE
def get_inactive_members():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members WHERE status='inactive' ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# OWNER - GET WARNED
def get_warned_members():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members WHERE status='active' AND months_unpaid >= 1")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# SOFT REMOVE
def soft_remove_member(member_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE members SET status='inactive' WHERE id=?", (member_id,))
    conn.commit()
    conn.close()

# REACTIVATE
def reactivate_member(member_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE members SET status='active', months_unpaid=0, paid=0 WHERE id=?", (member_id,))
    conn.commit()
    conn.close()

# MONTHLY CHECK
def run_monthly_check():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE members SET months_unpaid=months_unpaid+1 WHERE status='active' AND paid=0")
    cursor.execute("UPDATE members SET status='inactive' WHERE status='active' AND months_unpaid >= 2")
    cursor.execute("UPDATE members SET paid=0 WHERE status='active'")
    conn.commit()
    conn.close()
#get all pass
def get_all_members_with_passwords():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members ORDER BY status, id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
def show_members():
    pass
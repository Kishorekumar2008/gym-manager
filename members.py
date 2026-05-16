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
    except:
        conn.close()
        return False, "Username already taken!"

def member_login(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members WHERE username=? AND password=?", (username, password))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_member_by_id(member_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members WHERE id=?", (member_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def change_password(member_id, old_password, new_password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members WHERE id=? AND password=?", (member_id, old_password))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return False, "Old password is wrong!"
    cursor.execute("UPDATE members SET password=? WHERE id=?", (new_password, member_id))
    conn.commit()
    conn.close()
    return True, "Password changed successfully!"

def select_plan(member_id, membership_type, is_first_month=True):
    plan = PLANS[membership_type]
    fee = plan["fee"]
    admission = plan["admission"] if is_first_month and membership_type == "monthly" else 0
    total = fee + admission
    member = get_member_by_id(member_id)
    # Extend existing plan if already has one
    if member["expiry_date"]:
        try:
            existing_expiry = datetime.strptime(member["expiry_date"], "%d-%m-%Y")
            if existing_expiry > datetime.now():
                new_expiry = existing_expiry + timedelta(days=plan["days"])
            else:
                new_expiry = datetime.now() + timedelta(days=plan["days"])
        except:
            new_expiry = datetime.now() + timedelta(days=plan["days"])
    else:
        new_expiry = datetime.now() + timedelta(days=plan["days"])
    expiry = new_expiry.strftime("%d-%m-%Y")
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

def create_payment_request(member_id, member_name, membership_type, total_fee, payment_method):
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now().strftime("%d-%m-%Y")
    cursor.execute("""
        INSERT INTO payment_requests
        (member_id, member_name, membership_type, total_fee, payment_method, status, date)
        VALUES (?, ?, ?, ?, ?, 'pending', ?)
    """, (member_id, member_name, membership_type, total_fee, payment_method, today))
    conn.commit()
    conn.close()

def get_pending_payments():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM payment_requests WHERE status='pending' ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def approve_payment(request_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM payment_requests WHERE id=?", (request_id,))
    req = cursor.fetchone()
    if req:
        cursor.execute("UPDATE members SET paid=1, months_unpaid=0, status='active' WHERE id=?", (req["member_id"],))
        cursor.execute("UPDATE payment_requests SET status='approved' WHERE id=?", (request_id,))
    conn.commit()
    conn.close()

def mark_paid(member_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE members SET paid=1, months_unpaid=0 WHERE id=?", (member_id,))
    conn.commit()
    conn.close()

def get_all_members():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members WHERE status='active' ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_unverified_members():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members WHERE status='unverified' ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_inactive_members():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members WHERE status='inactive' ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_warned_members():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members WHERE status='active' AND months_unpaid>=1")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_all_members_with_passwords():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members ORDER BY status, id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def soft_remove_member(member_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE members SET status='inactive' WHERE id=?", (member_id,))
    conn.commit()
    conn.close()

def reactivate_member(member_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE members SET status='active', months_unpaid=0, paid=0 WHERE id=?", (member_id,))
    conn.commit()
    conn.close()

def run_monthly_check():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE members SET months_unpaid=months_unpaid+1 WHERE status='active' AND paid=0")
    cursor.execute("UPDATE members SET status='inactive' WHERE status='active' AND months_unpaid>=2")
    cursor.execute("UPDATE members SET paid=0 WHERE status='active'")
    conn.commit()
    conn.close()

def show_members():
    pass
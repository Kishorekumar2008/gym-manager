from database import get_connection
from datetime import datetime

def setup():
    pass

def get_current_session():
    hour = datetime.now().hour
    if 5 <= hour < 10:
        return "morning"
    elif 16 <= hour < 22:
        return "evening"
    return None

def check_in(member_id, member_name):
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now().strftime("%d-%m-%Y")
    now_time = datetime.now().strftime("%H:%M")
    now = datetime.now()
    session = get_current_session()
    if not session:
        conn.close()
        return False, "Gym is closed! Open: Morning 5AM-10AM · Evening 4PM-10PM"
    cursor.execute("""
        SELECT * FROM attendance
        WHERE member_id=? AND date=? AND status='present' AND check_out IS NULL
    """, (member_id, today))
    existing = cursor.fetchone()
    if existing:
        conn.close()
        return False, "You are already checked in!"
    cursor.execute("""
        INSERT INTO attendance
        (member_id, member_name, date, check_in, status, month, year)
        VALUES (?, ?, ?, ?, 'present', ?, ?)
    """, (member_id, member_name, today, now_time, now.strftime("%B"), now.year))
    conn.commit()
    conn.close()
    return True, f"Checked in at {now_time} ✅"

def check_out(member_id):
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now().strftime("%d-%m-%Y")
    now_time = datetime.now().strftime("%H:%M")
    cursor.execute("""
        SELECT * FROM attendance
        WHERE member_id=? AND date=? AND check_out IS NULL AND status='present'
        ORDER BY id DESC LIMIT 1
    """, (member_id, today))
    record = cursor.fetchone()
    if not record:
        conn.close()
        return False, "You haven't checked in yet!"
    cursor.execute("UPDATE attendance SET check_out=? WHERE id=?", (now_time, record["id"]))
    conn.commit()
    conn.close()
    return True, f"Checked out at {now_time} 👋"

def mark_leave(member_id, member_name, remark=""):
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now().strftime("%d-%m-%Y")
    now = datetime.now()
    cursor.execute("""
        SELECT * FROM attendance WHERE member_id=? AND date=?
    """, (member_id, today))
    existing = cursor.fetchone()
    if existing:
        conn.close()
        return False, "Attendance already marked for today!"
    cursor.execute("""
        INSERT INTO attendance
        (member_id, member_name, date, status, remark, month, year)
        VALUES (?, ?, ?, 'leave', ?, ?, ?)
    """, (member_id, member_name, today, remark, now.strftime("%B"), now.year))
    conn.commit()
    conn.close()
    return True, "Leave marked successfully!"

def auto_mark_absent():
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now()
    today = now.strftime("%d-%m-%Y")
    hour = now.hour
    if hour >= 22:
        from members import get_all_members
        all_members = get_all_members()
        for m in all_members:
            cursor.execute("""
                SELECT * FROM attendance WHERE member_id=? AND date=?
            """, (m["id"], today))
            existing = cursor.fetchone()
            if not existing:
                cursor.execute("""
                    INSERT INTO attendance
                    (member_id, member_name, date, status, remark, month, year, auto_checkout)
                    VALUES (?, ?, ?, 'absent', 'Auto marked absent at gym closing', ?, ?, 1)
                """, (m["id"], m["name"], today, now.strftime("%B"), now.year))
            elif existing["status"] == "present" and not existing["check_out"]:
                cursor.execute("""
                    UPDATE attendance SET check_out='22:00', auto_checkout=1 WHERE id=?
                """, (existing["id"],))
    conn.commit()
    conn.close()

def auto_checkout_all():
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now().strftime("%d-%m-%Y")
    cursor.execute("""
        UPDATE attendance SET check_out='22:00 (Auto)', auto_checkout=1
        WHERE date=? AND check_out IS NULL AND status='present'
    """, (today,))
    conn.commit()
    conn.close()

def get_today_attendance():
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now().strftime("%d-%m-%Y")
    cursor.execute("SELECT * FROM attendance WHERE date=? ORDER BY id DESC", (today,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_member_attendance(member_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM attendance WHERE member_id=?
        ORDER BY id DESC LIMIT 30
    """, (member_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_member_today(member_id):
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now().strftime("%d-%m-%Y")
    cursor.execute("""
        SELECT * FROM attendance WHERE member_id=? AND date=?
        ORDER BY id DESC LIMIT 1
    """, (member_id, today))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None
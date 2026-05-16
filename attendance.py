from database import get_connection
from datetime import datetime

MORNING_CLOSE = "10:00"
EVENING_CLOSE = "22:00"

def setup():
    pass

def get_current_session():
    now = datetime.now()
    hour = now.hour
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
    month = now.strftime("%B")
    year = now.year
    session = get_current_session()
    if not session:
        conn.close()
        return False, "Gym is closed! Open: Morning 5AM-10AM, Evening 4PM-10PM"
    cursor.execute("""
        SELECT * FROM attendance
        WHERE member_id=? AND date=? AND check_out IS NULL
    """, (member_id, today))
    existing = cursor.fetchone()
    if existing:
        conn.close()
        return False, "You are already checked in!"
    cursor.execute("""
        INSERT INTO attendance (member_id, member_name, date, check_in, month, year)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (member_id, member_name, today, now_time, month, year))
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
        WHERE member_id=? AND date=? AND check_out IS NULL
        ORDER BY id DESC LIMIT 1
    """, (member_id, today))
    record = cursor.fetchone()
    if not record:
        conn.close()
        return False, "You haven't checked in yet!"
    cursor.execute("""
        UPDATE attendance SET check_out=? WHERE id=?
    """, (now_time, record["id"]))
    conn.commit()
    conn.close()
    return True, f"Checked out at {now_time} 👋"

def auto_checkout_all():
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now().strftime("%d-%m-%Y")
    now = datetime.now()
    hour = now.hour
    if hour == 10 or hour == 22:
        checkout_time = f"{hour:02d}:00 (Auto)"
        cursor.execute("""
            UPDATE attendance SET check_out=?, auto_checkout=1
            WHERE date=? AND check_out IS NULL
        """, (checkout_time, today))
        conn.commit()
    conn.close()

def get_today_attendance():
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now().strftime("%d-%m-%Y")
    cursor.execute("SELECT * FROM attendance WHERE date=? ORDER BY check_in DESC", (today,))
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
        SELECT * FROM attendance
        WHERE member_id=? AND date=?
        ORDER BY id DESC LIMIT 1
    """, (member_id, today))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None
from database import get_connection
from datetime import datetime

def setup():
    pass

def mark_attendance(member_id, member_name):
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now().strftime("%d-%m-%Y")
    cursor.execute("""
        SELECT * FROM attendance
        WHERE member_id = ? AND date = ?
    """, (member_id, today))
    existing = cursor.fetchone()
    if existing:
        print(f"{member_name} already marked today!")
        conn.close()
        return
    now = datetime.now()
    cursor.execute("""
        INSERT INTO attendance (member_id, member_name, date, month, year)
        VALUES (?, ?, ?, ?, ?)
    """, (member_id, member_name, today, now.strftime("%B"), now.year))
    conn.commit()
    conn.close()
    print(f"{member_name} marked present!")

def get_today_attendance():
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now().strftime("%d-%m-%Y")
    cursor.execute("SELECT * FROM attendance WHERE date = ?", (today,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def show_today():
    today_list = get_today_attendance()
    today = datetime.now().strftime("%d-%m-%Y")
    print(f"\n===== TODAY'S ATTENDANCE ({today}) =====")
    if len(today_list) == 0:
        print("Nobody present yet!")
    else:
        for r in today_list:
            print(f"{r['member_name']}")
        print(f"Total: {len(today_list)}")
    print("==========================================\n")

def member_history(member_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendance WHERE member_id = ?", (member_id,))
    rows = cursor.fetchall()
    conn.close()
    records = [dict(row) for row in rows]
    print(f"\n===== ATTENDANCE HISTORY =====")
    for r in records:
        print(f"{r['date']}")
    print(f"Total days: {len(records)}\n")

def inactive_members():
    from members import get_all_members
    conn = get_connection()
    cursor = conn.cursor()
    all_members = get_all_members()
    today = datetime.now()
    print("\n===== INACTIVE MEMBERS =====")
    found = False
    for m in all_members:
        cursor.execute("""
            SELECT * FROM attendance
            WHERE member_id = ?
            ORDER BY id DESC LIMIT 1
        """, (m["id"],))
        last = cursor.fetchone()
        if not last:
            print(f"{m['name']} — Never attended!")
            found = True
        else:
            last_date = datetime.strptime(last["date"], "%d-%m-%Y")
            days = (today - last_date).days
            if days >= 7:
                print(f"{m['name']} — Last came {days} days ago!")
                found = True
    if not found:
        print("All members active!")
    conn.close()
    print("============================\n")
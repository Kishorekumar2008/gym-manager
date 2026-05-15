import json
import os
from datetime import datetime

ATTENDANCE_FILE = "data/attendance.json"

def setup():
    if not os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, "w") as f:
            json.dump([], f)

# Mark a member as present today
def mark_attendance(member_id, member_name):
    setup()
    with open(ATTENDANCE_FILE, "r") as f:
        records = json.load(f)
    today = datetime.now().strftime("%d-%m-%Y")
    # Check if already marked today
    for r in records:
        if r["member_id"] == member_id and r["date"] == today:
            print(f"{member_name} already marked present today!")
            return
    entry = {
        "member_id": member_id,
        "member_name": member_name,
        "date": today,
        "month": datetime.now().strftime("%B"),
        "year": datetime.now().year
    }
    records.append(entry)
    with open(ATTENDANCE_FILE, "w") as f:
        json.dump(records, f)
    print(f"✅ {member_name} marked present for {today}!")

# Show today's attendance
def show_today():
    setup()
    with open(ATTENDANCE_FILE, "r") as f:
        records = json.load(f)
    today = datetime.now().strftime("%d-%m-%Y")
    today_list = [r for r in records if r["date"] == today]
    print(f"\n===== TODAY'S ATTENDANCE ({today}) =====")
    if len(today_list) == 0:
        print("Nobody marked present yet!")
    else:
        for r in today_list:
            print(f"✅ {r['member_name']}")
        print(f"\nTotal present: {len(today_list)}")
    print("==========================================\n")

# Show attendance history of one member
def member_history(member_id):
    setup()
    with open(ATTENDANCE_FILE, "r") as f:
        records = json.load(f)
    history = [r for r in records if r["member_id"] == member_id]
    print(f"\n===== ATTENDANCE HISTORY =====")
    if len(history) == 0:
        print("No attendance records found!")
    else:
        for r in history:
            print(f"📅 {r['date']}")
        print(f"\nTotal days attended: {len(history)}")
    print("==============================\n")

# Show members who havent come in 7 days
def inactive_members():
    setup()
    from members import get_all_members
    with open(ATTENDANCE_FILE, "r") as f:
        records = json.load(f)
    all_members = get_all_members()
    today = datetime.now()
    print("\n===== INACTIVE MEMBERS (7+ days absent) =====")
    found = False
    for m in all_members:
        member_records = [r for r in records if r["member_id"] == m["id"]]
        if len(member_records) == 0:
            print(f"⚠️  {m['name']} — Never attended!")
            found = True
        else:
            last_date = datetime.strptime(member_records[-1]["date"], "%d-%m-%Y")
            days_absent = (today - last_date).days
            if days_absent >= 7:
                print(f"⚠️  {m['name']} — Last came {days_absent} days ago!")
                found = True
    if not found:
        print("All members are active! 💪")
    print("==============================================\n")
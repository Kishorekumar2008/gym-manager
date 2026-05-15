import json
import os

# This is where we store members data
DATA_FILE = "data/members.json"

# This runs when app starts - creates file if not exists
def setup():
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)

# Add a new member to the gym
def add_member(name, phone, membership_type, fee):
    members = get_all_members()
    member = {
        "id": len(members) + 1,
        "name": name,
        "phone": phone,
        "membership_type": membership_type,
        "fee": fee,
        "paid": False
    }
    members.append(member)
    with open(DATA_FILE, "w") as f:
        json.dump(members, f)
    print(f"Member {name} added successfully!")

# Get all members from file
def get_all_members():
    setup()
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Show all members on screen
def show_members():
    members = get_all_members()
    if len(members) == 0:
        print("No members yet!")
        return
    print("\n===== GYM MEMBERS =====")
    for m in members:
        status = "✅ PAID" if m["paid"] else "❌ NOT PAID"
        print(f"ID:{m['id']} | {m['name']} | {m['phone']} | {m['membership_type']} | ₹{m['fee']} | {status}")
    print("=======================\n")

# Mark a member as paid
def mark_paid(member_id):
    members = get_all_members()
    for m in members:
        if m["id"] == member_id:
            m["paid"] = True
            print(f"{m['name']} marked as PAID!")
    with open(DATA_FILE, "w") as f:
        json.dump(members, f)
from members import get_all_members
from datetime import datetime

# Search member by name or phone
def search_member(keyword):
    members = get_all_members()
    keyword = keyword.lower()
    results = []
    for m in members:
        if keyword in m["name"].lower() or keyword in m["phone"]:
            results.append(m)
    print(f"\n===== SEARCH RESULTS FOR '{keyword}' =====")
    if len(results) == 0:
        print("No members found!")
    else:
        for m in results:
            status = "✅ PAID" if m["paid"] else "❌ NOT PAID"
            print(f"ID:{m['id']} | {m['name']} | {m['phone']} | {m['membership_type']} | ₹{m['fee']} | {status}")
    print("==========================================\n")

# Show all unpaid members
def show_unpaid():
    members = get_all_members()
    unpaid = [m for m in members if not m["paid"]]
    print("\n===== ⚠️  UNPAID MEMBERS =====")
    if len(unpaid) == 0:
        print("All members have paid! 🎉")
    else:
        total_pending = 0
        for m in unpaid:
            print(f"❌ ID:{m['id']} | {m['name']} | {m['phone']} | ₹{m['fee']} PENDING")
            total_pending += m["fee"]
        print(f"\nTotal pending amount: ₹{total_pending}")
    print("================================\n")

# Show payment summary
def payment_summary():
    members = get_all_members()
    paid = [m for m in members if m["paid"]]
    unpaid = [m for m in members if not m["paid"]]
    total_collected = sum(m["fee"] for m in paid)
    total_pending = sum(m["fee"] for m in unpaid)
    print("\n===== 💰 PAYMENT SUMMARY =====")
    print(f"Total Members  : {len(members)}")
    print(f"Paid           : {len(paid)} members")
    print(f"Unpaid         : {len(unpaid)} members")
    print(f"Total Collected: ₹{total_collected}")
    print(f"Total Pending  : ₹{total_pending}")
    print("================================\n")
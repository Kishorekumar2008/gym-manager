from members import get_all_members
from finance import show_monthly_income
from expense import show_monthly_expenses, get_monthly_expense_total
from attendance import show_today
from datetime import datetime
import json

def full_report():
    print("\n")
    print("=" * 50)
    print("       🏋️  GYM MANAGER FULL REPORT 🏋️")
    print(f"       {datetime.now().strftime('%d %B %Y - %I:%M %p')}")
    print("=" * 50)

    # Members summary
    members = get_all_members()
    paid = [m for m in members if m["paid"]]
    unpaid = [m for m in members if not m["paid"]]
    print(f"\n👥 MEMBERS")
    print(f"   Total    : {len(members)}")
    print(f"   Paid     : {len(paid)}")
    print(f"   Unpaid   : {len(unpaid)}")

    # Finance summary
    with open("data/finance.json", "r") as f:
        finance_records = json.load(f)
    current_month = datetime.now().strftime("%B")
    current_year = datetime.now().year
    monthly_income = sum(r["amount"] for r in finance_records
                        if r["month"] == current_month and r["year"] == current_year)
    monthly_expense = get_monthly_expense_total()
    profit = monthly_income - monthly_expense

    print(f"\n💰 FINANCE ({current_month} {current_year})")
    print(f"   Income   : ₹{monthly_income}")
    print(f"   Expenses : ₹{monthly_expense}")
    print(f"   Profit   : ₹{profit}")
    if profit > 0:
        print(f"   Status   : 📈 PROFITABLE")
    else:
        print(f"   Status   : 📉 LOSS")

    # Attendance today
    with open("data/attendance.json", "r") as f:
        att_records = json.load(f)
    today = datetime.now().strftime("%d-%m-%Y")
    today_count = len([r for r in att_records if r["date"] == today])
    print(f"\n📅 ATTENDANCE TODAY")
    print(f"   Present  : {today_count} members")

    # Pending fees
    total_pending = sum(m["fee"] for m in unpaid)
    print(f"\n⚠️  PENDING FEES")
    print(f"   Amount   : ₹{total_pending} from {len(unpaid)} members")

    print("\n" + "=" * 50 + "\n")
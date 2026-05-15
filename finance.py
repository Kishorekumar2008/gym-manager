import json
import os
from datetime import datetime

FINANCE_FILE = "data/finance.json"

def setup():
    if not os.path.exists(FINANCE_FILE):
        with open(FINANCE_FILE, "w") as f:
            json.dump([], f)

# Record an income entry
def add_income(source, amount):
    setup()
    with open(FINANCE_FILE, "r") as f:
        records = json.load(f)
    entry = {
        "type": "income",
        "source": source,
        "amount": amount,
        "month": datetime.now().strftime("%B"),
        "year": datetime.now().year,
        "date": datetime.now().strftime("%d-%m-%Y")
    }
    records.append(entry)
    with open(FINANCE_FILE, "w") as f:
        json.dump(records, f)
    print(f"Income of ₹{amount} recorded!")

# Show monthly income
def show_monthly_income():
    setup()
    with open(FINANCE_FILE, "r") as f:
        records = json.load(f)
    current_month = datetime.now().strftime("%B")
    current_year = datetime.now().year
    total = 0
    print(f"\n===== INCOME FOR {current_month} {current_year} =====")
    for r in records:
        if r["month"] == current_month and r["year"] == current_year:
            print(f"{r['date']} | {r['source']} | ₹{r['amount']}")
            total += r["amount"]
    print(f"TOTAL: ₹{total}")
    print("================================\n")

# Compare this year vs last year
def yearly_comparison():
    setup()
    with open(FINANCE_FILE, "r") as f:
        records = json.load(f)
    this_year = datetime.now().year
    last_year = this_year - 1
    this_total = sum(r["amount"] for r in records if r["year"] == this_year)
    last_total = sum(r["amount"] for r in records if r["year"] == last_year)
    print(f"\n===== YEARLY COMPARISON =====")
    print(f"{last_year}: ₹{last_total}")
    print(f"{this_year}: ₹{this_total}")
    if this_total > last_total:
        print(f"📈 UP by ₹{this_total - last_total}")
    else:
        print(f"📉 DOWN by ₹{last_total - this_total}")
    print("==============================\n")
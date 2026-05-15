import json
import os
from datetime import datetime

EXPENSE_FILE = "data/expenses.json"

def setup():
    if not os.path.exists(EXPENSE_FILE):
        with open(EXPENSE_FILE, "w") as f:
            json.dump([], f)

def add_expense(category, description, amount):
    setup()
    with open(EXPENSE_FILE, "r") as f:
        records = json.load(f)
    entry = {
        "category": category,
        "description": description,
        "amount": amount,
        "month": datetime.now().strftime("%B"),
        "year": datetime.now().year,
        "date": datetime.now().strftime("%d-%m-%Y")
    }
    records.append(entry)
    with open(EXPENSE_FILE, "w") as f:
        json.dump(records, f)
    print(f"Expense of ₹{amount} recorded!")

def show_monthly_expenses():
    setup()
    with open(EXPENSE_FILE, "r") as f:
        records = json.load(f)
    current_month = datetime.now().strftime("%B")
    current_year = datetime.now().year
    total = 0
    print(f"\n===== EXPENSES FOR {current_month} {current_year} =====")
    for r in records:
        if r["month"] == current_month and r["year"] == current_year:
            print(f"{r['date']} | {r['category']} | {r['description']} | ₹{r['amount']}")
            total += r["amount"]
    print(f"TOTAL EXPENSES: ₹{total}")
    print("==========================================\n")
    return total

def get_monthly_expense_total():
    setup()
    with open(EXPENSE_FILE, "r") as f:
        records = json.load(f)
    current_month = datetime.now().strftime("%B")
    current_year = datetime.now().year
    return sum(r["amount"] for r in records if r["month"] == current_month and r["year"] == current_year)
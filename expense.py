from database import get_connection
from datetime import datetime

def setup():
    pass

def add_expense(category, description, amount):
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now()
    cursor.execute("""
        INSERT INTO expenses (category, description, amount, month, year, date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (category, description, amount, now.strftime("%B"), now.year, now.strftime("%d-%m-%Y")))
    conn.commit()
    conn.close()
    print(f"Expense ₹{amount} recorded!")

def get_monthly_expenses():
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now()
    cursor.execute("""
        SELECT * FROM expenses
        WHERE month = ? AND year = ?
    """, (now.strftime("%B"), now.year))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def show_monthly_expenses():
    records = get_monthly_expenses()
    total = sum(r["amount"] for r in records)
    now = datetime.now()
    print(f"\n===== EXPENSES {now.strftime('%B %Y')} =====")
    for r in records:
        print(f"{r['date']} | {r['category']} | {r['description']} | ₹{r['amount']}")
    print(f"TOTAL: ₹{total}\n")
    return total

def get_monthly_expense_total():
    records = get_monthly_expenses()
    return sum(r["amount"] for r in records)
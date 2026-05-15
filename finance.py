from database import get_connection
from datetime import datetime

def setup():
    pass

def add_income(source, amount):
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now()
    cursor.execute("""
        INSERT INTO finance (source, amount, month, year, date)
        VALUES (?, ?, ?, ?, ?)
    """, (source, amount, now.strftime("%B"), now.year, now.strftime("%d-%m-%Y")))
    conn.commit()
    conn.close()
    print(f"Income ₹{amount} recorded!")

def get_monthly_income():
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now()
    cursor.execute("""
        SELECT * FROM finance
        WHERE month = ? AND year = ?
    """, (now.strftime("%B"), now.year))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def show_monthly_income():
    records = get_monthly_income()
    now = datetime.now()
    total = 0
    print(f"\n===== INCOME FOR {now.strftime('%B %Y')} =====")
    for r in records:
        print(f"{r['date']} | {r['source']} | ₹{r['amount']}")
        total += r["amount"]
    print(f"TOTAL: ₹{total}\n")

def get_monthly_total():
    records = get_monthly_income()
    return sum(r["amount"] for r in records)

def yearly_comparison():
    conn = get_connection()
    cursor = conn.cursor()
    this_year = datetime.now().year
    last_year = this_year - 1
    cursor.execute("SELECT SUM(amount) as total FROM finance WHERE year = ?", (this_year,))
    this_total = cursor.fetchone()["total"] or 0
    cursor.execute("SELECT SUM(amount) as total FROM finance WHERE year = ?", (last_year,))
    last_total = cursor.fetchone()["total"] or 0
    conn.close()
    print(f"\n===== YEARLY COMPARISON =====")
    print(f"{last_year}: ₹{last_total}")
    print(f"{this_year}: ₹{this_total}")
    if this_total > last_total:
        print(f"UP by ₹{this_total - last_total}")
    else:
        print(f"DOWN by ₹{last_total - this_total}")
    print("==============================\n")
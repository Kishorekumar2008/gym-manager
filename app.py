from flask import Flask, render_template, request, redirect, url_for
import members
import finance
import attendance
import expense
import reports
import search

app = Flask(__name__)

# Setup all data files when app starts
members.setup()
finance.setup()
attendance.setup()
expense.setup()

# HOME PAGE - shows full report
@app.route("/")
def home():
    all_members = members.get_all_members()
    paid = [m for m in all_members if m["paid"]]
    unpaid = [m for m in all_members if not m["paid"]]
    total_members = len(all_members)
    total_paid = len(paid)
    total_unpaid = len(unpaid)
    total_pending = sum(m["fee"] for m in unpaid)
    total_collected = sum(m["fee"] for m in paid)
    return render_template("home.html",
        total_members=total_members,
        total_paid=total_paid,
        total_unpaid=total_unpaid,
        total_pending=total_pending,
        total_collected=total_collected
    )

# MEMBERS PAGE
@app.route("/members")
def show_members():
    all_members = members.get_all_members()
    return render_template("members.html", members=all_members)

# ADD MEMBER
@app.route("/add_member", methods=["GET", "POST"])
def add_member():
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        membership = request.form["membership"]
        fee = int(request.form["fee"])
        members.add_member(name, phone, membership, fee)
        return redirect(url_for("show_members"))
    return render_template("add_member.html")

# MARK PAID
@app.route("/mark_paid/<int:member_id>")
def mark_paid(member_id):
    members.mark_paid(member_id)
    return redirect(url_for("show_members"))

# ATTENDANCE PAGE
@app.route("/attendance")
def show_attendance():
    from datetime import datetime
    import json
    with open("data/attendance.json", "r") as f:
        records = json.load(f)
    today = datetime.now().strftime("%d-%m-%Y")
    today_list = [r for r in records if r["date"] == today]
    all_members = members.get_all_members()
    return render_template("attendance.html",
        today_list=today_list,
        all_members=all_members,
        today=today
    )

# MARK ATTENDANCE
@app.route("/mark_attendance/<int:member_id>/<string:name>")
def mark_attendance(member_id, name):
    attendance.mark_attendance(member_id, name)
    return redirect(url_for("show_attendance"))

# FINANCE PAGE
@app.route("/finance")
def show_finance():
    from datetime import datetime
    import json
    with open("data/finance.json", "r") as f:
        records = json.load(f)
    current_month = datetime.now().strftime("%B")
    current_year = datetime.now().year
    monthly = [r for r in records if r["month"] == current_month and r["year"] == current_year]
    total_income = sum(r["amount"] for r in monthly)
    total_expense = expense.get_monthly_expense_total()
    profit = total_income - total_expense
    return render_template("finance.html",
        records=monthly,
        total_income=total_income,
        total_expense=total_expense,
        profit=profit,
        month=current_month,
        year=current_year
    )

# ADD INCOME
@app.route("/add_income", methods=["GET", "POST"])
def add_income():
    if request.method == "POST":
        source = request.form["source"]
        amount = int(request.form["amount"])
        finance.add_income(source, amount)
        return redirect(url_for("show_finance"))
    return render_template("add_income.html")

# EXPENSES PAGE
@app.route("/expenses")
def show_expenses():
    from datetime import datetime
    import json
    with open("data/expenses.json", "r") as f:
        records = json.load(f)
    current_month = datetime.now().strftime("%B")
    current_year = datetime.now().year
    monthly = [r for r in records if r["month"] == current_month and r["year"] == current_year]
    total = sum(r["amount"] for r in monthly)
    return render_template("expenses.html",
        records=monthly,
        total=total,
        month=current_month
    )

# ADD EXPENSE
@app.route("/add_expense", methods=["GET", "POST"])
def add_expense():
    if request.method == "POST":
        category = request.form["category"]
        description = request.form["description"]
        amount = int(request.form["amount"])
        expense.add_expense(category, description, amount)
        return redirect(url_for("show_expenses"))
    return render_template("add_expense.html")

# UNPAID MEMBERS
@app.route("/unpaid")
def show_unpaid():
    all_members = members.get_all_members()
    unpaid = [m for m in all_members if not m["paid"]]
    total_pending = sum(m["fee"] for m in unpaid)
    return render_template("unpaid.html",
        unpaid=unpaid,
        total_pending=total_pending
    )

if __name__ == "__main__":
    app.run(debug=True)
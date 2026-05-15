from flask import Flask, render_template, request, redirect, url_for
from database import setup_database
import members
import finance
import attendance
import expense
import search
from datetime import datetime

app = Flask(__name__)
setup_database()

@app.route("/")
def home():
    all_members = members.get_all_members()
    paid = [m for m in all_members if m["paid"]]
    unpaid = [m for m in all_members if not m["paid"]]
    total_collected = sum(m["fee"] for m in paid)
    total_pending = sum(m["fee"] for m in unpaid)
    return render_template("home.html",
        total_members=len(all_members),
        total_paid=len(paid),
        total_unpaid=len(unpaid),
        total_collected=total_collected,
        total_pending=total_pending
    )

@app.route("/members")
def show_members():
    all_members = members.get_all_members()
    return render_template("members.html", members=all_members)

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

@app.route("/mark_paid/<int:member_id>")
def mark_paid(member_id):
    members.mark_paid(member_id)
    return redirect(url_for("show_members"))

@app.route("/attendance")
def show_attendance():
    today = datetime.now().strftime("%d-%m-%Y")
    today_list = attendance.get_today_attendance()
    all_members = members.get_all_members()
    return render_template("attendance.html",
        today_list=today_list,
        all_members=all_members,
        today=today
    )

@app.route("/mark_attendance/<int:member_id>/<string:name>")
def mark_attendance(member_id, name):
    attendance.mark_attendance(member_id, name)
    return redirect(url_for("show_attendance"))

@app.route("/finance")
def show_finance():
    now = datetime.now()
    records = finance.get_monthly_income()
    total_income = sum(r["amount"] for r in records)
    total_expense = expense.get_monthly_expense_total()
    profit = total_income - total_expense
    return render_template("finance.html",
        records=records,
        total_income=total_income,
        total_expense=total_expense,
        profit=profit,
        month=now.strftime("%B"),
        year=now.year
    )

@app.route("/add_income", methods=["GET", "POST"])
def add_income():
    if request.method == "POST":
        source = request.form["source"]
        amount = int(request.form["amount"])
        finance.add_income(source, amount)
        return redirect(url_for("show_finance"))
    return render_template("add_income.html")

@app.route("/expenses")
def show_expenses():
    now = datetime.now()
    records = expense.get_monthly_expenses()
    total = sum(r["amount"] for r in records)
    return render_template("expenses.html",
        records=records,
        total=total,
        month=now.strftime("%B")
    )

@app.route("/add_expense", methods=["GET", "POST"])
def add_expense():
    if request.method == "POST":
        category = request.form["category"]
        description = request.form["description"]
        amount = int(request.form["amount"])
        expense.add_expense(category, description, amount)
        return redirect(url_for("show_expenses"))
    return render_template("add_expense.html")

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
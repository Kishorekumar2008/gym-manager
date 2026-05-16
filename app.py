from flask import Flask, render_template, request, redirect, url_for
from database import setup_database
import members
import finance
import attendance
import expense
from datetime import datetime

app = Flask(__name__)
setup_database()

PLANS = members.PLANS

@app.route("/")
def home():
    all_members = members.get_all_members()
    paid = [m for m in all_members if m["paid"]]
    unpaid = [m for m in all_members if not m["paid"]]
    warned = members.get_warned_members()
    inactive = members.get_inactive_members()
    total_collected = sum(m["total_fee"] for m in paid)
    total_pending = sum(m["total_fee"] for m in unpaid)
    monthly_income = finance.get_monthly_total()
    monthly_expense = expense.get_monthly_expense_total()
    profit = monthly_income - monthly_expense
    today_att = attendance.get_today_attendance()
    return render_template("home.html",
        total_members=len(all_members),
        total_paid=len(paid),
        total_unpaid=len(unpaid),
        total_warned=len(warned),
        total_inactive=len(inactive),
        total_collected=total_collected,
        total_pending=total_pending,
        monthly_income=monthly_income,
        monthly_expense=monthly_expense,
        profit=profit,
        today_count=len(today_att)
    )

@app.route("/members")
def show_members():
    all_members = members.get_all_members()
    warned = members.get_warned_members()
    warned_ids = [m["id"] for m in warned]
    return render_template("members.html",
        members=all_members,
        warned_ids=warned_ids,
        plans=PLANS
    )

@app.route("/add_member", methods=["GET", "POST"])
def add_member():
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        membership = request.form["membership"]
        is_first = "admission" in request.form
        members.add_member(name, phone, membership, is_first)
        return redirect(url_for("show_members"))
    return render_template("add_member.html", plans=PLANS)

@app.route("/mark_paid/<int:member_id>")
def mark_paid(member_id):
    members.mark_paid(member_id)
    return redirect(url_for("show_members"))

@app.route("/soft_remove/<int:member_id>")
def soft_remove(member_id):
    members.soft_remove_member(member_id)
    return redirect(url_for("show_members"))

@app.route("/inactive")
def inactive_members():
    inactive = members.get_inactive_members()
    return render_template("inactive.html", members=inactive)

@app.route("/reactivate/<int:member_id>")
def reactivate(member_id):
    members.reactivate_member(member_id)
    return redirect(url_for("inactive_members"))

@app.route("/monthly_check")
def monthly_check():
    members.run_monthly_check()
    return redirect(url_for("home"))

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
    total_pending = sum(m["total_fee"] for m in unpaid)
    return render_template("unpaid.html",
        unpaid=unpaid,
        total_pending=total_pending
    )

@app.route("/plans")
def show_plans():
    return render_template("plans.html", plans=PLANS)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
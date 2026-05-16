from flask import Flask, render_template, request, redirect, url_for, session
from database import setup_database
from auth import check_credentials
import members
import finance
import attendance
import expense
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = "goldengym_secret_2026"
UPI_ID = "9585194396@upi"
GYM_NAME = "Golden Gym"

setup_database()
PLANS = members.PLANS

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

def member_login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("member_id"):
            return redirect(url_for("member_login"))
        return f(*args, **kwargs)
    return decorated

# ─── OWNER AUTH ───
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if check_credentials(username, password):
            session["logged_in"] = True
            return redirect(url_for("home"))
        return render_template("login.html", error="Wrong username or password!")
    return render_template("login.html", error=None)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ─── MEMBER AUTH ───
@app.route("/member/register", methods=["GET", "POST"])
def member_register():
    if request.method == "POST":
        name = request.form["name"]
        username = request.form["username"]
        phone = request.form["phone"]
        password = request.form["password"]
        confirm = request.form["confirm"]
        if password != confirm:
            return render_template("member_register.html", error="Passwords don't match!")
        success, msg = members.register_member(name, username, phone, password)
        if success:
            return redirect(url_for("member_login", success="1"))
        return render_template("member_register.html", error=msg)
    return render_template("member_register.html", error=None)

@app.route("/member/login", methods=["GET", "POST"])
def member_login():
    success = request.args.get("success")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        member = members.member_login(username, password)
        if member:
            session["member_id"] = member["id"]
            session["member_name"] = member["name"]
            return redirect(url_for("member_home"))
        return render_template("member_login.html", error="Wrong username or password! Contact owner if forgotten.")
    return render_template("member_login.html", error=None, success=success)

@app.route("/member/logout")
def member_logout():
    session.pop("member_id", None)
    session.pop("member_name", None)
    return redirect(url_for("member_login"))

# ─── MEMBER PORTAL ───
@app.route("/member")
@member_login_required
def member_home():
    member = members.get_member_by_id(session["member_id"])
    today_att = attendance.get_member_today(session["member_id"])
    recent_att = attendance.get_member_attendance(session["member_id"])
    session_info = attendance.get_current_session()
    return render_template("member_home.html",
        member=member,
        today_att=today_att,
        recent_att=recent_att,
        session_info=session_info,
        plans=PLANS
    )

@app.route("/member/checkin")
@member_login_required
def member_checkin():
    success, msg = attendance.check_in(session["member_id"], session["member_name"])
    return redirect(url_for("member_home"))

@app.route("/member/checkout")
@member_login_required
def member_checkout():
    success, msg = attendance.check_out(session["member_id"])
    return redirect(url_for("member_home"))

@app.route("/member/plan", methods=["GET", "POST"])
@member_login_required
def member_plan():
    member = members.get_member_by_id(session["member_id"])
    if request.method == "POST":
        plan_type = request.form["membership"]
        is_first = member["membership_type"] is None
        total, expiry = members.select_plan(session["member_id"], plan_type, is_first)
        return render_template("member_payment.html",
            member=member,
            plan=PLANS[plan_type],
            plan_type=plan_type,
            total=total,
            expiry=expiry,
            upi_id=UPI_ID,
            gym_name=GYM_NAME
        )
    return render_template("member_plan.html", member=member, plans=PLANS)

@app.route("/member/change_password", methods=["GET", "POST"])
@member_login_required
def member_change_password():
    if request.method == "POST":
        old = request.form["old_password"]
        new = request.form["new_password"]
        confirm = request.form["confirm"]
        if new != confirm:
            return render_template("member_change_password.html", error="Passwords don't match!")
        success, msg = members.change_password(session["member_id"], old, new)
        if success:
            return render_template("member_change_password.html", success=msg)
        return render_template("member_change_password.html", error=msg)
    return render_template("member_change_password.html", error=None)

# ─── OWNER PORTAL ───
@app.route("/")
@login_required
def home():
    all_members = members.get_all_members()
    unverified = members.get_unverified_members()
    paid = [m for m in all_members if m["paid"]]
    unpaid = [m for m in all_members if not m["paid"]]
    warned = members.get_warned_members()
    inactive = members.get_inactive_members()
    monthly_income = finance.get_monthly_total()
    monthly_expense = expense.get_monthly_expense_total()
    profit = monthly_income - monthly_expense
    today_att = attendance.get_today_attendance()
    return render_template("home.html",
        total_members=len(all_members),
        new_registrations=len(unverified),
        total_paid=len(paid),
        total_unpaid=len(unpaid),
        total_warned=len(warned),
        total_inactive=len(inactive),
        total_collected=sum(m["total_fee"] for m in paid),
        total_pending=sum(m["total_fee"] for m in unpaid),
        monthly_income=monthly_income,
        monthly_expense=monthly_expense,
        profit=profit,
        today_att=today_att,
        today_count=len(today_att)
    )

@app.route("/members")
@login_required
def show_members():
    all_members = members.get_all_members()
    unverified = members.get_unverified_members()
    warned = members.get_warned_members()
    warned_ids = [m["id"] for m in warned]
    return render_template("members.html",
        members=all_members,
        unverified=unverified,
        warned_ids=warned_ids,
        plans=PLANS
    )

@app.route("/mark_paid/<int:member_id>")
@login_required
def mark_paid(member_id):
    members.mark_paid(member_id)
    return redirect(url_for("show_members"))

@app.route("/soft_remove/<int:member_id>")
@login_required
def soft_remove(member_id):
    members.soft_remove_member(member_id)
    return redirect(url_for("show_members"))

@app.route("/inactive")
@login_required
def inactive_members():
    inactive = members.get_inactive_members()
    return render_template("inactive.html", members=inactive)

@app.route("/reactivate/<int:member_id>")
@login_required
def reactivate(member_id):
    members.reactivate_member(member_id)
    return redirect(url_for("inactive_members"))

@app.route("/monthly_check")
@login_required
def monthly_check():
    members.run_monthly_check()
    return redirect(url_for("home"))

@app.route("/attendance")
@login_required
def show_attendance():
    today_att = attendance.get_today_attendance()
    all_members = members.get_all_members()
    today = datetime.now().strftime("%d-%m-%Y")
    present_ids = [r["member_id"] for r in today_att]
    return render_template("attendance.html",
        today_att=today_att,
        all_members=all_members,
        present_ids=present_ids,
        today=today
    )

@app.route("/auto_checkout")
@login_required
def auto_checkout():
    attendance.auto_checkout_all()
    return redirect(url_for("show_attendance"))

@app.route("/finance")
@login_required
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
@login_required
def add_income():
    if request.method == "POST":
        source = request.form["source"]
        amount = int(request.form["amount"])
        finance.add_income(source, amount)
        return redirect(url_for("show_finance"))
    return render_template("add_income.html")

@app.route("/expenses")
@login_required
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
@login_required
def add_expense():
    if request.method == "POST":
        category = request.form["category"]
        description = request.form["description"]
        amount = int(request.form["amount"])
        expense.add_expense(category, description, amount)
        return redirect(url_for("show_expenses"))
    return render_template("add_expense.html")

@app.route("/unpaid")
@login_required
def show_unpaid():
    all_members = members.get_all_members()
    unpaid = [m for m in all_members if not m["paid"]]
    total_pending = sum(m["total_fee"] for m in unpaid)
    return render_template("unpaid.html",
        unpaid=unpaid,
        total_pending=total_pending
    )

@app.route("/plans")
@login_required
def show_plans():
    return render_template("plans.html", plans=PLANS)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

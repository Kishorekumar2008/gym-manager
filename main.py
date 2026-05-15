import members
import finance
import attendance
import expense
import search
import reports

def show_menu():
    print("\n🏋️  GYM MANAGER  🏋️")
    print("--- MEMBERS ---")
    print("1.  Add Member")
    print("2.  Show All Members")
    print("3.  Mark Fee as Paid")
    print("4.  Search Member")
    print("5.  Unpaid Members")
    print("6.  Payment Summary")
    print("--- ATTENDANCE ---")
    print("7.  Mark Attendance")
    print("8.  Today's Attendance")
    print("9.  Member History")
    print("10. Inactive Members")
    print("--- FINANCE ---")
    print("11. Add Income")
    print("12. Monthly Income")
    print("13. Yearly Comparison")
    print("--- EXPENSES ---")
    print("14. Add Expense")
    print("15. Monthly Expenses")
    print("--- REPORTS ---")
    print("16. Full Report")
    print("--- SYSTEM ---")
    print("17. Exit")
    return input("\nChoose option: ")

def main():
    members.setup()
    finance.setup()
    attendance.setup()
    expense.setup()

    while True:
        choice = show_menu()

        if choice == "1":
            name = input("Member Name: ")
            phone = input("Phone Number: ")
            print("Membership: monthly / quarterly / yearly")
            membership = input("Type: ")
            fee = input("Fee Amount (₹): ")
            members.add_member(name, phone, membership, int(fee))

        elif choice == "2":
            members.show_members()

        elif choice == "3":
            members.show_members()
            mid = int(input("Enter Member ID to mark paid: "))
            members.mark_paid(mid)

        elif choice == "4":
            keyword = input("Search by name or phone: ")
            search.search_member(keyword)

        elif choice == "5":
            search.show_unpaid()

        elif choice == "6":
            search.payment_summary()

        elif choice == "7":
            members.show_members()
            mid = int(input("Enter Member ID: "))
            name = input("Member Name: ")
            attendance.mark_attendance(mid, name)

        elif choice == "8":
            attendance.show_today()

        elif choice == "9":
            mid = int(input("Enter Member ID: "))
            attendance.member_history(mid)

        elif choice == "10":
            attendance.inactive_members()

        elif choice == "11":
            source = input("Income source: ")
            amount = int(input("Amount (₹): "))
            finance.add_income(source, amount)

        elif choice == "12":
            finance.show_monthly_income()

        elif choice == "13":
            finance.yearly_comparison()

        elif choice == "14":
            print("Categories: rent / electricity / equipment / salary / other")
            category = input("Category: ")
            description = input("Description: ")
            amount = int(input("Amount (₹): "))
            expense.add_expense(category, description, amount)

        elif choice == "15":
            expense.show_monthly_expenses()

        elif choice == "16":
            reports.full_report()

        elif choice == "17":
            print("Goodbye! 💪")
            break

        else:
            print("Invalid option!")

main()
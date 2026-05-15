import members
import finance
import attendance

def show_menu():
    print("\n🏋️  GYM MANAGER  🏋️")
    print("--- MEMBERS ---")
    print("1. Add Member")
    print("2. Show All Members")
    print("3. Mark Fee as Paid")
    print("--- ATTENDANCE ---")
    print("4. Mark Attendance")
    print("5. Today's Attendance")
    print("6. Member Attendance History")
    print("7. Inactive Members")
    print("--- FINANCE ---")
    print("8. Add Income")
    print("9. Monthly Income")
    print("10. Yearly Comparison")
    print("--- SYSTEM ---")
    print("11. Exit")
    return input("Choose option: ")

def main():
    members.setup()
    finance.setup()
    attendance.setup()

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
            members.show_members()
            mid = int(input("Enter Member ID: "))
            name = input("Member Name: ")
            attendance.mark_attendance(mid, name)

        elif choice == "5":
            attendance.show_today()

        elif choice == "6":
            mid = int(input("Enter Member ID: "))
            attendance.member_history(mid)

        elif choice == "7":
            attendance.inactive_members()

        elif choice == "8":
            source = input("Income source: ")
            amount = int(input("Amount (₹): "))
            finance.add_income(source, amount)

        elif choice == "9":
            finance.show_monthly_income()

        elif choice == "10":
            finance.yearly_comparison()

        elif choice == "11":
            print("Goodbye! 💪")
            break

        else:
            print("Invalid option!")

main()
import members
import finance

def show_menu():
    print("\n🏋️  GYM MANAGER  🏋️")
    print("1. Add Member")
    print("2. Show All Members")
    print("3. Mark Fee as Paid")
    print("4. Add Income")
    print("5. Show Monthly Income")
    print("6. Yearly Comparison")
    print("7. Exit")
    return input("Choose option: ")

def main():
    members.setup()
    finance.setup()
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
            source = input("Income source (eg: membership, personal training): ")
            amount = int(input("Amount (₹): "))
            finance.add_income(source, amount)

        elif choice == "5":
            finance.show_monthly_income()

        elif choice == "6":
            finance.yearly_comparison()

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid option!")

main()
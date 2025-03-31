# agrifinance/main.py
from agrifinance.utils.income_menu import IncomeMenu
from agrifinance.utils.expense_menu import ExpenseMenu
from agrifinance.utils.loan_menu import LoanMenu
from agrifinance.utils.report_menu import ReportMenu

class AgriFinanceTracker:
    def __init__(self):
        self.income_menu = IncomeMenu()
        self.expense_menu = ExpenseMenu()
        self.loan_menu = LoanMenu()
        self.report_menu = ReportMenu()

    def run(self):
        print("Welcome to AgriFinance Tracker")
        while True:
            print("\nMain Menu")
            print("1. Income Management")
            print("2. Expense Management")
            print("3. Loan Management")
            print("4. Reports")
            print("5. Exit")
            
            choice = input("Enter your choice: ")
            
            if choice == '1':
                self.income_menu.display_menu()
            elif choice == '2':
                self.expense_menu.display_menu()
            elif choice == '3':
                self.loan_menu.display_menu()
            elif choice == '4':
                self.report_menu.display_menu()
            elif choice == '5':
                print("Thank you for using AgriFinance Tracker. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    app = AgriFinanceTracker()
    app.run()
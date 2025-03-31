# agrifinance/utils/expense_menu.py
from datetime import datetime
from agrifinance.services.expense_service import ExpenseService
from agrifinance.models.expense import Expense

class ExpenseMenu:
    def __init__(self):
        self.service = ExpenseService()

    def display_menu(self):
        while True:
            print("\nExpense Management")
            print("1. Add Expense")
            print("2. View All Expenses")
            print("3. View Expenses by Date Range")
            print("4. Update Expense")
            print("5. Delete Expense")
            print("6. Back to Main Menu")
            
            choice = input("Enter your choice: ")
            
            if choice == '1':
                self._add_expense()
            elif choice == '2':
                self._view_all_expenses()
            elif choice == '3':
                self._view_expenses_by_date_range()
            elif choice == '4':
                self._update_expense()
            elif choice == '5':
                self._delete_expense()
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")

    def _add_expense(self):
        print("\nAdd New Expense")
        try:
            amount = float(input("Enter amount: "))
            category = input("Enter category: ")
            date_str = input("Enter date (YYYY-MM-DD): ")
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            description = input("Enter description (optional): ")
            
            expense = Expense(amount=amount, category=category, date=date, description=description)
            expense_id = self.service.add_expense(expense)
            print(f"Expense added successfully with ID: {expense_id}")
        except ValueError as e:
            print(f"Error: {e}. Please enter valid data.")

    def _view_all_expenses(self):
        print("\nAll Expenses")
        expenses = self.service.get_all_expenses()
        if not expenses:
            print("No expenses found.")
            return
        
        for expense in expenses:
            print(f"ID: {expense.id}, Amount: {expense.amount}, Category: {expense.category}, "
                  f"Date: {expense.date}, Description: {expense.description}")

    def _view_expenses_by_date_range(self):
        print("\nView Expenses by Date Range")
        try:
            start_date_str = input("Enter start date (YYYY-MM-DD): ")
            end_date_str = input("Enter end date (YYYY-MM-DD): ")
            
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            
            expenses = self.service.get_expenses_by_date_range(start_date, end_date)
            if not expenses:
                print("No expenses found for the specified date range.")
                return
            
            print(f"\nExpenses from {start_date} to {end_date}:")
            for expense in expenses:
                print(f"ID: {expense.id}, Amount: {expense.amount}, Category: {expense.category}, "
                      f"Date: {expense.date}, Description: {expense.description}")
        except ValueError as e:
            print(f"Error: {e}. Please enter valid dates in YYYY-MM-DD format.")
 def _update_expense(self):
        print("\nUpdate Expense")
        try:
            expense_id = int(input("Enter expense ID to update: "))
            existing_expense = self.service.get_expense_by_id(expense_id)
            
            if not existing_expense:
                print(f"No expense found with ID {expense_id}")
                return
            
            print(f"Current details: Amount: {existing_expense.amount}, Category: {existing_expense.category}, "
                  f"Date: {existing_expense.date}, Description: {existing_expense.description}")
            
            amount = float(input(f"Enter new amount (current: {existing_expense.amount}): ") or existing_expense.amount)
            category = input(f"Enter new category (current: {existing_expense.category}): ") or existing_expense.category
            date_str = input(f"Enter new date (YYYY-MM-DD) (current: {existing_expense.date}): ")
            date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else existing_expense.date
            description = input(f"Enter new description (current: {existing_expense.description}): ") or existing_expense.description
            
            updated_expense = Expense(
                id=expense_id,
                amount=amount,
                category=category,
                date=date,
                description=description
            )
            
            if self.service.update_expense(updated_expense):
                print("Expense updated successfully.")
            else:
                print("Failed to update expense.")
        except ValueError as e:
            print(f"Error: {e}. Please enter valid data.")

    def _delete_expense(self):
        print("\nDelete Expense")
        try:
            expense_id = int(input("Enter expense ID to delete: "))
            if self.service.delete_expense(expense_id):
                print("Expense deleted successfully.")
            else:
                print(f"No expense found with ID {expense_id}")
        except ValueError:
            print("Invalid ID. Please enter a number.")

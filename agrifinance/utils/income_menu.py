# agrifinance/utils/income_menu.py
from datetime import datetime
from agrifinance.services.income_service import IncomeService
from agrifinance.models.income import Income

class IncomeMenu:
    def __init__(self):
        self.service = IncomeService()

    def display_menu(self):
        while True:
            print("\nIncome Management")
            print("1. Add Income")
            print("2. View All Incomes")
            print("3. View Income by Date Range")
            print("4. Update Income")
            print("5. Delete Income")
            print("6. Back to Main Menu")
            
            choice = input("Enter your choice: ")
            
            if choice == '1':
                self._add_income()
            elif choice == '2':
                self._view_all_incomes()
            elif choice == '3':
                self._view_incomes_by_date_range()
            elif choice == '4':
                self._update_income()
            elif choice == '5':
                self._delete_income()
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")

    def _add_income(self):
        print("\nAdd New Income")
        try:
            amount = float(input("Enter amount: "))
            source = input("Enter source: ")
            date_str = input("Enter date (YYYY-MM-DD): ")
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            description = input("Enter description (optional): ")
            
            income = Income(amount=amount, source=source, date=date, description=description)
            income_id = self.service.add_income(income)
            print(f"Income added successfully with ID: {income_id}")
        except ValueError as e:
            print(f"Error: {e}. Please enter valid data.")

    def _view_all_incomes(self):
        print("\nAll Incomes")
        incomes = self.service.get_all_incomes()
        if not incomes:
            print("No incomes found.")
            return
        
        for income in incomes:
            print(f"ID: {income.id}, Amount: {income.amount}, Source: {income.source}, "
                  f"Date: {income.date}, Description: {income.description}")

    def _view_incomes_by_date_range(self):
        print("\nView Incomes by Date Range")
        try:
            start_date_str = input("Enter start date (YYYY-MM-DD): ")
            end_date_str = input("Enter end date (YYYY-MM-DD): ")
            
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            
            incomes = self.service.get_incomes_by_date_range(start_date, end_date)
            if not incomes:
                print("No incomes found for the specified date range.")
                return
            
            print(f"\nIncomes from {start_date} to {end_date}:")
            for income in incomes:
                print(f"ID: {income.id}, Amount: {income.amount}, Source: {income.source}, "
                      f"Date: {income.date}, Description: {income.description}")
        except ValueError as e:
            print(f"Error: {e}. Please enter valid dates in YYYY-MM-DD format.")

    def _update_income(self):
        print("\nUpdate Income")
        try:
            income_id = int(input("Enter income ID to update: "))
            existing_income = self.service.get_income_by_id(income_id)
            
            if not existing_income:
                print(f"No income found with ID {income_id}")
                return
            
            print(f"Current details: Amount: {existing_income.amount}, Source: {existing_income.source}, "
                  f"Date: {existing_income.date}, Description: {existing_income.description}")
            
            amount = float(input(f"Enter new amount (current: {existing_income.amount}): ") or existing_income.amount)
            source = input(f"Enter new source (current: {existing_income.source}): ") or existing_income.source
            date_str = input(f"Enter new date (YYYY-MM-DD) (current: {existing_income.date}): ")
            date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else existing_income.date
            description = input(f"Enter new description (current: {existing_income.description}): ") or existing_income.description
            
            updated_income = Income(
                id=income_id,
                amount=amount,
                source=source,
                date=date,
                description=description
            )
            
            if self.service.update_income(updated_income):
                print("Income updated successfully.")
            else:
                print("Failed to update income.")
        except ValueError as e:
            print(f"Error: {e}. Please enter valid data.")

    def _delete_income(self):
        print("\nDelete Income")
        try:
            income_id = int(input("Enter income ID to delete: "))
            if self.service.delete_income(income_id):
                print("Income deleted successfully.")
            else:
                print(f"No income found with ID {income_id}")
        except ValueError:
            print("Invalid ID. Please enter a number.")
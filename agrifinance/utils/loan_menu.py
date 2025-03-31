# agrifinance/utils/loan_menu.py
from datetime import datetime
from agrifinance.services.loan_service import LoanService
from agrifinance.models.loan import Loan, LoanStatus

class LoanMenu:
    def __init__(self):
        self.service = LoanService()

    def display_menu(self):
        while True:
            print("\nLoan Management")
            print("1. Add Loan")
            print("2. View All Loans")
            print("3. View Loans by Status")
            print("4. Update Loan")
            print("5. Delete Loan")
            print("6. View Payment Schedule")
            print("7. Back to Main Menu")
            
            choice = input("Enter your choice: ")
            
            if choice == '1':
                self._add_loan()
            elif choice == '2':
                self._view_all_loans()
            elif choice == '3':
                self._view_loans_by_status()
            elif choice == '4':
                self._update_loan()
            elif choice == '5':
                self._delete_loan()
            elif choice == '6':
                self._view_payment_schedule()
            elif choice == '7':
                break
            else:
                print("Invalid choice. Please try again.")

    def _add_loan(self):
        print("\nAdd New Loan")
        try:
            amount = float(input("Enter loan amount: "))
            interest_rate = float(input("Enter annual interest rate (%): "))
            term_months = int(input("Enter term in months: "))
            lender = input("Enter lender name: ")
            date_str = input("Enter issue date (YYYY-MM-DD): ")
            date_issued = datetime.strptime(date_str, "%Y-%m-%d").date()
            
            loan = Loan(
                amount=amount,
                interest_rate=interest_rate,
                term_months=term_months,
                lender=lender,
                date_issued=date_issued
            )
            loan_id = self.service.add_loan(loan)
            print(f"Loan added successfully with ID: {loan_id}")
        except ValueError as e:
            print(f"Error: {e}. Please enter valid data.")

    def _view_all_loans(self):
        print("\nAll Loans")
        loans = self.service.get_all_loans()
        if not loans:
            print("No loans found.")
            return
        
        for loan in loans:
            print(f"ID: {loan.id}, Amount: {loan.amount}, Rate: {loan.interest_rate}%, "
                  f"Term: {loan.term_months} months, Lender: {loan.lender}, "
                  f"Issued: {loan.date_issued}, Status: {loan.status.value}")

    def _view_loans_by_status(self):
        print("\nView Loans by Status")
        print("1. Active")
        print("2. Paid")
        print("3. Defaulted")
        
        choice = input("Enter status choice: ")
        status_map = {
            '1': LoanStatus.ACTIVE,
            '2': LoanStatus.PAID,
            '3': LoanStatus.DEFAULTED
        }
        
        if choice not in status_map:
            print("Invalid choice.")
            return
            
        loans = self.service.get_loans_by_status(status_map[choice])
        if not loans:
            print(f"No {status_map[choice].value} loans found.")
            return
            
        print(f"\n{status_map[choice].value.capitalize()} Loans:")
        for loan in loans:
            print(f"ID: {loan.id}, Amount: {loan.amount}, Lender: {loan.lender}")

    def _update_loan(self):
        print("\nUpdate Loan")
        try:
            loan_id = int(input("Enter loan ID to update: "))
            existing_loan = self.service.get_loan_by_id(loan_id)
            
            if not existing_loan:
                print(f"No loan found with ID {loan_id}")
                return
            
            print(f"Current details: Amount: {existing_loan.amount}, Rate: {existing_loan.interest_rate}%, "
                  f"Term: {existing_loan.term_months} months, Lender: {existing_loan.lender}, "
                  f"Issued: {existing_loan.date_issued}, Status: {existing_loan.status.value}")
            
            amount = float(input(f"Enter new amount (current: {existing_loan.amount}): ") or existing_loan.amount)
            interest_rate = float(input(f"Enter new rate (current: {existing_loan.interest_rate}): ") or existing_loan.interest_rate)
            term_months = int(input(f"Enter new term (current: {existing_loan.term_months}): ") or existing_loan.term_months)
            lender = input(f"Enter new lender (current: {existing_loan.lender}): ") or existing_loan.lender
            date_str = input(f"Enter new issue date (YYYY-MM-DD) (current: {existing_loan.date_issued}): ")
            date_issued = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else existing_loan.date_issued
            
            print("\nSelect new status:")
            print("1. Active")
            print("2. Paid")
            print("3. Defaulted")
            status_choice = input(f"Enter choice (current: {existing_loan.status.value}): ")
            
            status_map = {
                '1': LoanStatus.ACTIVE,
                '2': LoanStatus.PAID,
                '3': LoanStatus.DEFAULTED
            }
            status = status_map.get(status_choice, existing_loan.status)
            
            updated_loan = Loan(
                id=loan_id,
                amount=amount,
                interest_rate=interest_rate,
                term_months=term_months,
                lender=lender,
                date_issued=date_issued,
                status=status
            )
            
            if self.service.update_loan(updated_loan):
                print("Loan updated successfully.")
            else:
                print("Failed to update loan.")
        except ValueError as e:
            print(f"Error: {e}. Please enter valid data.")

    def _delete_loan(self):
        print("\nDelete Loan")
        try:
            loan_id = int(input("Enter loan ID to delete: "))
            if self.service.delete_loan(loan_id):
                print("Loan deleted successfully.")
            else:
                print(f"No loan found with ID {loan_id}")
        except ValueError:
            print("Invalid ID. Please enter a number.")

    def _view_payment_schedule(self):
        print("\nView Payment Schedule")
        try:
            loan_id = int(input("Enter loan ID: "))
            schedule = self.service.calculate_payment_schedule(loan_id)
            
            if not schedule:
                print("No payment schedule found for this loan.")
                return
                
            print(f"\nPayment Schedule for Loan {loan_id}:")
            print(f"{'Month':<8}{'Payment':<12}{'Principal':<12}{'Interest':<12}{'Balance':<12}")
            for payment in schedule:
                print(f"{payment['month']:<8}{payment['payment']:<12.2f}{payment['principal']:<12.2f}"
                      f"{payment['interest']:<12.2f}{payment['balance']:<12.2f}")
        except ValueError:
            print("Invalid ID. Please enter a number.")
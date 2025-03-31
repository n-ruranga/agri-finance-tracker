# agrifinance/services/loan_service.py
from datetime import date
from agrifinance.database.db_handler import DBHandler
from agrifinance.models.loan import Loan, LoanStatus

class LoanService:
    def __init__(self):
        self.db = DBHandler()

    def add_loan(self, loan: Loan) -> int:
        cursor = self.db.get_cursor()
        try:
            cursor.execute("""
                INSERT INTO loan (amount, interest_rate, term_months, lender, date_issued, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (loan.amount, loan.interest_rate, loan.term_months, 
                 loan.lender, loan.date_issued, loan.status.value))
            self.db.commit()
            return cursor.lastrowid
        finally:
            cursor.close()

    def get_loan_by_id(self, loan_id: int) -> Loan:
        cursor = self.db.get_cursor()
        try:
            cursor.execute("SELECT * FROM loan WHERE id = %s", (loan_id,))
            result = cursor.fetchone()
            return Loan.from_dict(result) if result else None
        finally:
            cursor.close()

    def get_all_loans(self) -> list[Loan]:
        cursor = self.db.get_cursor()
        try:
            cursor.execute("SELECT * FROM loan ORDER BY date_issued DESC")
            return [Loan.from_dict(row) for row in cursor.fetchall()]
        finally:
            cursor.close()

    def get_loans_by_status(self, status: LoanStatus) -> list[Loan]:
        cursor = self.db.get_cursor()
        try:
            cursor.execute("SELECT * FROM loan WHERE status = %s ORDER BY date_issued DESC", (status.value,))
            return [Loan.from_dict(row) for row in cursor.fetchall()]
        finally:
            cursor.close()

    def update_loan(self, loan: Loan) -> bool:
        cursor = self.db.get_cursor()
        try:
            cursor.execute("""
                UPDATE loan 
                SET amount = %s, interest_rate = %s, term_months = %s, 
                    lender = %s, date_issued = %s, status = %s
                WHERE id = %s
            """, (loan.amount, loan.interest_rate, loan.term_months,
                 loan.lender, loan.date_issued, loan.status.value, loan.id))
            self.db.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()

    def delete_loan(self, loan_id: int) -> bool:
        cursor = self.db.get_cursor()
        try:
            cursor.execute("DELETE FROM loan WHERE id = %s", (loan_id,))
            self.db.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()

    def calculate_payment_schedule(self, loan_id: int) -> list[dict]:
        loan = self.get_loan_by_id(loan_id)
        if not loan:
            return []
            
        monthly_rate = loan.interest_rate / 100 / 12
        payment = (loan.amount * monthly_rate) / (1 - (1 + monthly_rate) ** -loan.term_months)
        
        schedule = []
        balance = loan.amount
        
        for month in range(1, loan.term_months + 1):
            interest = balance * monthly_rate
            principal = payment - interest
            balance -= principal
            
            schedule.append({
                'month': month,
                'payment': round(payment, 2),
                'principal': round(principal, 2),
                'interest': round(interest, 2),
                'balance': round(max(balance, 0), 2)
            })
            
        return schedule
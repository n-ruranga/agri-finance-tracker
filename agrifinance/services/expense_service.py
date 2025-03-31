# agrifinance/services/expense_service.py
from datetime import date
from agrifinance.database.db_handler import DBHandler
from agrifinance.models.expense import Expense

class ExpenseService:
    def __init__(self):
        self.db = DBHandler()

    def add_expense(self, expense: Expense) -> int:
        cursor = self.db.get_cursor()
        try:
            cursor.execute("""
                INSERT INTO expense (amount, category, date, description)
                VALUES (%s, %s, %s, %s)
            """, (expense.amount, expense.category, expense.date, expense.description))
            self.db.commit()
            return cursor.lastrowid
        finally:
            cursor.close()

    def get_expense_by_id(self, expense_id: int) -> Expense:
        cursor = self.db.get_cursor()
        try:
            cursor.execute("SELECT * FROM expense WHERE id = %s", (expense_id,))
            result = cursor.fetchone()
            return Expense.from_dict(result) if result else None
        finally:
            cursor.close()

    def get_all_expenses(self) -> list[Expense]:
        cursor = self.db.get_cursor()
        try:
            cursor.execute("SELECT * FROM expense ORDER BY date DESC")
            return [Expense.from_dict(row) for row in cursor.fetchall()]
        finally:
            cursor.close()

    def get_expenses_by_date_range(self, start_date: date, end_date: date) -> list[Expense]:
        cursor = self.db.get_cursor()
        try:
            cursor.execute("""
                SELECT * FROM expense 
                WHERE date BETWEEN %s AND %s 
                ORDER BY date DESC
            """, (start_date, end_date))
            return [Expense.from_dict(row) for row in cursor.fetchall()]
        finally:
            cursor.close()

    def update_expense(self, expense: Expense) -> bool:
        cursor = self.db.get_cursor()
        try:
            cursor.execute("""
                UPDATE expense 
                SET amount = %s, category = %s, date = %s, description = %s
                WHERE id = %s
            """, (expense.amount, expense.category, expense.date, expense.description, expense.id))
            self.db.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()

    def delete_expense(self, expense_id: int) -> bool:
        cursor = self.db.get_cursor()
        try:
            cursor.execute("DELETE FROM expense WHERE id = %s", (expense_id,))
            self.db.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()
     

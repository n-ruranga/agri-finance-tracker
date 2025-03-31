# agrifinance/services/income_service.py
from datetime import date
from agrifinance.database.db_handler import DBHandler
from agrifinance.models.income import Income

class IncomeService:
    def __init__(self):
        self.db = DBHandler()

    def add_income(self, income: Income) -> int:
        cursor = self.db.get_cursor()
        try:
            cursor.execute("""
                INSERT INTO income (amount, source, date, description)
                VALUES (%s, %s, %s, %s)
            """, (income.amount, income.source, income.date, income.description))
            self.db.commit()
            return cursor.lastrowid
        finally:
            cursor.close()

    def get_income_by_id(self, income_id: int) -> Income:
        cursor = self.db.get_cursor()
        try:
            cursor.execute("SELECT * FROM income WHERE id = %s", (income_id,))
            result = cursor.fetchone()
            return Income.from_dict(result) if result else None
        finally:
            cursor.close()

    def get_all_incomes(self) -> list[Income]:
        cursor = self.db.get_cursor()
        try:
            cursor.execute("SELECT * FROM income ORDER BY date DESC")
            return [Income.from_dict(row) for row in cursor.fetchall()]
        finally:
            cursor.close()

    def get_incomes_by_date_range(self, start_date: date, end_date: date) -> list[Income]:
        cursor = self.db.get_cursor()
        try:
            cursor.execute("""
                SELECT * FROM income 
                WHERE date BETWEEN %s AND %s 
                ORDER BY date DESC
            """, (start_date, end_date))
            return [Income.from_dict(row) for row in cursor.fetchall()]
        finally:
            cursor.close()

    def update_income(self, income: Income) -> bool:
        cursor = self.db.get_cursor()
        try:
            cursor.execute("""
                UPDATE income 
                SET amount = %s, source = %s, date = %s, description = %s
                WHERE id = %s
            """, (income.amount, income.source, income.date, income.description, income.id))
            self.db.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()

    def delete_income(self, income_id: int) -> bool:
        cursor = self.db.get_cursor()
        try:
            cursor.execute("DELETE FROM income WHERE id = %s", (income_id,))
            self.db.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()
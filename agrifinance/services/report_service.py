# agrifinance/services/report_service.py
from datetime import date, timedelta
from typing import List, Dict 
from agrifinance.database.db_handler import DBHandler
from agrifinance.models.report import FinancialSummary, CategorySummary, TimePeriodReport
from agrifinance.models.loan import LoanStatus

class ReportService:
    def __init__(self):
        self.db = DBHandler()

    def generate_time_period_report(self, start_date: date, end_date: date) -> TimePeriodReport:
        income_by_category = self._get_income_by_category(start_date, end_date)
        expenses_by_category = self._get_expenses_by_category(start_date, end_date)
        
        total_income = sum(item.amount for item in income_by_category)
        total_expenses = sum(item.amount for item in expenses_by_category)
        
        # Get loan information
        active_loans = self._get_active_loan_count()
        loan_payments_due = self._get_loan_payments_due(start_date, end_date)
        
        return TimePeriodReport(
            start_date=start_date,
            end_date=end_date,
            income_by_category=income_by_category,
            expenses_by_category=expenses_by_category,
            financial_summary=FinancialSummary(
                total_income=total_income,
                total_expenses=total_expenses,
                net_profit=total_income - total_expenses,
                active_loans=active_loans,
                loan_payments_due=loan_payments_due
            )
        )

    def _get_income_by_category(self, start_date: date, end_date: date) -> List[CategorySummary]:
        cursor = self.db.get_cursor()
        try:
            cursor.execute("""
                SELECT source as category, SUM(amount) as amount 
                FROM income 
                WHERE date BETWEEN %s AND %s
                GROUP BY source
                ORDER BY amount DESC
            """, (start_date, end_date))
            
            results = cursor.fetchall()
            total = sum(item['amount'] for item in results) or 1  # Avoid division by zero
            
            return [
                CategorySummary(
                    category=item['category'],
                    amount=float(item['amount']),
                    percentage=(item['amount'] / total) * 100
                )
                for item in results
            ]
        finally:
            cursor.close()

    def _get_expenses_by_category(self, start_date: date, end_date: date) -> List[CategorySummary]:
        cursor = self.db.get_cursor()
        try:
            cursor.execute("""
                SELECT category, SUM(amount) as amount 
                FROM expense 
                WHERE date BETWEEN %s AND %s
                GROUP BY category
                ORDER BY amount DESC
            """, (start_date, end_date))
            
            results = cursor.fetchall()
            total = sum(item['amount'] for item in results) or 1  # Avoid division by zero
            
            return [
                CategorySummary(
                    category=item['category'],
                    amount=float(item['amount']),
                    percentage=(item['amount'] / total) * 100
                )
                for item in results
            ]
        finally:
            cursor.close()

    def _get_active_loan_count(self) -> int:
        cursor = self.db.get_cursor()
        try:
            cursor.execute("SELECT COUNT(*) as count FROM loan WHERE status = 'active'")
            return cursor.fetchone()['count']
        finally:
            cursor.close()

    def _get_loan_payments_due(self, start_date: date, end_date: date) -> float:
        cursor = self.db.get_cursor()
        try:
            cursor.execute("""
                SELECT SUM(amount) as total 
                FROM loan 
                WHERE status = 'active' 
                AND date_issued BETWEEN %s AND %s
            """, (start_date, end_date))
            result = cursor.fetchone()
            return float(result['total']) if result['total'] else 0.0
        finally:
            cursor.close()

    def generate_annual_report(self, year: int) -> Dict[str, TimePeriodReport]:
        reports = {}
        for month in range(1, 13):
            start_date = date(year, month, 1)
            end_date = date(year, month + 1, 1) - timedelta(days=1) if month < 12 else date(year, 12, 31)
            reports[start_date.strftime("%B")] = self.generate_time_period_report(start_date, end_date)
        return reports



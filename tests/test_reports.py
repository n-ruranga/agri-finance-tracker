# tests/test_reports.py
import pytest
from datetime import date, timedelta
from agrifinance.services.report_service import ReportService
from agrifinance.models.loan import Loan, LoanStatus
from agrifinance.models.income import Income
from agrifinance.models.expense import Expense

@pytest.fixture
def report_service():
    return ReportService()

@pytest.fixture
def sample_data():
    from agrifinance.database.db_handler import DBHandler
    db = DBHandler()
    
    # Add test data
    test_income = Income(
        amount=1000,
        source="Crop Sales",
        date=date.today(),
        description="Test income"
    )
    
    test_expense = Expense(
        amount=500,
        category="Seeds",
        date=date.today(),
        description="Test expense"
    )
    
    test_loan = Loan(
        amount=10000,
        interest_rate=5.5,
        term_months=12,
        lender="Test Bank",
        date_issued=date.today()
    )
    
    cursor = db.get_cursor()
    try:
        cursor.execute("""
            INSERT INTO income (amount, source, date, description)
            VALUES (%s, %s, %s, %s)
        """, (test_income.amount, test_income.source, test_income.date, test_income.description))
        
        cursor.execute("""
            INSERT INTO expense (amount, category, date, description)
            VALUES (%s, %s, %s, %s)
        """, (test_expense.amount, test_expense.category, test_expense.date, test_expense.description))
        
        cursor.execute("""
            INSERT INTO loan (amount, interest_rate, term_months, lender, date_issued, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (test_loan.amount, test_loan.interest_rate, test_loan.term_months, 
              test_loan.lender, test_loan.date_issued, test_loan.status.value))
        
        db.commit()
    finally:
        cursor.close()
    
    yield
    
    # Cleanup
    cursor = db.get_cursor()
    try:
        cursor.execute("DELETE FROM income WHERE description = 'Test income'")
        cursor.execute("DELETE FROM expense WHERE description = 'Test expense'")
        cursor.execute("DELETE FROM loan WHERE lender = 'Test Bank'")
        db.commit()
    finally:
        cursor.close()

def test_time_period_report(report_service, sample_data):
    start_date = date.today() - timedelta(days=1)
    end_date = date.today() + timedelta(days=1)
    
    report = report_service.generate_time_period_report(start_date, end_date)
    
    assert report.financial_summary.total_income == 1000
    assert report.financial_summary.total_expenses == 500
    assert report.financial_summary.net_profit == 500
    assert report.financial_summary.active_loans >= 1

def test_annual_report(report_service, sample_data):
    year = date.today().year
    reports = report_service.generate_annual_report(year)
    
    assert len(reports) == 12
    current_month = date.today().strftime("%B")
    assert reports[current_month].financial_summary.total_income == 1000
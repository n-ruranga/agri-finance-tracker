# agrifinance/models/report.py
from datetime import date
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class FinancialSummary:
    total_income: float
    total_expenses: float
    net_profit: float
    active_loans: int
    loan_payments_due: float

@dataclass
class CategorySummary:
    category: str
    amount: float
    percentage: float

@dataclass
class TimePeriodReport:
    start_date: date
    end_date: date
    income_by_category: List[CategorySummary]
    expenses_by_category: List[CategorySummary]
    financial_summary: FinancialSummary 
    
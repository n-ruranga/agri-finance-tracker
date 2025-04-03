# agrifinance/models/loan.py

from datetime import date
from enum import Enum

class LoanStatus(Enum):
    ACTIVE = "active"
    PAID = "paid"
    DEFAULTED = "defaulted"

class Loan:
    def __init__(self, amount: float, interest_rate: float, term_months: int, 
                 lender: str, date_issued: date, status: LoanStatus = LoanStatus.ACTIVE,
                 id: int = None):
        self.id = id
        self.amount = amount
        self.interest_rate = interest_rate
        self.term_months = term_months
        self.lender = lender
        self.date_issued = date_issued
        self.status = status

    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'interest_rate': self.interest_rate,
            'term_months': self.term_months,
            'lender': self.lender,
            'date_issued': self.date_issued,
            'status': self.status.value
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id'),
            amount=data['amount'],
            interest_rate=data['interest_rate'],
            term_months=data['term_months'],
            lender=data['lender'],
            date_issued=data['date_issued'],
            status=LoanStatus(data.get('status', 'active'))
        )

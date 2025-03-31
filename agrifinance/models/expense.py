# agrifinance/models/expense.py
from datetime import date

class Expense:
    def __init__(self, amount: float, category: str, date: date, description: str = None, id: int = None):
        self.id = id
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description

    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'category': self.category,
            'date': self.date,
            'description': self.description
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id'),
            amount=data['amount'],
            category=data['category'],
            date=data['date'],
            description=data.get('description')
        )

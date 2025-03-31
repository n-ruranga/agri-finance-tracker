# agrifinance/models/income.py
from datetime import date

class Income:
    def __init__(self, amount: float, source: str, date: date, description: str = None, id: int = None):
        self.id = id
        self.amount = amount
        self.source = source
        self.date = date
        self.description = description

    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'source': self.source,
            'date': self.date,
            'description': self.description
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id'),
            amount=data['amount'],
            source=data['source'],
            date=data['date'],
            description=data.get('description')
        )
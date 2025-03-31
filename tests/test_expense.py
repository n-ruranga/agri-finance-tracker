# tests/test_expense.py
import pytest
from datetime import date
from agrifinance.models.expense import Expense
from agrifinance.services.expense_service import ExpenseService

@pytest.fixture
def expense_service():
    return ExpenseService()

@pytest.fixture
def sample_expense():
    return Expense(
        amount=500.75,
        category="Seeds",
        date=date(2023, 10, 15),
        description="Maize seeds purchase"
    )

def test_add_and_get_expense(expense_service, sample_expense):
    # Add expense
    expense_id = expense_service.add_expense(sample_expense)
    assert expense_id is not None
    
    # Retrieve expense
    retrieved = expense_service.get_expense_by_id(expense_id)
    assert retrieved is not None
    assert retrieved.amount == sample_expense.amount
    assert retrieved.category == sample_expense.category
    assert retrieved.date == sample_expense.date
    assert retrieved.description == sample_expense.description
    
    # Cleanup
    expense_service.delete_expense(expense_id)

def test_update_expense(expense_service, sample_expense):
    # Add expense
    expense_id = expense_service.add_expense(sample_expense)
    
    # Update expense
    updated_expense = Expense(
        id=expense_id,
        amount=600.50,
        category="Fertilizer",
        date=date(2023, 10, 20),
        description="Organic fertilizer"
    )
    assert expense_service.update_expense(updated_expense)
    
    # Verify update
    retrieved = expense_service.get_expense_by_id(expense_id)
    assert retrieved.amount == updated_expense.amount
    assert retrieved.category == updated_expense.category
    
    # Cleanup
    expense_service.delete_expense(expense_id)

def test_delete_expense(expense_service, sample_expense):
    # Add expense
    expense_id = expense_service.add_expense(sample_expense)
    
    # Delete expense
    assert expense_service.delete_expense(expense_id)
    
    # Verify deletion
    assert expense_service.get_expense_by_id(expense_id) is None

def test_get_all_expenses(expense_service, sample_expense):
    # Get initial count
    initial_expenses = expense_service.get_all_expenses()
    initial_count = len(initial_expenses)
    
    # Add expense
    expense_id = expense_service.add_expense(sample_expense)
    
    # Verify count increased
    expenses = expense_service.get_all_expenses()
    assert len(expenses) == initial_count + 1
    
    # Cleanup
    expense_service.delete_expense(expense_id)
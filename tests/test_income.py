# tests/test_income.py
import pytest
from datetime import date
from agrifinance.models.income import Income
from agrifinance.services.income_service import IncomeService

@pytest.fixture
def income_service():
    return IncomeService()

@pytest.fixture
def sample_income():
    return Income(
        amount=1000.50,
        source="Crop Sales",
        date=date(2023, 10, 15),
        description="Maize harvest sale"
    )

def test_add_and_get_income(income_service, sample_income):
    # Add income
    income_id = income_service.add_income(sample_income)
    assert income_id is not None
    
    # Retrieve income
    retrieved = income_service.get_income_by_id(income_id)
    assert retrieved is not None
    assert retrieved.amount == sample_income.amount
    assert retrieved.source == sample_income.source
    assert retrieved.date == sample_income.date
    assert retrieved.description == sample_income.description
    
    # Cleanup
    income_service.delete_income(income_id)

def test_update_income(income_service, sample_income):
    # Add income
    income_id = income_service.add_income(sample_income)
    
    # Update income
    updated_income = Income(
        id=income_id,
        amount=1500.75,
        source="Livestock Sales",
        date=date(2023, 10, 20),
        description="Cattle sale"
    )
    assert income_service.update_income(updated_income)
    
    # Verify update
    retrieved = income_service.get_income_by_id(income_id)
    assert retrieved.amount == updated_income.amount
    assert retrieved.source == updated_income.source
    
    # Cleanup
    income_service.delete_income(income_id)

def test_delete_income(income_service, sample_income):
    # Add income
    income_id = income_service.add_income(sample_income)
    
    # Delete income
    assert income_service.delete_income(income_id)
    
    # Verify deletion
    assert income_service.get_income_by_id(income_id) is None

def test_get_all_incomes(income_service, sample_income):
    # Get initial count
    initial_incomes = income_service.get_all_incomes()
    initial_count = len(initial_incomes)
    
    # Add income
    income_id = income_service.add_income(sample_income)
    
    # Verify count increased
    incomes = income_service.get_all_incomes()
    assert len(incomes) == initial_count + 1
    
    # Cleanup
    income_service.delete_income(income_id)
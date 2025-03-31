# tests/test_loan.py
import pytest
from datetime import date
from agrifinance.models.loan import Loan, LoanStatus
from agrifinance.services.loan_service import LoanService

@pytest.fixture
def loan_service():
    return LoanService()

@pytest.fixture
def sample_loan():
    return Loan(
        amount=10000,
        interest_rate=5.5,
        term_months=24,
        lender="Agricultural Bank",
        date_issued=date(2023, 1, 15)
    )

def test_add_and_get_loan(loan_service, sample_loan):
    # Add loan
    loan_id = loan_service.add_loan(sample_loan)
    assert loan_id is not None
    
    # Retrieve loan
    retrieved = loan_service.get_loan_by_id(loan_id)
    assert retrieved is not None
    assert retrieved.amount == sample_loan.amount
    assert retrieved.lender == sample_loan.lender
    
    # Cleanup
    loan_service.delete_loan(loan_id)

def test_update_loan(loan_service, sample_loan):
    # Add loan
    loan_id = loan_service.add_loan(sample_loan)
    
    # Update loan
    updated_loan = Loan(
        id=loan_id,
        amount=12000,
        interest_rate=6.0,
        term_months=36,
        lender="Farm Credit",
        date_issued=date(2023, 2, 1),
        status=LoanStatus.ACTIVE
    )
    assert loan_service.update_loan(updated_loan)
    
    # Verify update
    retrieved = loan_service.get_loan_by_id(loan_id)
    assert retrieved.amount == updated_loan.amount
    assert retrieved.lender == updated_loan.lender
    
    # Cleanup
    loan_service.delete_loan(loan_id)

def test_payment_schedule(loan_service, sample_loan):
    loan_id = loan_service.add_loan(sample_loan)
    schedule = loan_service.calculate_payment_schedule(loan_id)
    
    assert len(schedule) == sample_loan.term_months
    assert schedule[0]['payment'] == pytest.approx(440.96, 0.01)
    assert schedule[-1]['balance'] == pytest.approx(0, 0.01)
    
    loan_service.delete_loan(loan_id)

def test_get_loans_by_status(loan_service, sample_loan):
    # Get initial counts
    active_loans = loan_service.get_loans_by_status(LoanStatus.ACTIVE)
    initial_active = len(active_loans)
    
    # Add loan
    loan_id = loan_service.add_loan(sample_loan)
    
    # Verify count increased
    assert len(loan_service.get_loans_by_status(LoanStatus.ACTIVE)) == initial_active + 1
    
    # Cleanup
    loan_service.delete_loan(loan_id)
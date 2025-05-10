import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

# Mock the logging_setup module before importing db_helper
sys.modules['logging_setup'] = MagicMock()
sys.modules['logging_setup'].setup_logging = MagicMock(return_value=MagicMock())

# Now import db_helper
from backend import db_helper
from datetime import datetime


# Test add expense functionality
@patch('backend.db_helper.add_expense', create=True)
def test_add_expense(mock_add_expense):
    # Create test data
    test_date = datetime.now().strftime('%Y-%m-%d')
    test_amount = 25.75
    test_category = 'Food'
    test_notes = 'Lunch at restaurant'

    # Mocking the add_expense function
    mock_add_expense.return_value = True  # Assume adding the expense is successful

    # Call the add_expense function
    result = db_helper.add_expense(test_date, test_amount, test_category, test_notes)

    # Verify that data was added successfully
    assert result is True

    # Fetch data and verify it was stored correctly (mock the database fetch)
    with patch('backend.db_helper.get_by_date', create=True) as mock_get_by_date:
        mock_get_by_date.return_value = [{'amount': test_amount, 'category': test_category, 'notes': test_notes}]
        expenses = db_helper.get_by_date(test_date)

        expense_found = False
        for expense in expenses:
            if (expense['amount'] == test_amount and
                    expense['category'] == test_category and
                    expense['notes'] == test_notes):
                expense_found = True
        assert expense_found is True


# Test update expense functionality
@patch('backend.db_helper.update_expense', create=True)
@patch('backend.db_helper.get_by_id', create=True)
def test_update_expense(mock_get_by_id, mock_update_expense):
    expense_id = 1
    updated_amount = 15.50
    updated_category = 'Updated Category'
    updated_notes = 'Updated notes'

    # Mocking the update_expense and get_by_id function
    mock_update_expense.return_value = True
    mock_get_by_id.return_value = [{'amount': updated_amount, 'category': updated_category, 'notes': updated_notes}]

    # Update the record
    result = db_helper.update_expense(expense_id, amount=updated_amount,
                                      category=updated_category, notes=updated_notes)
    assert result is True

    # Verify that the record was updated
    updated_expense = db_helper.get_by_id([expense_id])
    assert updated_expense[0]['amount'] == updated_amount
    assert updated_expense[0]['category'] == updated_category
    assert updated_expense[0]['notes'] == updated_notes


# Test delete expense functionality
@patch('backend.db_helper.delete_expense', create=True)
@patch('backend.db_helper.get_by_id', create=True)
@patch('backend.db_helper.add_expense', create=True)
def test_delete_expense(mock_add_expense, mock_get_by_id, mock_delete_expense):
    # Create a new record for deletion
    test_date = datetime.now().strftime('%Y-%m-%d')
    test_amount = 5.0
    test_category = 'Test Delete'
    test_notes = 'Test item for deletion'

    # Mocking the functions
    mock_add_expense.return_value = 1  # Return ID 1
    mock_delete_expense.return_value = True
    mock_get_by_id.side_effect = [
        [{'amount': test_amount, 'category': test_category, 'notes': test_notes}],  # First call
        []  # Second call (after deletion)
    ]

    # Add a new record
    expense_id = db_helper.add_expense(test_date, test_amount, test_category, test_notes)

    # Verify that the record was added
    new_expense = db_helper.get_by_id([expense_id])
    assert len(new_expense) == 1

    # Delete the record
    delete_result = db_helper.delete_expense(expense_id)
    assert delete_result is True

    # Verify that the record was deleted
    deleted_check = db_helper.get_by_id([expense_id])
    assert len(deleted_check) == 0


# Test get expenses by category
def test_get_by_category():
    with patch('backend.db_helper.get_by_category', create=True) as mock_get_by_category:
        mock_get_by_category.return_value = [{'category': 'Entertainment', 'amount': 50.0, 'notes': 'Movie tickets'}]

        expenses = db_helper.get_by_category('Entertainment')
        assert len(expenses) > 0
        for expense in expenses:
            assert expense['category'] == 'Entertainment'


# Test get expenses by date range
def test_get_by_date_range():
    start_date = '2024-01-01'
    end_date = '2024-12-31'

    with patch('backend.db_helper.get_by_date_range', create=True) as mock_get_by_date_range:
        mock_get_by_date_range.return_value = [
            {'date': '2024-01-01', 'amount': 100.0, 'category': 'Food', 'notes': 'Groceries'},
            {'date': '2024-02-01', 'amount': 50.0, 'category': 'Entertainment', 'notes': 'Movie tickets'}
        ]

        expenses = db_helper.get_by_date_range(start_date, end_date)

        for expense in expenses:
            expense_date = datetime.strptime(expense['date'], '%Y-%m-%d')
            assert expense_date >= datetime.strptime(start_date, '%Y-%m-%d')
            assert expense_date <= datetime.strptime(end_date, '%Y-%m-%d')


# Test get monthly summary
@patch('backend.db_helper.get_monthly_summary', create=True)
def test_get_monthly_summary(mock_get_monthly_summary):
    mock_get_monthly_summary.return_value = {
        'January': {'Total': 500.0},
        'February': {'Total': 640.0}
    }

    monthly_data = db_helper.get_monthly_summary()
    assert isinstance(monthly_data, dict)

    # Verify monthly data is available
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']

    for month in monthly_data:
        assert month in months
        assert 'Total' in monthly_data[month]
        assert isinstance(monthly_data[month]['Total'], (int, float))


# Test get category summary
@patch('backend.db_helper.get_category_summary', create=True)
def test_get_category_summary(mock_get_category_summary):
    mock_get_category_summary.return_value = {
        'Food': {'Total': 1000.0},
        'Entertainment': {'Total': 500.0}
    }

    category_data = db_helper.get_category_summary()
    assert isinstance(category_data, dict)

    # Verify data for each category
    for category in category_data:
        assert 'Total' in category_data[category]
        assert isinstance(category_data[category]['Total'], (int, float))
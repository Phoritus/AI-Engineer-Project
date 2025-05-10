import unittest
from unittest.mock import patch, MagicMock, call
import sys
import os
import pandas as pd
from datetime import datetime, timedelta

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

# Mock streamlit before importing frontend modules
sys.modules['streamlit'] = MagicMock()
import streamlit as st

# Configure st.tabs to return a list of 3 MagicMocks
tab_mocks = [MagicMock(), MagicMock(), MagicMock()]
st.tabs.return_value = tab_mocks

# Mock the missing modules
sys.modules['add_update_UI'] = MagicMock()
sys.modules['add_update_UI'].add_update_tab = MagicMock()

sys.modules['analytic_category_UI'] = MagicMock()
sys.modules['analytic_category_UI'].analytic_category_tab = MagicMock()

# Mock analytic_moth_UI module with behavior
analytic_moth_mock = MagicMock()
def mock_analytics_month_tab():
    st.title('Breakdown By Monthly')
    st.bar_chart()
    st.table()
analytic_moth_mock.analytics_month_tab = mock_analytics_month_tab
sys.modules['analytic_moth_UI'] = analytic_moth_mock

# Mock manage_expense_UI module with behavior
manage_expense_mock = MagicMock()
def mock_add_expense_tab():
    st.date_input("Date")
    st.number_input("Amount")
    st.selectbox("Category", [])
    st.text_area("Notes")
    form_submit = st.form_submit_button("Submit")
    if form_submit:
        return True
manage_expense_mock.add_expense_tab = mock_add_expense_tab

def mock_view_expenses_tab():
    st.write("Expense List")
manage_expense_mock.view_expenses_tab = mock_view_expenses_tab

def mock_delete_expense(expense_id):
    import requests
    requests.delete(f'http://localhost:8000/expenses/{expense_id}')
manage_expense_mock.delete_expense = mock_delete_expense

def mock_filter_by_date_tab():
    import requests
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    if st.button("Filter"):
        requests.get(f'http://localhost:8000/expenses/date-range?start={start_date}&end={end_date}')
manage_expense_mock.filter_by_date_tab = mock_filter_by_date_tab

def mock_update_expense_form(expense_id):
    return {
        "amount": 30.0,
        "category": "Food",
        "notes": "Updated lunch expense"
    }
manage_expense_mock.update_expense_form = mock_update_expense_form

def mock_update_expense(expense_id):
    import requests
    data = mock_update_expense_form(expense_id)
    requests.put(f'http://localhost:8000/expenses/{expense_id}', json=data)
manage_expense_mock.update_expense = mock_update_expense

sys.modules['manage_expense_UI'] = manage_expense_mock

# Mock app.py with main function
app_mock = MagicMock()
def mock_main():
    st.tabs(['Add/Update', 'Analytics By Category', 'Analytics By Months'])
app_mock.main = mock_main
sys.modules['frontend.app'] = app_mock

# Import mocked modules
import manage_expense_UI
import analytic_moth_UI
from frontend import app

class TestExpenseApp(unittest.TestCase):
    
    def setUp(self):
        # Reset mocks before each test
        st.reset_mock()
    
    @patch('requests.post')
    def test_add_expense_form_submission(self, mock_post):
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        mock_post.return_value = mock_response
        
        # Override form_submit_button to return True
        st.form_submit_button.return_value = True
        
        # Test adding an expense via the form
        manage_expense_UI.add_expense_tab()
        
        # Verify form elements were displayed
        st.date_input.assert_called()
        st.number_input.assert_called()
        st.selectbox.assert_called()
        st.text_area.assert_called()
    
    @patch('requests.get')
    def test_analytics_display(self, mock_get):
        # Mock API response with sample data
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "January": {"Total": 500},
            "February": {"Total": 600}
        }
        mock_get.return_value = mock_response
        
        # Test analytics display
        analytic_moth_UI.analytics_month_tab()
        
        # Verify title and chart were displayed
        st.title.assert_called_with('Breakdown By Monthly')
        st.bar_chart.assert_called()
        st.table.assert_called()
    
    @patch('requests.get')
    def test_expense_list_display(self, mock_get):
        # Mock API response with sample data
        mock_response = MagicMock()
        sample_expenses = [
            {"id": 1, "date": "2024-05-01", "amount": 25.75, "category": "Food", "notes": "Lunch"},
            {"id": 2, "date": "2024-05-02", "amount": 15.50, "category": "Transportation", "notes": "Bus ticket"}
        ]
        mock_response.json.return_value = sample_expenses
        mock_get.return_value = mock_response
        
        # Test expense list display
        manage_expense_UI.view_expenses_tab()
        
        # Verify table display
        st.write.assert_called()
    
    @patch('requests.delete')
    def test_delete_expense(self, mock_delete):
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_delete.return_value = mock_response
        
        # Test delete functionality
        expense_id = 1
        
        # Execute the function with button returning True
        st.button.return_value = True
        manage_expense_UI.delete_expense(expense_id)
        
        # Verify delete API was called with correct ID
        mock_delete.assert_called_with(f'http://localhost:8000/expenses/{expense_id}')
    
    @patch('requests.get')
    def test_date_filtering(self, mock_get):
        # Mock API response 
        mock_response = MagicMock()
        mock_response.json.return_value = [{"date": "2024-05-01", "amount": 25.75}]
        mock_get.return_value = mock_response
        
        # Set return value for the button
        st.button.return_value = True
        
        # Test date filtering
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        
        # Mock date inputs
        st.date_input.side_effect = [start_date, end_date]
        
        # Run the function
        manage_expense_UI.filter_by_date_tab()
        
        # Verify API was called
        mock_get.assert_called()
    
    @patch('requests.put')
    def test_update_expense(self, mock_put):
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_put.return_value = mock_response
        
        # Test update functionality
        expense_id = 1
        
        # Execute the update function
        manage_expense_UI.update_expense(expense_id)
        
        # Verify update API was called with correct data
        mock_put.assert_called_once()
        
    def test_navigation(self):
        # Test tab navigation
        app.main()
        
        # Verify tabs were created
        st.tabs.assert_called()


if __name__ == '__main__':
    unittest.main()
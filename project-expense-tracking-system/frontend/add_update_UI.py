import streamlit as st
from datetime import datetime
import requests

API_URL = 'http://localhost:8000'

def add_update_tab():
    selected_date = st.date_input('Enter Date', datetime(2024, 8, 2), label_visibility='collapsed')
    response = requests.get(f'{API_URL}/expenses/{selected_date}')
    if response.status_code == 200:
        existing_expenses = response.json()
    else:
        st.error('Failed to retrieve expenses')
        existing_expenses = []

    categories = ['Rent', 'Entertainment', 'Shopping', 'Food', 'Big Toy Shop', 'Other', " "]
    with st.form(key='expense_form'):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader('Amount')
        with col2:
            st.subheader('Category')
        with col3:
            st.subheader('Notes')

        expense = []  # List to create new data in DB

        for i in range(5):

            if i < len(existing_expenses):
                amount = existing_expenses[i]['amount']
                category = existing_expenses[i]['category']
                note = existing_expenses[i]['notes']
            else:
                amount = 0.0
                category = ' '
                note = ""

            with col1:
                amount_input = st.number_input(label='Amount', min_value=0.0, step=1.0, value=amount, key=f'amount_{i}',
                                               help="", label_visibility='collapsed')  # Remove the help text
            with col2:
                category_input = st.selectbox(label='Category', options=categories, index=categories.index(category),
                                              key=f'category_{i}', label_visibility='collapsed')
            with col3:
                notes_input = st.text_input(label="Notes", value=note, key=f'notes_{i}', label_visibility='collapsed')

            expense.append({
                'amount': amount_input,
                'category': category_input,
                'notes': notes_input
            })

        submit_button = st.form_submit_button("Submit")  # This button submits the form

        if submit_button:
            filter_expense = [data for data in expense if data['amount'] > 0]

            response = requests.post(f'{API_URL}/expenses/{selected_date}', json=filter_expense)
            if response.status_code == 200:
                st.success('Expenses Update Successfully')
            else:
                st.error('Failed To Update')
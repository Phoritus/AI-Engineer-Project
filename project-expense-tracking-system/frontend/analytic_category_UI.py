import streamlit as st
from datetime import datetime
import requests
import pandas as pd

API_URL = 'http://localhost:8000'


def analytic_category_tab():
    col1 ,col2 = st.columns(2)
    with col1:
        start_date = st.date_input('Start Date',datetime(2024,8,2))
    with col2:
        end_date = st.date_input('End Date', datetime(2024,9,29))

    if st.button('Get Analytics'):
        payload = {
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d')
        }

        response = requests.post(f'{API_URL}/analytic/date',json=payload)
        response = response.json()

        df = pd.DataFrame({
            'Category': list(response.keys()),
            'Total': [response[data]['Total'] for data in response],
            'Percentage': [response[data]['Percentage'] for data in response]
        })

        df_sorted = df.sort_values(by='Percentage', ascending=False)

        st.title('Breakdown By Category')

        st.bar_chart(data=df_sorted.set_index('Category')['Percentage'])

        df_sorted['Total'] = df_sorted['Total'].map('{:.2f}'.format)
        df_sorted['Percentage'] = df_sorted['Percentage'].map('{:.2f}'.format)

        st.table(df_sorted)


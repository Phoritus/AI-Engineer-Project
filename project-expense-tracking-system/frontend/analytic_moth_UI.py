import streamlit as st
import requests
import pandas as pd

API_URL = 'http://localhost:8000'

def analytics_month_tab():
    response = requests.get(f'{API_URL}/analytic/month')
    response = response.json()

    df = pd.DataFrame({
        'Month': list(response.keys()),
        'Total': [response[data]['Total'] for data in response]
    })
    
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                   'November', 'December']
    df['Month'] = pd.Categorical(df['Month'], categories=month_order, ordered=True)
    df = df.sort_values('Month')

    st.title('Breakdown By Monthly')
    
    st.bar_chart(data=df.set_index('Month')['Total'])
    
    table_df = df.copy()
    table_df['Total'] = table_df['Total'].map('{:.2f}'.format)
    table_df.index = range(1, len(table_df) + 1)
    
    st.table(table_df)

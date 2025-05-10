import streamlit as st
from add_update_UI  import add_update_tab
from analytic_category_UI import analytic_category_tab
from analytic_moth_UI import analytics_month_tab

st.title('Expense Tracking System')

tab1, tab2, tab3 = st.tabs(['Add/Update', 'Analytics By Category','Analytics By Months'])

with tab1:
    add_update_tab()

with tab2:
    analytic_category_tab()

with tab3:
    analytics_month_tab()
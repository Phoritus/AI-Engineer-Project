from fastapi import FastAPI, HTTPException
from datetime import date
from pydantic import BaseModel
from typing import List
import db_helper

app = FastAPI()

class Expenses(BaseModel):
    amount: float
    category: str
    notes: str

class RangeDate(BaseModel):
    start_date:date
    end_date:date


@app.get('/expenses/{expense_date}',response_model=List[Expenses])
def get_By_date(expense_date: date):
    expense = db_helper.get_by_date(expense_date)
    return expense


@app.post('/expenses/{expense_date}')
def add_or_update(expense_date: date,expense:List[Expenses]):
    db_helper.delete_data(expense_date)
    for data in expense:
        db_helper.insert_data(expense_date, data.amount, data.category, data.notes)
    return {'message': "Update Successfully"}


@app.post('/analytic/date')
def fetch_sum_data(data_range:RangeDate):
    data = db_helper.fetch_sum_date(data_range.start_date, data_range.end_date)
    if data is None:
        raise HTTPException(status_code=500,detail='Failed to retrieve summarize from DataBase')

    total = sum([row['Total'] for row in data])
    expenses = {}

    for row in data:
        percent = (row['Total']/total)*100
        expenses[row['category']] = {
            'Total':row['Total'],
            'Percentage':percent
        }

    return expenses


@app.get('/analytic/month')
def fetch_sum_month():
    data = db_helper.fetch_sum_months()
    if data is None:
        raise HTTPException(status_code=500,detail='Failed to retrieve summarize from DataBase')

    month_names = {
        1: "January", 2: "February", 3: "March", 4: "April",
        5: "May", 6: "June", 7: "July", 8: "August",
        9: "September", 10: "October", 11: "November", 12: "December"
    }

    expenses = {}

    for row in data:
        month_name = month_names[row['month']]
        expenses[month_name] ={
            'Total': row['total']
        }

    return expenses
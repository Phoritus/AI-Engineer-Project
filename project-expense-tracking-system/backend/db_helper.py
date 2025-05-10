import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logging

logger = setup_logging('db_helper')

@contextmanager
def connection(commit=False):
    connect = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '12345',
        database = 'expense_manager'
    )

    if connect.is_connected():
        print('Connection Successful')
    else:
        print('Connection Error')

    cursor = connect.cursor(dictionary=True)

    yield cursor

    if commit:
        connect.commit()
    cursor.close()
    connect.close()

def get_all_data():
    logger.info(f'fetch_expenses_for_All_Data')
    with connection() as cursor:
        cursor.execute("SELECT * FROM expenses;")
        expenses = cursor.fetchall()
        for data in expenses:
            print(data)


def get_by_date(date):
    logger.info(f'fetch_expenses_for_date called with {date}')
    with connection() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s;", (date,))
        expenses = cursor.fetchall()
        return expenses


def insert_data(date,amount,category,notes):
    logger.info(f'Insert_expense_data_in_date {date}')
    with connection(commit=True) as cursor:
        cursor.execute("insert into expenses (expense_date,amount,category,notes) values (%s,%s,%s,%s);",
                       (date,amount,category,notes))


def delete_data(date):
    logger.info(f'Delete_expense_in_date {date}')
    with connection(commit=True) as cursor:
        cursor.execute("delete from expenses where expense_date = %s ;",(date,))

def get_by_id(ids):
    with connection() as cursor:
        cursor.execute("select * from expenses where id = %s ;",ids)
        expenses = cursor.fetchall()
        return expenses

def fetch_sum_date(start_date,end_date):
    logger.info(f'fetch_sum_date start_date:{start_date}, end_date:{end_date}')
    with connection() as cursor:
        cursor.execute("select category,sum(amount) as Total from expenses where expense_date between %s and %s group by category;",
                       (start_date,end_date))
        return cursor.fetchall()


def fetch_sum_months():
    logger.info('fetch_sum_by_months')
    query = """
            SELECT MONTH(expense_date) AS month, SUM(amount) AS total FROM expenses 
            WHERE YEAR(expense_date) = 2024
            GROUP BY MONTH(expense_date) 
            ORDER BY MONTH(expense_date);
            """
    with connection() as cursor:
        cursor.execute(query)
        expense = cursor.fetchall()

        return expense






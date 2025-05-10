# 💰 Expense Tracking System

A comprehensive expense tracking system with analytical data visualization capabilities.

## 🔍 Project Overview

This system was developed to help manage and track personal or business expenses with the following key features:
- 📝 Record and manage expenses
- 📊 Analyze expenses by category and time period
- 📈 Display data in graphs and tables
- 🔎 Filter data by date and category

## 🏗️ System Architecture

The project is divided into two main components:

### ⚙️ Backend
- **FastAPI**: Provides RESTful API for data management
- **MySQL**: Database for storing expense data
- **db_helper.py**: Module for managing connections and SQL commands

### 🖥️ Frontend
- **Streamlit**: Creates an easy-to-use and interactive UI
- **Pandas**: Manages and analyzes data
- **Matplotlib/Streamlit Charts**: Visualizes data

## 📁 File Structure

```
project-expense-tracking-system/
├── backend/
│   ├── db_helper.py            # Database management
│   └── server.py               # FastAPI server
├── frontend/
│   ├── app.py                  # Main Streamlit application
│   ├── add_update_UI.py        # UI for adding/updating expenses
│   ├── analytic_category_UI.py # UI for category analysis
│   ├── analytic_moth_UI.py     # UI for monthly analysis
│   └── manage_expense_UI.py    # UI for expense management
├── test/
│   ├── backend/
│   │   └── test_db_helper.py   # Database module tests
│   └── frontend/
│       └── test_frontend.py    # UI tests
├── logging_setup.py            # Logging configuration
└── README.md                   # This document
```

## ✨ Features

### 💼 Expense Management
- ➕ **Add Expense**: Record date, amount, category, and notes
- ✏️ **Edit Expense**: Update existing records
- 🗑️ **Delete Expense**: Remove entries from the system
- 📋 **View Listings**: Display all expenses in tabular format

### 📊 Data Analysis
- 🍕 **Category Analysis**: Show expense distribution by category with pie charts
- 📊 **Monthly Analysis**: Display monthly expenses with bar charts
- 📅 **Date Filtering**: View expenses within a specified time period

## 🔧 Installation

### Prerequisites
- Python 3.12+
- MySQL Server
- pip (Python package manager)

### Steps

1. **Clone the project**
   ```bash
   git clone https://github.com/yourusername/project-expense-tracking-system.git
   cd project-expense-tracking-system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup MySQL database**
   - Create a database named `expense_manager`
   ```sql
   CREATE DATABASE expense_manager;
   ```
   - Modify connection details in db_helper.py as appropriate

4. **Create database table**
   ```sql
   USE expense_manager;
   CREATE TABLE expenses (
     id INT AUTO_INCREMENT PRIMARY KEY,
     date DATE NOT NULL,
     amount DECIMAL(10,2) NOT NULL,
     category VARCHAR(100) NOT NULL,
     notes TEXT
   );
   ```

## 🚀 Usage

### Starting the Backend
```bash
cd backend
uvicorn server:app --reload
```
The Backend API will run at http://localhost:8000

### Starting the Frontend
```bash
cd frontend
streamlit run app.py
```
Open your browser and go to the displayed URL (typically http://localhost:8501)

## 📖 How to Use

### Adding an Expense
1. Select the "Add/Update" tab
2. Enter data: date, amount, category, and notes
3. Click "Submit"

### Analyzing Expenses
1. Select the "Analytics By Category" or "Analytics By Months" tab
2. To filter by date, select start and end dates
3. Click the "Filter" or "Get Analytics" button

## 🧪 Testing

The system includes tests for both backend and frontend:

### Backend Testing
```bash
pytest test/backend/test_db_helper.py
```

### Frontend Testing
```bash
pytest test/frontend/test_frontend.py
```

## 🔮 Future Development

Features that can be developed further:
- 🔐 Add user system and authentication
- 📤 Add ability to export data as CSV or Excel files
- 📉 Add additional analytical data displays such as future expense forecasting
- 📱 Develop a mobile application for recording expenses anywhere

## 💻 Technologies Used

- **Python**: Main development language for the entire system
- **FastAPI**: Modern web API framework
- **Streamlit**: Web UI framework for analytical data
- **MySQL**: Relational database management system
- **Pandas**: Data management and analysis
- **Pytest**: Automated testing

## 📋 Summary

This expense tracking system is a full-stack application that allows users to easily track and analyze spending patterns. By separating the frontend and backend, future development and customization can be done flexibly.
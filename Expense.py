import streamlit as st
import json
import os
import uuid

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="icon.png",
    layout="centered",
)

# File to save the expenses
EXPENSE_FILE = 'expenses.json'

# Load expenses from file
def load_expenses():
    if os.path.exists(EXPENSE_FILE):
        try:
            with open(EXPENSE_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []

# Save expenses to file
def save_expenses(expenses):
    with open(EXPENSE_FILE, 'w') as f:
        json.dump(expenses, f)

# Generate a unique session ID if it doesn't exist
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    # Clear expenses for new session
    st.session_state.expenses = []

# Function to add an expense
def add_expense(item_name, item_amount):
    if item_name and item_amount:
        st.session_state.expenses.append({'name': item_name, 'amount': float(item_amount)})
        save_expenses(st.session_state.expenses)

# Function to clear all expenses
def clear_expenses():
    st.session_state.expenses = []
    save_expenses(st.session_state.expenses)

st.title('EXPENSE TRACKER')

item_name = st.text_input('Item Name')
item_amount = st.text_input('Item Amount (₹)')

if st.button('Add Expense'):
    add_expense(item_name, item_amount)

if st.button('Clear All'):
    clear_expenses()

total_amount = sum(expense['amount'] for expense in st.session_state.expenses)

st.write('## Expenses')
for expense in st.session_state.expenses:
    st.write(f"{expense['name']}: ₹{expense['amount']}")

st.write(f'## Total: ₹{total_amount}')
